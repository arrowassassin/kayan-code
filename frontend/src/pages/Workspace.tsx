import { useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router-dom'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import {
  BookOpenText,
  Eraser,
  History,
  Lightbulb,
  Lock,
  Play,
  RotateCcw,
  UploadCloud,
} from 'lucide-react'
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels'
import { api, type JudgeResult, type TestCase } from '@/lib/api'
import { LANGUAGES, langById, starterFor } from '@/lib/languages'
import { cn, fmtClock, fmtMs, timeAgo } from '@/lib/utils'
import { Badge, DifficultyBadge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Spinner, Textarea } from '@/components/ui/inputs'
import { CodeEditor, type EditorMode } from '@/components/CodeEditor'
import { Markdown } from '@/components/Markdown'
import { ResultsPanel } from '@/components/ResultsPanel'
import { AIReviewButton } from '@/components/AIReview'

type UiMode = EditorMode | 'whiteboard'

const TARGET_SECONDS = 25 * 60 // Medium target: 25 minutes

/** Practice stopwatch: starts on first keystroke, persists per slug. */
function useStopwatch(slug: string) {
  const key = `kayan-timer:${slug}`
  const [startedAt, setStartedAt] = useState<number | null>(() => {
    const v = localStorage.getItem(key)
    return v ? Number(v) : null
  })
  const [nowTick, setNowTick] = useState(Date.now())
  useEffect(() => {
    const v = localStorage.getItem(key)
    setStartedAt(v ? Number(v) : null)
  }, [key])
  useEffect(() => {
    if (startedAt === null) return
    const t = setInterval(() => setNowTick(Date.now()), 1000)
    return () => clearInterval(t)
  }, [startedAt])
  const start = () => {
    if (localStorage.getItem(key)) return
    const ts = Date.now()
    localStorage.setItem(key, String(ts))
    setStartedAt(ts)
  }
  const reset = () => {
    localStorage.removeItem(key)
    setStartedAt(null)
  }
  const elapsed =
    startedAt === null ? 0 : Math.floor((nowTick - startedAt) / 1000)
  return { elapsed, running: startedAt !== null, start, reset }
}

function useSavedCode(cacheKey: string, starter: string | undefined) {
  const key = `kayan-code:${cacheKey}`
  const [code, setCode] = useState<string>('')
  // the key that `code` currently belongs to — guards the persist effect from
  // writing the old language's code into a freshly-switched key.
  const codeKey = useRef<string | null>(null)

  useEffect(() => {
    if (starter === undefined) return
    const saved = localStorage.getItem(key)
    setCode(saved ?? starter)
    codeKey.current = key
  }, [key, starter])

  useEffect(() => {
    if (codeKey.current === key && code) localStorage.setItem(key, code)
  }, [key, code])

  return [code, setCode] as const
}

export function ProblemPage() {
  const { slug = '' } = useParams()
  return <Workspace slug={slug} />
}

