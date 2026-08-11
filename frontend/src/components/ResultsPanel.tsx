import { useState } from 'react'
import { motion } from 'framer-motion'
import type { CaseResult, JudgeResult } from '@/lib/api'
import { cn, fmtMs } from '@/lib/utils'
import { AIReviewButton } from '@/components/AIReview'

const verdictLabel: Record<string, string> = {
  AC: 'Accepted',
  WA: 'Wrong Answer',
  TLE: 'Time Limit Exceeded',
  RE: 'Runtime Error',
}

const verdictColor: Record<string, string> = {
  AC: 'text-easy',
  WA: 'text-hard',
  RE: 'text-hard',
  TLE: 'text-medium',
}

/** first index where two JSON strings diverge, for highlighting mismatches */
function firstDiff(a: string, b: string) {
  const n = Math.min(a.length, b.length)
  for (let i = 0; i < n; i++) if (a[i] !== b[i]) return i
  return a.length === b.length ? -1 : n
}

function J({ v, diffAt }: { v: unknown; diffAt?: number }) {
  const s = v === undefined ? '—' : JSON.stringify(v)
  return (
    <pre className="m-0 whitespace-pre-wrap break-all rounded-lg border border-line bg-bg2 px-3 py-2 font-mono text-[13px]">
      {diffAt !== undefined && diffAt >= 0 && diffAt < s.length ? (
        <>
          {s.slice(0, diffAt)}
          <mark className="rounded bg-hard/40 text-ink">{s.slice(diffAt, diffAt + 1)}</mark>
          {s.slice(diffAt + 1)}
        </>
      ) : (
        s
      )}
    </pre>
  )
}

function pyRepr(v: unknown): string {
  if (v === null) return 'None'
  if (v === true) return 'True'
  if (v === false) return 'False'
  if (Array.isArray(v)) return '[' + v.map(pyRepr).join(', ') + ']'
  if (typeof v === 'string') return JSON.stringify(v)
  if (typeof v === 'object')
    return (
      '{' +
      Object.entries(v as object)
        .map(([k, val]) => `${JSON.stringify(k)}: ${pyRepr(val)}`)
        .join(', ') +
      '}'
    )
  return String(v)
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="mb-2.5">
      <div className="mb-1 text-[11.5px] font-semibold uppercase tracking-wider text-ink-faint">
        {label}
      </div>
      {children}
    </div>
  )
}

export function ResultsPanel({
  result,
  entry,
}: {
  result: JudgeResult
  entry?: string
}) {
  const [sel, setSel] = useState(0)
  const [copied, setCopied] = useState(false)

  if (result.status === 'error') {
    return (
      <div className="p-4">
        <div className="mb-2 text-lg font-extrabold text-hard">Error</div>
        <pre className="whitespace-pre-wrap rounded-lg border border-hard/35 bg-hard/8 p-3 font-mono text-[12.5px] text-[#ffb4b4]">
          {result.error}
        </pre>
      </div>
    )
  }

  const cases = result.cases ?? []
  const transpiled = result.transpiled_code
  const firstFail = cases.findIndex((c) => c.verdict !== 'AC')
  const selIdx = Math.min(sel, cases.length - 1)
  const c: CaseResult | undefined = cases[selIdx]

  return (
    <div className="p-4">
      {result.verdict && (
        <motion.div
          initial={{ scale: 0.96, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="mb-3 flex items-baseline gap-3.5"
        >
          <span className={cn('text-xl font-extrabold', verdictColor[result.verdict])}>
            {verdictLabel[result.verdict]}
          </span>
          <span className="text-[13px] text-ink-dim">
            {result.passed}/{result.total} cases · {fmtMs(result.runtime_ms)} total
          </span>
          {result.submission_id != null && (
            <span className="ml-auto">
              <AIReviewButton submissionId={result.submission_id} />
            </span>
          )}
        </motion.div>
      )}
      <div className="mb-3 flex flex-wrap gap-1.5">
        {cases.map((cs, i) => (
          <button
            key={i}
            onClick={() => setSel(i)}
            className={cn(
              'cursor-pointer rounded-lg border border-line bg-panel2 px-3 py-1 text-[12.5px] font-semibold transition-colors',
              cs.verdict === 'AC' ? 'text-easy' : 'text-hard',
              i === selIdx && 'border-accent',
              i === firstFail && cs.verdict !== 'AC' && 'ring-1 ring-hard/50',
            )}
          >
            {cs.hidden ? `Hidden ${i + 1}` : `Case ${i + 1}`}{' '}
            {cs.verdict === 'AC' ? '✓' : '✗'}
          </button>
        ))}
      </div>
      {transpiled && (
        <details className="mb-3 rounded-lg border border-line bg-bg2">
          <summary className="cursor-pointer px-3 py-2 text-[13px] font-semibold text-accent2">
            AI-translated Python (what the judge actually ran)
          </summary>
          <pre className="m-0 max-h-56 overflow-auto whitespace-pre-wrap border-t border-line px-3 py-2 font-mono text-[12.5px]">
            {transpiled}
          </pre>
        </details>
      )}
      {c && (
        <div>
          <div className="mb-2 text-[13px] text-ink-dim">
            <span className={cn('font-bold', verdictColor[c.verdict])}>
              {verdictLabel[c.verdict]}
            </span>{' '}
            · {fmtMs(c.time_ms)}
          </div>
          {c.input !== undefined && (
            <Field label="Input">
              <J v={c.input} />
              {entry && Array.isArray(c.input) && (
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(
                      `Solution().${entry}(${(c.input as unknown[]).map(pyRepr).join(', ')})`,
                    )
                    setCopied(true)
                    setTimeout(() => setCopied(false), 1500)
                  }}
                  className="mt-1 cursor-pointer text-xs text-accent2 hover:underline"
                >
                  {copied ? 'Copied ✓' : 'Copy repro call'}
                </button>
              )}
            </Field>
          )}
          {c.hidden && c.input === undefined ? (
            <div className="text-[13px] text-ink-faint">
              Hidden test case — verdict and runtime only.
            </div>
          ) : (
            <>
              {c.verdict !== 'RE' && (
                <Field label="Your output">
                  <J
                    v={c.output}
                    diffAt={
                      c.verdict === 'WA' && c.expected !== undefined
                        ? firstDiff(JSON.stringify(c.output), JSON.stringify(c.expected))
                        : undefined
                    }
                  />
                </Field>
              )}
              {c.expected !== undefined && c.expected !== null && (
                <Field label="Expected">
                  <J
                    v={c.expected}
                    diffAt={
                      c.verdict === 'WA'
                        ? firstDiff(JSON.stringify(c.expected), JSON.stringify(c.output))
                        : undefined
                    }
                  />
                </Field>
              )}
            </>
          )}
          {c.stdout && (
            <Field label="Stdout">
              <pre className="m-0 whitespace-pre-wrap rounded-lg border border-line bg-bg2 px-3 py-2 font-mono text-[12.5px] text-ink-dim">
                {c.stdout}
              </pre>
            </Field>
          )}
          {c.error && (
            <Field label="Error">
              <pre className="m-0 whitespace-pre-wrap rounded-lg border border-hard/35 bg-hard/8 px-3 py-2 font-mono text-[12.5px] text-[#ffb4b4]">
                {c.error}
              </pre>
            </Field>
          )}
        </div>
      )}
    </div>
  )
}
