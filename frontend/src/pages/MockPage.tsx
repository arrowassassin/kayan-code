import { useEffect, useRef, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { toast } from 'sonner'
import { AlarmClock, Mic, PartyPopper, Timer } from 'lucide-react'
import { api, type MockSession } from '@/lib/api'
import { cn, fmtClock } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Checkbox, Spinner, Textarea } from '@/components/ui/inputs'
import { Workspace } from '@/pages/Workspace'
import { AIReviewButton } from '@/components/AIReview'
import { Markdown } from '@/components/Markdown'
import { useQuery as useRQ } from '@tanstack/react-query'

const NUDGE_EVERY_MS = 8 * 60 * 1000

export function MockPage() {
  const [sessionId, setSessionId] = useState<string | null>(
    () => localStorage.getItem('kayan-mock-session'),
  )
  const qc = useQueryClient()

  const { data: session } = useQuery({
    queryKey: ['mock', sessionId],
    queryFn: () => api.mock(sessionId!),
    enabled: !!sessionId,
    refetchInterval: 15_000,
  })

  const startMut = useMutation({
    mutationFn: () => api.mockStart(),
    onSuccess: (s) => {
      localStorage.setItem('kayan-mock-session', s.id)
      setSessionId(s.id)
      qc.setQueryData(['mock', s.id], s)
    },
    onError: (e: Error) => toast.error(e.message),
  })

  const clear = () => {
    localStorage.removeItem('kayan-mock-session')
    setSessionId(null)
  }

  if (!sessionId || !session) return <StartScreen onStart={() => startMut.mutate()} starting={startMut.isPending} />
  if (session.stage === 'done') return <Debrief session={session} onNew={clear} />
  return <LiveSession session={session} onAbandon={clear} />
}

function StartScreen({ onStart, starting }: { onStart: () => void; starting: boolean }) {
  const steps = [
    ['Clarify', 'Type 2–3 clarifying questions before the editor unlocks.'],
    ['Approach', 'One paragraph + time/space complexity, out loud.'],
    ['Code', '60-min clock, assists off, narration nudges every 8 min.'],
    ['Follow-up', 'Pass the warmup and the harder extension appears.'],
  ]
  return (
    <main className="mx-auto max-w-3xl px-6 py-14 text-center">
      <h1 className="text-4xl font-extrabold">
        Mock <span className="grad-text">Interview</span>
      </h1>
      <p className="mx-auto mt-3 max-w-xl text-ink-dim">
        A faithful rehearsal of Snowflake's 60-minute coding round: warmup +
        hidden harder follow-up, communication gates, no editor assists, AI
        debrief only after the clock stops.
      </p>
      <div className="my-9 grid grid-cols-2 gap-3 text-left md:grid-cols-4">
        {steps.map(([title, desc], i) => (
          <Card key={title} className="p-4">
            <div className="mb-2 flex size-7 items-center justify-center rounded-full grad-bg text-[13px] font-extrabold text-bg">
              {i + 1}
            </div>
            <b className="mb-1 block">{title}</b>
            <span className="text-[12.5px] text-ink-dim">{desc}</span>
          </Card>
        ))}
      </div>
      <Button variant="primary" size="lg" onClick={onStart} disabled={starting}>
        {starting ? <Spinner /> : <Timer size={17} />} Start 60-minute session
      </Button>
    </main>
  )
}

/* ---------------- live session ---------------- */

function useCountdown(session: MockSession) {
  const [remaining, setRemaining] = useState(session.remaining_seconds)
  useEffect(() => {
    setRemaining(session.remaining_seconds)
    const t = setInterval(() => setRemaining((r) => Math.max(0, r - 1)), 1000)
    return () => clearInterval(t)
  }, [session.remaining_seconds])
  return remaining
}

