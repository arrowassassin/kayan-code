import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { api } from '@/lib/api'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress, Spinner } from '@/components/ui/inputs'

export function DashboardPage() {
  const { data: stats } = useQuery({ queryKey: ['stats'], queryFn: api.stats })
  const { data: daily } = useQuery({ queryKey: ['daily'], queryFn: api.daily })

  const activityData = useMemo(() => {
    if (!stats) return []
    const days: { day: string; count: number }[] = []
    for (let i = 29; i >= 0; i--) {
      const d = new Date(Date.now() - i * 86400_000)
      const key = d.toISOString().slice(0, 10)
      days.push({ day: key.slice(5), count: stats.activity[key] ?? 0 })
    }
    return days
  }, [stats])

  if (!stats)
    return (
      <div className="flex h-64 items-center justify-center text-ink-dim">
        <Spinner className="mr-2" /> Loading stats…
      </div>
    )

  const topicRows = Object.entries(stats.topics).sort(
    (a, b) => b[1].solved / b[1].total - a[1].solved / a[1].total,
  )

  return (
    <main className="mx-auto max-w-6xl p-6">
      <h1 className="mb-5 text-2xl font-bold">Dashboard</h1>

      <div className="mb-5 grid grid-cols-2 gap-3.5 md:grid-cols-4">
        {[
          [stats.solved, 'problems solved'],
          [stats.attempted, 'attempted'],
          [
            stats.median_solve_seconds != null
              ? `${Math.floor(stats.median_solve_seconds / 60)}m`
              : '—',
            'median solve (25m target)',
          ],
          [daily?.streak ?? 0, 'day streak 🔥'],
        ].map(([v, label]) => (
          <Card key={label as string}>
            <div className="grad-text text-[32px] font-extrabold">{v}</div>
            <div className="text-[13px] text-ink-dim">{label}</div>
          </Card>
        ))}
      </div>

      <div className="grid gap-3.5 lg:grid-cols-2">
        <Card>
          <h3 className="mt-0 mb-4 font-bold">Per-topic mastery</h3>
          {topicRows.map(([topic, t]) => (
            <div key={topic} className="grid grid-cols-[170px_1fr_70px] items-center gap-3 py-1.5">
              <span className="truncate text-[13.5px] text-ink-dim">{topic}</span>
              <Progress value={(100 * t.solved) / t.total} />
              <span className="text-right font-mono text-[12.5px] text-ink-faint">
                {t.solved}/{t.total}
              </span>
            </div>
          ))}
        </Card>

        <div className="flex flex-col gap-3.5">
          <Card>
            <h3 className="mt-0 mb-2 font-bold">Last 30 days</h3>
            <div className="h-40">
              <ResponsiveContainer>
                <BarChart data={activityData} margin={{ top: 4, right: 4, left: -26, bottom: 0 }}>
                  <CartesianGrid stroke="#232b3d" vertical={false} />
                  <XAxis
                    dataKey="day"
                    tick={{ fill: '#626c80', fontSize: 10 }}
                    interval={5}
                    axisLine={false}
                    tickLine={false}
                  />
                  <YAxis
                    tick={{ fill: '#626c80', fontSize: 10 }}
                    allowDecimals={false}
                    axisLine={false}
                    tickLine={false}
                  />
                  <Tooltip
                    cursor={{ fill: 'rgba(109,141,255,.08)' }}
                    contentStyle={{
                      background: '#1a2030',
                      border: '1px solid #33405c',
                      borderRadius: 8,
                      color: '#e6e9f0',
                    }}
                  />
                  <Bar dataKey="count" fill="#6d8dff" radius={[3, 3, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>

          <Card>
            <h3 className="mt-0 mb-3 font-bold">Spaced-repetition queue</h3>
            {stats.review_queue.length === 0 && (
              <p className="m-0 text-[13.5px] text-ink-dim">
                Queue is empty — fail or shake through a problem and it'll
                resurface at 1 / 3 / 7 days.
              </p>
            )}
            {stats.review_queue.map((r) => {
              const overdue = new Date(r.due_at).getTime() <= Date.now()
              return (
                <Link
                  key={r.slug}
                  to={`/problems/${r.slug}`}
                  className="flex items-center gap-3 border-b border-line/55 py-2 text-sm text-ink last:border-0 hover:text-accent"
                >
                  {r.slug}
                  <Badge variant={overdue ? 'due' : 'default'} className="ml-auto">
                    {overdue ? 'due now' : `due ${r.due_at.slice(0, 10)}`}
                  </Badge>
                </Link>
              )
            })}
          </Card>
        </div>
      </div>
    </main>
  )
}