export function Workspace({
  slug,
  mock,
}: {
  slug: string
  mock?: {
    sessionId: string
    onAccepted?: () => void
    locked?: boolean
  }
}) {
  const locked = mock?.locked ?? false
  const qc = useQueryClient()
  const { data: problem } = useQuery({
    queryKey: ['problem', slug],
    queryFn: () => api.problem(slug),
  })
  const [language, setLanguage] = useState('python')
  const { data: langStarter, isFetching: starterFetching } = useQuery({
    queryKey: ['starter', slug, language],
    queryFn: () => api.starter(slug, language),
    enabled: !!problem && language !== 'python',
    staleTime: Infinity,
  })
  // Keep starter undefined until the real per-language stub arrives, so the
  // saved-code hook never persists the comment-contract fallback over it.
  const starter =
    problem === undefined
      ? undefined
      : language === 'python'
        ? problem.starter
        : langStarter?.starter ??
          (starterFetching
            ? undefined
            : starterFor(langById(language), problem.starter))
  const [code, setCode] = useSavedCode(`${slug}:${language}`, starter)
  const [uiMode, setUiMode] = useState<UiMode>(mock ? 'interview' : 'practice')
  const [bottomTab, setBottomTab] = useState<'tests' | 'result'>('tests')
  const [result, setResult] = useState<JudgeResult | null>(null)
  const [cases, setCases] = useState<TestCase[] | null>(null)
  const [fontSize, setFontSize] = useState(() =>
    Number(localStorage.getItem('kayan-font') ?? 14),
  )
  const stopwatch = useStopwatch(slug)

  useEffect(() => {
    setResult(null)
    setCases(null)
    setBottomTab('tests')
  }, [slug])
  useEffect(() => {
    localStorage.setItem('kayan-font', String(fontSize))
  }, [fontSize])

  const editorMode: EditorMode = uiMode === 'practice' ? 'practice' : 'interview'
  const effectiveCases = cases ?? problem?.visible_tests ?? []

  const onCodeChange = (v: string) => {
    setCode(v)
    if (!mock) stopwatch.start() // practice clock starts on first keystroke
  }

  const runMut = useMutation({
    mutationFn: () => api.run(slug, code, cases ?? undefined, language),
    onSuccess: (r) => {
      setResult(r)
      setBottomTab('result')
    },
    onError: (e: Error) => toast.error(e.message),
  })
  const submitMut = useMutation({
    mutationFn: () =>
      api.submit(
        slug,
        code,
        mock ? 'mock' : uiMode,
        mock?.sessionId,
        language,
        mock ? undefined : stopwatch.elapsed || undefined,
      ),
    onSuccess: (r) => {
      setResult(r)
      setBottomTab('result')
      qc.invalidateQueries({ queryKey: ['problems'] })
      qc.invalidateQueries({ queryKey: ['submissions', slug] })
      qc.invalidateQueries({ queryKey: ['stats'] })
      if (r.verdict === 'AC') {
        toast.success('Accepted 🎉')
        if (!mock) stopwatch.reset()
        if (mock?.onAccepted) mock.onAccepted()
      } else if (r.status === 'ok') {
        toast.error(`${r.verdict} — ${r.passed}/${r.total} cases passed`)
      }
    },
    onError: (e: Error) => toast.error(e.message),
  })
  const busy = runMut.isPending || submitMut.isPending

  // keyboard: Cmd/Ctrl-Enter = Run, Cmd/Ctrl-Shift-Enter = Submit
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
        e.preventDefault()
        if (busy || locked) return
        if (e.shiftKey) submitMut.mutate()
        else if (uiMode !== 'whiteboard') runMut.mutate()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [busy, uiMode, code, language, cases]) // eslint-disable-line react-hooks/exhaustive-deps

  if (!problem) {
    return (
      <div className="flex h-full items-center justify-center text-ink-dim">
        <Spinner className="mr-2" /> Loading problem…
      </div>
    )
  }

  return (
    <PanelGroup
      direction="horizontal"
      autoSaveId="kayan-hsplit"
      className="h-[calc(100vh-56px)] p-3"
    >
      {/* left: statement / editorial / hints / submissions */}
      <Panel defaultSize={44} minSize={26}>
      <section className="flex h-full min-h-0 flex-col overflow-hidden rounded-xl border border-line bg-panel">
        <Tabs defaultValue="description" className="flex min-h-0 flex-1 flex-col">
          <TabsList>
            <TabsTrigger value="description">
              <BookOpenText size={14} className="mr-1.5 inline" />
              Description
            </TabsTrigger>
            {!mock && <TabsTrigger value="editorial">Editorial</TabsTrigger>}
            {!mock && (
              <TabsTrigger value="hints">
                <Lightbulb size={14} className="mr-1.5 inline" />
                Hints
              </TabsTrigger>
            )}
            <TabsTrigger value="submissions">
              <History size={14} className="mr-1.5 inline" />
              Submissions
            </TabsTrigger>
          </TabsList>
          <TabsContent value="description" className="overflow-auto p-5">
            <div className="mb-3.5 flex flex-wrap items-center gap-2">
              <h1 className="mr-2 text-xl font-bold">
                {problem.id}. {problem.title}
              </h1>
              <DifficultyBadge difficulty={problem.difficulty} />
              {problem.snowflake_priority === 1 && (
                <Badge variant="priority">★ Snowflake</Badge>
              )}
              {problem.topics.map((t) => (
                <Badge key={t}>{t}</Badge>
              ))}
            </div>
            <Markdown>{problem.statement.replace(/^#\s.*\n+/, '')}</Markdown>
          </TabsContent>
          {!mock && (
            <TabsContent value="editorial" className="overflow-auto p-5">
              <EditorialTab slug={slug} />
            </TabsContent>
          )}
          {!mock && (
            <TabsContent value="hints" className="overflow-auto p-5">
              <HintsTab hints={problem.hints} />
            </TabsContent>
          )}
          <TabsContent value="submissions" className="overflow-auto p-5">
            <SubmissionsTab slug={slug} onLoadCode={setCode} />
          </TabsContent>
        </Tabs>
      </section>
      </Panel>

      <PanelResizeHandle className="group mx-1 flex w-1.5 items-center justify-center">
        <div className="h-10 w-1 rounded-full bg-line transition-colors group-hover:bg-accent group-data-[resize-handle-state=drag]:bg-accent" />
      </PanelResizeHandle>

      {/* right: editor + tests */}
      <Panel defaultSize={56} minSize={30}>
      <PanelGroup direction="vertical" autoSaveId="kayan-vsplit" className="gap-0">
        <Panel defaultSize={62} minSize={20}>
        <div className="flex h-full min-h-0 flex-col overflow-hidden rounded-xl border border-line bg-panel">
          <div className="flex shrink-0 items-center gap-2.5 border-b border-line px-3 py-2">
            {mock ? (
              <span className="font-mono text-[12.5px] text-ink-faint">python3</span>
            ) : (
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="cursor-pointer rounded-lg border border-line bg-bg2 px-2 py-1 font-mono text-[12.5px] text-ink-dim outline-none transition-colors hover:border-accent focus:border-accent"
                title="Non-Python solutions are AI-translated to Python before judging (needs OPENROUTER_API_KEY)"
              >
                {LANGUAGES.map((l) => (
                  <option key={l.id} value={l.id}>
                    {l.label}
                    {l.id !== 'python' ? ' (AI→py)' : ''}
                  </option>
                ))}
              </select>
            )}
            {!mock && (
              <div className="flex overflow-hidden rounded-lg border border-line">
                {(['practice', 'interview', 'whiteboard'] as const).map((m) => (
                  <button
                    key={m}
                    onClick={() => setUiMode(m)}
                    className={cn(
                      'cursor-pointer px-3 py-1 text-xs font-semibold capitalize transition-colors',
                      uiMode === m
                        ? 'bg-accent/18 text-ink'
                        : 'text-ink-dim hover:text-ink',
                    )}
                    title={
                      m === 'interview'
                        ? 'All editor assists off — like CoderPad with assists disabled'
                        : m === 'whiteboard'
                          ? 'Run disabled — submit blind, like an interviewer who turned off execution'
                          : 'Bracket matching on'
                    }
                  >
                    {m}
                  </button>
                ))}
              </div>
            )}
            {mock && (
              <Badge variant="outline" className="text-accent2">
                interview editor — assists off
              </Badge>
            )}
            <div className="ml-auto flex items-center gap-2">
              {!mock && (
                <span
                  className={cn(
                    'font-mono text-[13px] tabular-nums',
                    stopwatch.elapsed >= TARGET_SECONDS
                      ? 'text-medium'
                      : 'text-ink-faint',
                  )}
                  title="Practice stopwatch — starts on your first keystroke; amber past the 25-min Medium target"
                >
                  {stopwatch.running ? fmtClock(stopwatch.elapsed) : '25:00 target'}
                </span>
              )}
              <div className="flex items-center rounded-lg border border-line text-ink-dim">
                <button
                  onClick={() => setFontSize((f) => Math.max(11, f - 1))}
                  className="cursor-pointer px-2 py-1 text-xs hover:text-ink"
                  title="Smaller font"
                >
                  A-
                </button>
                <button
                  onClick={() => setFontSize((f) => Math.min(22, f + 1))}
                  className="cursor-pointer px-2 py-1 text-sm hover:text-ink"
                  title="Larger font"
                >
                  A+
                </button>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => {
                  setCode(starter ?? problem.starter)
                  if (!mock) stopwatch.reset()
                  toast('Reset to starter code')
                }}
              >
                <RotateCcw size={14} /> Reset
              </Button>
            </div>
          </div>
          <div className="min-h-0 flex-1 overflow-auto">
            <CodeEditor
              value={code}
              onChange={onCodeChange}
              mode={editorMode}
              language={mock ? 'python' : language}
              fontSize={fontSize}
              readOnly={locked}
            />
          </div>
        </div>
        </Panel>

        <PanelResizeHandle className="group my-1 flex h-1.5 items-center justify-center">
          <div className="h-1 w-10 rounded-full bg-line transition-colors group-hover:bg-accent group-data-[resize-handle-state=drag]:bg-accent" />
        </PanelResizeHandle>

        <Panel defaultSize={38} minSize={12}>

        <div className="flex h-full min-h-0 flex-col overflow-hidden rounded-xl border border-line bg-panel">
          <div className="flex shrink-0 items-center border-b border-line px-2.5 pt-1.5">
            <button
              onClick={() => setBottomTab('tests')}
              className={cn(
                'cursor-pointer border-b-2 px-4 py-2 text-[13.5px] font-semibold transition-colors',
                bottomTab === 'tests'
                  ? 'border-accent text-ink'
                  : 'border-transparent text-ink-dim hover:text-ink',
              )}
            >
              Testcase
            </button>
            <button
              onClick={() => setBottomTab('result')}
              className={cn(
                'cursor-pointer border-b-2 px-4 py-2 text-[13.5px] font-semibold transition-colors',
                bottomTab === 'result'
                  ? 'border-accent text-ink'
                  : 'border-transparent text-ink-dim hover:text-ink',
              )}
            >
              Result {busy && <Spinner className="ml-1 size-3" />}
            </button>
            <div className="ml-auto flex items-center gap-2 pb-1.5">
              <Button
                size="sm"
                onClick={() => runMut.mutate()}
                disabled={busy || locked || uiMode === 'whiteboard'}
                title={
                  uiMode === 'whiteboard'
                    ? 'Whiteboard mode: Run is disabled — submit when confident'
                    : 'Run against the visible testcases  (⌘/Ctrl+Enter)'
                }
              >
                {uiMode === 'whiteboard' ? <Lock size={14} /> : <Play size={14} />}
                Run
              </Button>
              <Button
                variant="primary"
                size="sm"
                onClick={() => submitMut.mutate()}
                disabled={busy || locked}
                title="Submit against the full hidden suite  (⌘/Ctrl+Shift+Enter)"
              >
                <UploadCloud size={14} /> Submit
              </Button>
            </div>
          </div>
          <div className="min-h-0 flex-1 overflow-auto">
            {bottomTab === 'tests' ? (
              <TestcaseEditor
                cases={effectiveCases}
                hiddenCount={problem.hidden_count}
                onChange={setCases}
                onReset={() => setCases(null)}
                edited={cases !== null}
              />
            ) : result ? (
              <ResultsPanel result={result} entry={problem.judge?.entry} />
            ) : (
              <div className="p-5 text-[13.5px] text-ink-faint">
                {busy ? 'Judging…' : 'Run or submit to see results.'}
              </div>
            )}
          </div>
        </div>
        </Panel>
      </PanelGroup>
      </Panel>
    </PanelGroup>
  )
}

