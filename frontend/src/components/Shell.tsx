import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { Flame, Snowflake } from 'lucide-react'
import { api } from '@/lib/api'
import { cn } from '@/lib/utils'

export function Shell() {
  const navigate = useNavigate()
  const { data: daily } = useQuery({ queryKey: ['daily'], queryFn: api.daily })

  return (
    <div className="flex h-full flex-col">
      <header className="sticky top-0 z-50 flex h-14 shrink-0 items-center gap-7 border-b border-line bg-bg/80 px-5 backdrop-blur-md">
        <Link to="/" className="flex items-center gap-1 text-[19px] font-bold tracking-tight">
          <Snowflake size={20} className="text-accent" />
          <span>
            Kayan<span className="grad-text">Code</span>
          </span>
        </Link>
        <nav className="flex gap-1">
          {[
            { to: '/', label: 'Problems' },
            { to: '/study', label: 'Study' },
            { to: '/mock', label: 'Mock Interview' },
            { to: '/dashboard', label: 'Dashboard' },
          ].map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.to === '/'}
              className={({ isActive }) =>
                cn(
                  'rounded-lg px-3.5 py-1.5 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-accent/14 text-ink'
                    : 'text-ink-dim hover:bg-white/5 hover:text-ink',
                )
              }
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
        <div className="ml-auto flex items-center gap-3">
          {daily && (
            <button
              onClick={() => navigate(`/problems/${daily.slug}`)}
              className="flex cursor-pointer items-center gap-2 rounded-full border border-line px-3.5 py-1.5 text-[13px] text-ink-dim transition-colors hover:border-accent hover:text-ink"
              title={`Daily challenge: ${daily.title}`}
            >
              <Flame
                size={14}
                className={daily.streak > 0 ? 'text-medium' : 'text-ink-faint'}
              />
              {daily.done ? 'Daily ✓' : 'Daily'}
              {daily.streak > 0 && (
                <span className="font-bold text-medium">{daily.streak}</span>
              )}
            </button>
          )}
        </div>
      </header>
      <div className="min-h-0 flex-1">
        <Outlet />
      </div>
    </div>
  )
}