function LiveSession({ session, onAbandon }: { session: MockSession; onAbandon: () => void }) {
  const qc = useQueryClient()
  const remaining = useCountdown(session)
  const { data: warmup } = useRQ({
    queryKey: ['problem', session.warmup_slug],
    queryFn: () => api.problem(session.warmup_slug),
  })

  // narration nudge every ~8 minutes while coding
  const nudgeTimer = useRef<ReturnType<typeof setInterval> | null>(null)
  useEffect(() => {
    if (session.stage !== 'coding') return
    nudgeTimer.current = setInterval(() => {
      toast('🎙️ Narrate: say out loud what the block you are writing does — and why.', {
        duration: 10_000,
      })
    }, NUDGE_EVERY_MS)
    return () => {
      if (nudgeTimer.current) clearInterval(nudgeTimer.current)
    }
  }, [session.stage])

  // follow-up reveal toast
  const revealedRef = useRef(false)
  useEffect(() => {
    if (session.followup_revealed && session.followup_slug && !revealedRef.current) {
      revealedRef.current = true
      toast.success('Follow-up unlocked — the harder extension is now available below the warmup.', {
        duration: 12_000,
      })
    }
  }, [session.followup_revealed, session.followup_slug])

  const [activeSlug, setActiveSlug] = useState(session.warmup_slug)
  const timeUp = remaining <= 0

  const refresh = () => qc.invalidateQueries({ queryKey: ['mock', session.id] })

  return (
    <div className="flex h-full flex-col">
      <div className="sticky top-14 z-40 mx-3 mt-2 flex items-center gap-4 rounded-xl border border-line bg-bg2/92 px-4 py-2 backdrop-blur-md">
        <AlarmClock size={17} className="text-accent2" />
        <span
          className={cn(
            'font-mono text-xl font-bold tracking-wider',
            remaining < 300 && 'timer-low',
          )}
        >
          {fmtClock(remaining)}
        </span>
        <span className="text-xs font-bold uppercase tracking-widest text-accent2">
          {session.stage}
        </span>
        {session.followup_revealed && session.followup_slug && (
          <div className="flex gap-1 rounded-lg border border-line p-0.5">
            {[session.warmup_slug, session.followup_slug].map((s, i) => (
              <button
                key={s}
                onClick={() => setActiveSlug(s)}
                className={cn(
                  'cursor-pointer rounded-md px-3 py-1 text-xs font-semibold',
                  activeSlug === s ? 'bg-accent/18 text-ink' : 'text-ink-dim',
                )}
              >
                {i === 0 ? 'Warmup' : '🔥 Follow-up'}
              </button>
            ))}
          </div>
        )}
        <div className="ml-auto flex items-center gap-2">
          <Mic size={14} className="text-ink-faint" />
          <span className="hidden text-xs text-ink-faint md:inline">
            communication is scored — keep talking
          </span>
          <FinishButton session={session} label={timeUp ? "Time's up — debrief" : 'End session'} />
          <Button variant="ghost" size="sm" onClick={onAbandon}>
            Abandon
          </Button>
        </div>
      </div>

      {session.stage === 'clarify' && warmup && (
        <ClarifyGate session={session} statement={warmup.statement} title={`${warmup.id}. ${warmup.title}`} onDone={refresh} />
      )}
      {session.stage === 'approach' && <ApproachGate session={session} onDone={refresh} />}
      {session.stage === 'coding' && (
        <div className="min-h-0 flex-1">
          <Workspace
            key={activeSlug}
            slug={activeSlug}
            mock={{ sessionId: session.id, onAccepted: refresh }}
          />
        </div>
      )}
    </div>
  )
}

function ClarifyGate({
  session,
  statement,
  title,
  onDone,
}: {
  session: MockSession
  statement: string
  title: string
  onDone: () => void
}) {
  const [text, setText] = useState('')
  const mut = useMutation({
    mutationFn: () => api.mockClarify(session.id, text),
    onSuccess: onDone,
    onError: (e: Error) => toast.error(e.message, { duration: 6000 }),
  })
  return (
    <main className="mx-auto w-full max-w-3xl px-6 py-8">
      <h2 className="text-xl font-bold">{title}</h2>
      <Card className="my-4 max-h-72 overflow-auto">
        <Markdown>{statement}</Markdown>
      </Card>
      <h3 className="mb-1 mt-6 font-bold">
        Before you code: what would you ask the interviewer?
      </h3>
      <p className="mb-3 text-[13.5px] text-ink-dim">
        Type 2–3 clarifying questions, one per line — input bounds? empty
        input? duplicates? case sensitivity / punctuation? The editor stays
        locked until you do.
      </p>
      <Textarea
        autoFocus
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={'Can the grid be empty?\nAre values bounded to 32-bit ints?\nCan I assume ASCII only?'}
      />
      <Button variant="primary" className="mt-3" onClick={() => mut.mutate()} disabled={mut.isPending}>
        Unlock the approach gate
      </Button>
    </main>
  )
}

function ApproachGate({ session, onDone }: { session: MockSession; onDone: () => void }) {
  const [text, setText] = useState('')
  const [complexity, setComplexity] = useState('')
  const mut = useMutation({
    mutationFn: () => api.mockApproach(session.id, text, complexity),
    onSuccess: onDone,
    onError: (e: Error) => toast.error(e.message, { duration: 6000 }),
  })
  return (
    <main className="mx-auto w-full max-w-3xl px-6 py-8">
      <h2 className="font-bold text-xl">State your approach before touching the editor</h2>
      <p className="mb-3 mt-1 text-[13.5px] text-ink-dim">
        One paragraph, as you'd say it out loud: the pattern you recognized,
        the data structures, the plan. Then commit to a time and space
        complexity — the debrief compares it with reality.
      </p>
      <Textarea
        autoFocus
        rows={6}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="I'll treat the grid as a graph and BFS from every unvisited land cell…"
      />
      <input
        value={complexity}
        onChange={(e) => setComplexity(e.target.value)}
        placeholder="Time O(m·n), space O(m·n) for the queue"
        className="mt-3 w-full rounded-lg border border-line bg-bg2 px-3 py-2 font-mono text-sm text-ink outline-none placeholder:text-ink-faint focus:border-accent"
      />
      <Button variant="primary" className="mt-3" onClick={() => mut.mutate()} disabled={mut.isPending}>
        Unlock the editor
      </Button>
    </main>
  )
}