/* ---------------- testcase editor ---------------- */

function TestcaseEditor({
  cases,
  hiddenCount,
  onChange,
  onReset,
  edited,
}: {
  cases: TestCase[]
  hiddenCount: number
  onChange: (c: TestCase[]) => void
  onReset: () => void
  edited: boolean
}) {
  const [sel, setSel] = useState(0)
  const selIdx = Math.min(sel, cases.length - 1)
  const c = cases[selIdx]
  const [inputText, setInputText] = useState('')
  const [inputErr, setInputErr] = useState(false)

  useEffect(() => {
    setInputText(c ? JSON.stringify(c.input) : '')
    setInputErr(false)
  }, [selIdx, cases.length]) // eslint-disable-line react-hooks/exhaustive-deps

  if (!c) return null

  const commitInput = (text: string) => {
    setInputText(text)
    try {
      const parsed = JSON.parse(text)
      if (!Array.isArray(parsed)) throw new Error()
      setInputErr(false)
      const next = cases.map((x, i) => (i === selIdx ? { ...x, input: parsed } : x))
      onChange(next)
    } catch {
      setInputErr(true)
    }
  }

  return (
    <div className="p-4">
      <div className="mb-3 flex flex-wrap items-center gap-1.5">
        {cases.map((_, i) => (
          <button
            key={i}
            onClick={() => setSel(i)}
            className={cn(
              'cursor-pointer rounded-lg border border-line bg-panel2 px-3 py-1 text-[12.5px] font-semibold text-ink-dim transition-colors hover:text-ink',
              i === selIdx && 'border-accent text-ink',
            )}
          >
            Case {i + 1}
          </button>
        ))}
        <button
          onClick={() => {
            onChange([...cases, { input: cases[selIdx].input, expected: cases[selIdx].expected }])
            setSel(cases.length)
          }}
          className="cursor-pointer rounded-lg border border-dashed border-line px-3 py-1 text-[12.5px] font-semibold text-ink-faint hover:border-accent hover:text-ink"
        >
          +
        </button>
        {edited && (
          <Button variant="ghost" size="sm" className="ml-auto" onClick={onReset}>
            <Eraser size={13} /> Reset cases
          </Button>
        )}
        <span className={cn('text-xs text-ink-faint', !edited && 'ml-auto')}>
          + {hiddenCount} hidden on submit
        </span>
      </div>
      <div className="mb-1 text-[11.5px] font-semibold uppercase tracking-wider text-ink-faint">
        Input (JSON array of arguments)
      </div>
      <Textarea
        value={inputText}
        onChange={(e) => commitInput(e.target.value)}
        spellCheck={false}
        className={cn('min-h-[64px] font-mono text-[13px]', inputErr && 'border-hard')}
      />
      {inputErr && (
        <div className="mt-1 text-xs text-hard">Not a valid JSON array — case not saved.</div>
      )}
      {c.expected !== undefined && (
        <>
          <div className="mb-1 mt-3 text-[11.5px] font-semibold uppercase tracking-wider text-ink-faint">
            Expected
          </div>
          <pre className="m-0 whitespace-pre-wrap break-all rounded-lg border border-line bg-bg2 px-3 py-2 font-mono text-[13px]">
            {JSON.stringify(c.expected)}
          </pre>
        </>
      )}
    </div>
  )
}

