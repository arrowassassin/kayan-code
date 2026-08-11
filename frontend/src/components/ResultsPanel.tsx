import { useState } from 'react'
import { motion } from 'framer-motion'
import type { CaseResult, JudgeResult } from '@/lib/api'
import { cn, fmtMs } from '@/lib/utils'

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

function J({ v }: { v: unknown }) {
  return (
    <pre className="m-0 whitespace-pre-wrap break-all rounded-lg border border-line bg-bg2 px-3 py-2 font-mono text-[13px]">
      {v === undefined ? '—' : JSON.stringify(v)}
    </pre>
  )
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

export function ResultsPanel({ result }: { result: JudgeResult }) {
  const [sel, setSel] = useState(0)

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
                  <J v={c.output} />
                </Field>
              )}
              {c.expected !== undefined && c.expected !== null && (
                <Field label="Expected">
                  <J v={c.expected} />
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
