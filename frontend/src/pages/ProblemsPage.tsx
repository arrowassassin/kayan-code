import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import {
  ArrowDown,
  ArrowUp,
  CheckCircle2,
  Circle,
  CircleDot,
  Search,
  Star,
} from 'lucide-react'
import { api, type ProblemSummary } from '@/lib/api'
import { cn, fmtClock, timeAgo } from '@/lib/utils'
import { Badge, DifficultyBadge } from '@/components/ui/badge'
import { Input } from '@/components/ui/inputs'
import { Progress } from '@/components/ui/inputs'

type SortKey = 'priority' | 'id' | 'difficulty' | 'attempts' | 'recent' | 'time'
const DIFF_RANK = { Easy: 0, Medium: 1, Hard: 2 } as const

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
  const {
    data: problems = [],
    isLoading,
    isError,
    refetch,
  } = useQuery({
    queryKey: ['problems'],
    queryFn: api.problems,
  })
  const [q, setQ] = useState('')
  const [topic, setTopic] = useState<string | null>(null)
  const [diff, setDiff] = useState<string | null>(null)
  const [status, setStatus] = useState<string | null>(null)
  const [prioOnly, setPrioOnly] = useState(false)
  const [sort, setSort] = useState<{ key: SortKey; dir: 1 | -1 }>({
    key: 'priority',
    dir: 1,
  })

  const topics = useMemo(
    () => [...new Set(problems.flatMap((p) => p.topics))].sort(),
    [problems],
  )

  const toggleSort = (key: SortKey) =>
    setSort((s) => (s.key === key ? { key, dir: (s.dir * -1) as 1 | -1 } : { key, dir: 1 }))

  const filtered = useMemo(() => {
    const rows = problems.filter((p) => {
      if (q && !`${p.id} ${p.title}`.toLowerCase().includes(q.toLowerCase()))
        return false
      if (topic && !p.topics.includes(topic)) return false
      if (diff && p.difficulty !== diff) return false
      if (status === 'Solved' && !p.solved) return false
      if (status === 'Unsolved' && p.solved) return false
      if (status === 'Due' && !p.due_for_review) return false
      if (prioOnly && p.priority !== 1) return false
      return true
    })
    const val = (p: ProblemSummary): number | string => {
      switch (sort.key) {
        case 'id':
          return p.id ?? 0
        case 'difficulty':
          return DIFF_RANK[p.difficulty]
        case 'attempts':
          return p.attempts
        case 'recent':
          return p.last_submitted_at ? Date.parse(p.last_submitted_at) : 0
        case 'time':
          return p.solve_seconds ?? Number.MAX_SAFE_INTEGER
        default:
          return p.priority * 1e7 + (p.id ?? 0)
      }
    }
    return rows.sort((a, b) => {
      const va = val(a)
      const vb = val(b)
      return va < vb ? -sort.dir : va > vb ? sort.dir : 0
    })
  }, [problems, q, topic, diff, status, prioOnly, sort])

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
          ★ Top priority
        </Chip>
      </div>
      <div className="mb-4 flex flex-wrap gap-2">
        {topics.map((t) => (
          <Chip key={t} on={topic === t} onClick={() => setTopic(topic === t ? null : t)}>
            {t}
          </Chip>
        ))}
      </div>

      <div className="overflow-x-auto rounded-xl border border-line bg-panel">
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-line text-left text-xs uppercase tracking-wider text-ink-faint">
              <th className="w-10 px-4 py-2.5" />
              <SortTh label="Title" active={sort} k="id" onSort={toggleSort} />
              <SortTh label="Difficulty" active={sort} k="difficulty" onSort={toggleSort} />
              <th className="px-3 py-2.5">Topics</th>
              <SortTh label="Attempts" active={sort} k="attempts" onSort={toggleSort} className="text-right" />
              <SortTh label="Best time" active={sort} k="time" onSort={toggleSort} className="text-right" />
              <SortTh label="Last tried" active={sort} k="recent" onSort={toggleSort} className="text-right" />
              <SortTh label="Priority" active={sort} k="priority" onSort={toggleSort} className="text-right" />
            </tr>
          </thead>
          <tbody>
            {isLoading && (
              <tr>
                <td colSpan={8} className="px-4 py-10 text-center text-ink-dim">
                  Loading bank…
                </td>
              </tr>
            )}
            {isError && (
              <tr>
                <td colSpan={8} className="px-4 py-10 text-center text-ink-dim">
                  Couldn't reach the backend.{' '}
                  <button
                    onClick={() => refetch()}
                    className="cursor-pointer text-accent hover:underline"
                  >
                    Retry
                  </button>
                </td>
              </tr>
            )}
            {!isLoading && !isError && filtered.length === 0 && (
              <tr>
                <td colSpan={8} className="px-4 py-10 text-center text-ink-dim">
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

function SortTh({
  label,
  k,
  active,
  onSort,
  className,
}: {
  label: string
  k: SortKey
  active: { key: SortKey; dir: 1 | -1 }
  onSort: (k: SortKey) => void
  className?: string
}) {
  const on = active.key === k
  return (
    <th className={cn('px-3 py-2.5', className)}>
      <button
        onClick={() => onSort(k)}
        className={cn(
          'inline-flex cursor-pointer items-center gap-1 uppercase tracking-wider hover:text-ink',
          on ? 'text-ink' : 'text-ink-faint',
          className?.includes('text-right') && 'flex-row-reverse',
        )}
      >
        {label}
        {on &&
          (active.dir === 1 ? <ArrowUp size={12} /> : <ArrowDown size={12} />)}
      </button>
    </th>
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
      <td className="px-3 py-2.5 text-right text-[13px] text-ink-dim tabular-nums">
        {p.attempts || '—'}
      </td>
      <td
        className={cn(
          'px-3 py-2.5 text-right text-[13px] tabular-nums',
          p.solve_seconds != null && p.solve_seconds > 25 * 60
            ? 'text-medium'
            : 'text-ink-dim',
        )}
        title={p.solve_seconds != null ? 'First-AC solve time vs 25-min target' : ''}
      >
        {p.solve_seconds != null ? fmtClock(p.solve_seconds) : '—'}
      </td>
      <td className="px-3 py-2.5 text-right text-xs text-ink-faint">
        {p.last_submitted_at ? timeAgo(p.last_submitted_at) : '—'}
      </td>
      <td className="px-3 py-2.5 text-right">
        {p.priority === 1 ? (
          <Star size={15} className="ml-auto fill-medium text-medium" />
        ) : p.priority === 2 ? (
          <Star size={15} className="ml-auto text-ink-dim" />
        ) : null}
      </td>
    </tr>
  )
}