/* ---------------- editorial / hints / submissions tabs ---------------- */

function EditorialTab({ slug }: { slug: string }) {
  const [revealed, setRevealed] = useState(false)
  const { data, isLoading, error } = useQuery({
    queryKey: ['editorial', slug],
    queryFn: () => api.editorial(slug),
    enabled: revealed,
  })
  if (!revealed)
    return (
      <div className="flex flex-col items-start gap-3">
        <p className="text-ink-dim">
          The editorial walks brute force → key insight → optimal, with the
          spoken complexity justification and the interviewer follow-up. Try
          the problem first.
        </p>
        <Button onClick={() => setRevealed(true)}>Show editorial</Button>
      </div>
    )
  if (isLoading) return <Spinner />
  if (error) return <p className="text-ink-dim">No editorial yet.</p>
  return <Markdown>{data!.editorial}</Markdown>
}

function HintsTab({ hints }: { hints: string[] }) {
  const [shown, setShown] = useState(0)
  if (!hints.length) return <p className="text-ink-dim">No hints for this one.</p>
  return (
    <div className="flex flex-col gap-3">
      {hints.map((h, i) =>
        i < shown ? (
          <div key={i} className="rounded-xl border border-dashed border-line-bright p-4">
            <div className="mb-1 text-xs font-bold uppercase tracking-wider text-accent2">
              Hint {i + 1}
            </div>
            <Markdown>{h}</Markdown>
          </div>
        ) : (
          <button
            key={i}
            onClick={() => setShown(i + 1)}
            disabled={i > shown}
            className={cn(
              'cursor-pointer rounded-xl border border-dashed border-line-bright p-4 text-left text-ink-faint transition-colors hover:border-accent hover:text-ink-dim',
              i > shown && 'cursor-not-allowed opacity-50',
            )}
          >
            <Lightbulb size={15} className="mr-2 inline" />
            Reveal hint {i + 1} of {hints.length}
          </button>
        ),
      )}
    </div>
  )
}

