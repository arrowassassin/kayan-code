import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { CheckCircle2, Circle, CircleDot, Search, Star } from 'lucide-react'
import { api, type ProblemSummary } from '@/lib/api'
import { cn } from '@/lib/utils'
import { Badge, DifficultyBadge } from '@/components/ui/badge'
import { Input } from '@/components/ui/inputs'
import { Progress } from '@/components/ui/inputs'

const DIFFS = ['Easy', 'Medium', 'Hard'] as const
const STATUS = ['Unsolved', 'Solved', 'Due'] as const

function Chip({
  on,
  onClick,
  children,
}: {
  on: boolean
  onClick: () => void
  children: React.ReactNode
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        'cursor-pointer select-none rounded-full border px-3.5 py-1 text-[13px] transition-all',
        on
          ? 'grad-bg border-transparent font-semibold text-bg'
          : 'border-line bg-panel text-ink-dim hover:border-line-bright hover:text-ink',
      )}
    >
      {children}
    </button>
  )
}

export function ProblemsPage() {
  const navigate = useNavigate()
  const { data: problems = [], isLoading } = useQuery({
    queryKey: ['problems'],
    queryFn: api.problems,
  })
  const [q, setQ] = useState('')
  const [topic, setTopic] = useState<string | null>(null)
  const [diff, setDiff] = useState<string | null>(null)
  const [status, setStatus] = useState<string | null>(null)
  const [prioOnly, setPrioOnly] = useState(false)

  const topics = useMemo(
    () => [...new Set(problems.flatMap((p) => p.topics))].sort(),
    [problems],
  )

  const filtered = useMemo(
    () =>
      problems.filter((p) => {
        if (q && !`${p.id} ${p.title}`.toLowerCase().includes(q.toLowerCase()))
          return false
        if (topic && !p.topics.includes(topic)) return false
        if (diff && p.difficulty !== diff) return false
        if (status === 'Solved' && !p.solved) return false
        if (status === 'Unsolved' && p.solved) return false
        if (status === 'Due' && !p.due_for_review) return false
        if (prioOnly && p.snowflake_priority !== 1) return false
        return true
      }),
    [problems, q, topic, diff, status, prioOnly],
  )

  const solved = problems.filter((p) => p.solved).length

  return (
    <main className="mx-auto max-w-6xl p-6">
      <div className="mb-4 flex flex-wrap items-center gap-4">
        <h1 className="mr-auto text-2xl font-bold">Problems</h1>
        <div className="flex w-56 flex-col gap-1">
          <div className="flex justify-between text-[12.5px] text-ink-dim">
            <span>
              {solved} / {problems.length} solved
            </span>
            <span>{problems.length ? Math.round((100 * solved) / problems.length) : 0}%</span>
          </div>
          <Progress value={problems.length ? (100 * solved) / problems.length : 0} />
        </div>
      </div>

      <div className="mb-3 flex flex-wrap items-center gap-2">
        <div className="relative">
          <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-faint" />
          <Input
            placeholder="Search…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            className="w-52 pl-9"
          />
        </div>
        {DIFFS.map((d) => (
          <Chip key={d} on={diff === d} onClick={() => setDiff(diff === d ? null : d)}>
            {d}
          </Chip>
        ))}
        <span className="mx-1 h-5 w-px bg-line" />
        {STATUS.map((s) => (
          <Chip key={s} on={status === s} onClick={() => setStatus(status === s ? null : s)}>
            {s}
          </Chip>
        ))}
        <span className="mx-1 h-5 w-px bg-line" />
        <Chip on={prioOnly} onClick={() => setPrioOnly(!prioOnly)}>
          ★ Snowflake-reported
        </Chip>
      </div>
      <div className="mb-4 flex flex-wrap gap-2">
        {topics.map((t) => (
          <Chip key={t} on={topic === t} onClick={() => setTopic(topic === t ? null : t)}>
            {t}
          </Chip>
        ))}
      </div>

      <div className="overflow-hidden rounded-xl border border-line bg-panel">
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-line text-left text-xs uppercase tracking-wider text-ink-faint">
              <th className="w-10 px-4 py-2.5" />
              <th className="px-3 py-2.5">Title</th>
              <th className="px-3 py-2.5">Difficulty</th>
              <th className="px-3 py-2.5">Topics</th>
              <th className="px-3 py-2.5 text-right">Priority</th>
            </tr>
          </thead>
          <tbody>
            {isLoading && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-ink-dim">
                  Loading bank…
                </td>
              </tr>
            )}
            {!isLoading && filtered.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-8 text-center text-ink-dim">
                  Nothing matches those filters.
                </td>
              </tr>
            )}
            {filtered.map((p) => (
              <Row key={p.slug} p={p} onClick={() => navigate(`/problems/${p.slug}`)} />
            ))}
          </tbody>
        </table>
      </div>
    </main>
  )
}

function Row({ p, onClick }: { p: ProblemSummary; onClick: () => void }) {
  return (
    <tr
      onClick={onClick}
      className="cursor-pointer border-b border-line/55 transition-colors last:border-0 hover:bg-accent/6"
    >
      <td className="px-4 py-2.5">
        {p.solved ? (
          <CheckCircle2 size={17} className="text-easy" />
        ) : p.attempted ? (
          <CircleDot size={17} className="text-medium" />
        ) : (
          <Circle size={17} className="text-ink-faint" />
        )}
      </td>
      <td className="px-3 py-2.5">
        <span className="font-semibold">
          {p.id}. {p.title}
        </span>
        {p.due_for_review && (
          <Badge variant="due" className="ml-2 text-[11px]">
            due for review
          </Badge>
        )}
      </td>
      <td className="px-3 py-2.5">
        <DifficultyBadge difficulty={p.difficulty} />
      </td>
      <td className="px-3 py-2.5">
        <div className="flex flex-wrap gap-1.5">
          {p.topics.map((t) => (
            <Badge key={t}>{t}</Badge>
          ))}
        </div>
      </td>
      <td className="px-3 py-2.5 text-right">
        {p.snowflake_priority === 1 ? (
          <Star size={15} className="ml-auto fill-medium text-medium" />
        ) : p.snowflake_priority === 2 ? (
          <Star size={15} className="ml-auto text-ink-dim" />
        ) : null}
      </td>
    </tr>
  )
}