/* ---------------- finish + debrief ---------------- */

const RUBRIC: [string, string][] = [
  ['clarified', 'I asked real clarifying questions before coding'],
  ['stated_complexity', 'I stated time & space complexity before coding'],
  ['narrated', 'I narrated my thinking while coding'],
  ['clean_code', 'My code is clean: good names, no dead code'],
  ['tested_edges', 'I tested edge cases before declaring done'],
  ['finished_followup', 'I got to (or finished) the follow-up'],
]

function FinishButton({ session, label }: { session: MockSession; label: string }) {
  const [open, setOpen] = useState(false)
  const [checks, setChecks] = useState<Record<string, boolean>>({})
  const qc = useQueryClient()
  const mut = useMutation({
    mutationFn: () => api.mockFinish(session.id, checks),
    onSuccess: () => {
      setOpen(false)
      qc.invalidateQueries({ queryKey: ['mock', session.id] })
    },
    onError: (e: Error) => toast.error(e.message),
  })
  return (
    <>
      <Button size="sm" onClick={() => setOpen(true)}>
        {label}
      </Button>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
          <div className="w-[92%] max-w-lg rounded-2xl border border-line-bright bg-panel p-6">
            <h2 className="mb-1 text-lg font-bold">Self-review before the debrief</h2>
            <p className="mb-4 text-[13.5px] text-ink-dim">
              Honest answers only — this is the rubric the real round grades you on.
            </p>
            {RUBRIC.map(([key, label]) => (
              <label key={key} className="flex cursor-pointer items-center gap-3 py-2 text-[14.5px]">
                <Checkbox
                  checked={!!checks[key]}
                  onCheckedChange={(v) => setChecks((c) => ({ ...c, [key]: v === true }))}
                />
                {label}
              </label>
            ))}
            <div className="mt-4 flex justify-end gap-2">
              <Button variant="ghost" onClick={() => setOpen(false)}>
                Back
              </Button>
              <Button variant="primary" onClick={() => mut.mutate()} disabled={mut.isPending}>
                Finish session
              </Button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

function Debrief({ session, onNew }: { session: MockSession; onNew: () => void }) {
  const rubric: Record<string, boolean> = session.rubric_json
    ? JSON.parse(session.rubric_json)
    : {}
  const { data: subs = [] } = useQuery({
    queryKey: ['mock-subs', session.id],
    queryFn: () => api.submissions(),
    select: (all) => all.filter((s) => s.mock_session_id === session.id),
  })
  const score = RUBRIC.filter(([k]) => rubric[k]).length

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <div className="mb-6 flex items-center gap-3">
        <PartyPopper className="text-accent2" />
        <h1 className="text-2xl font-extrabold">Session debrief</h1>
        <span className="ml-auto text-ink-dim">
          rubric {score}/{RUBRIC.length}
        </span>
      </div>
      <Card className="mb-4">
        <h3 className="mt-0 mb-3 font-bold">Communication rubric</h3>
        {RUBRIC.map(([key, label]) => (
          <div key={key} className="flex items-center gap-2.5 py-1 text-[14.5px]">
            <span className={rubric[key] ? 'text-easy' : 'text-hard'}>
              {rubric[key] ? '✓' : '✗'}
            </span>
            <span className={rubric[key] ? '' : 'text-ink-dim'}>{label}</span>
          </div>
        ))}
      </Card>
      <Card className="mb-4">
        <h3 className="mt-0 mb-3 font-bold">Submissions this session</h3>
        {subs.length === 0 && <p className="text-ink-dim">No submissions were made.</p>}
        {subs.map((s) => (
          <div key={s.id} className="flex items-center gap-3 border-b border-line/55 py-2 last:border-0">
            <span
              className={cn(
                'min-w-[42px] font-bold',
                s.verdict === 'AC' ? 'text-easy' : 'text-hard',
              )}
            >
              {s.verdict}
            </span>
            <span className="text-sm text-ink-dim">
              {s.slug} · {s.passed}/{s.total}
            </span>
            <div className="ml-auto">
              <AIReviewButton submissionId={s.id} />
            </div>
          </div>
        ))}
        {subs.length > 0 && (
          <p className="mt-3 text-[13px] text-ink-faint">
            The AI reviewer unlocks only now that the session is over — same
            rules as the real round.
          </p>
        )}
      </Card>
      <Button variant="primary" onClick={onNew}>
        New mock session
      </Button>
    </main>
  )
}