export function SubmissionsTab({
  slug,
  onLoadCode,
}: {
  slug: string
  onLoadCode?: (code: string) => void
}) {
  const { data: subs = [] } = useQuery({
    queryKey: ['submissions', slug],
    queryFn: () => api.submissions(slug),
  })
  const [openId, setOpenId] = useState<number | null>(null)
  const { data: detail } = useQuery({
    queryKey: ['submission', openId],
    queryFn: () => api.submission(openId!),
    enabled: openId !== null,
  })

  if (!subs.length)
    return <p className="text-ink-dim">No submissions yet — go on, submit something.</p>

  return (
    <div>
      {subs.map((s) => (
        <div key={s.id}>
          <button
            onClick={() => setOpenId(openId === s.id ? null : s.id)}
            className="flex w-full cursor-pointer items-center gap-3.5 rounded-lg border-b border-line/55 px-2 py-2.5 text-left transition-colors hover:bg-accent/6"
          >
            <span
              className={cn(
                'min-w-[42px] text-[13px] font-bold',
                s.verdict === 'AC'
                  ? 'text-easy'
                  : s.verdict === 'TLE'
                    ? 'text-medium'
                    : 'text-hard',
              )}
            >
              {s.verdict}
            </span>
            <span className="text-[13px] text-ink-dim">
              {s.passed}/{s.total} · {fmtMs(s.runtime_ms)}
            </span>
            {s.mode !== 'practice' && <Badge>{s.mode}</Badge>}
            {s.language && s.language !== 'python' && (
              <Badge variant="outline">{s.language} → py</Badge>
            )}
            <span className="ml-auto text-xs text-ink-faint">{timeAgo(s.created_at)}</span>
          </button>
          {openId === s.id && detail && (
            <div className="my-2 rounded-lg border border-line bg-bg2 p-3">
              <pre className="m-0 max-h-64 overflow-auto whitespace-pre-wrap font-mono text-[12.5px]">
                {detail.code}
              </pre>
              <div className="mt-2 flex gap-2">
                {onLoadCode && (
                  <Button size="sm" onClick={() => onLoadCode(detail.code)}>
                    Load into editor
                  </Button>
                )}
                <AIReviewButton submissionId={s.id} />
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
