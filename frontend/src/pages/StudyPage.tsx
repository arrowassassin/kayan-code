import { useEffect } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { BookOpen, ChevronRight, Clock } from 'lucide-react'
import { api } from '@/lib/api'
import { cn } from '@/lib/utils'
import { Markdown } from '@/components/Markdown'
import { Spinner } from '@/components/ui/inputs'

export function StudyPage() {
  const { '*': path = '' } = useParams()
  const navigate = useNavigate()
  const { data: sections = [], isLoading } = useQuery({
    queryKey: ['study'],
    queryFn: api.studyIndex,
  })

  // default to the first chapter
  useEffect(() => {
    if (!path && sections.length && sections[0].chapters.length) {
      navigate(`/study/${sections[0].chapters[0].path}`, { replace: true })
    }
  }, [path, sections, navigate])

  const flat = sections.flatMap((s) => s.chapters)
  const idx = flat.findIndex((c) => c.path === path)
  const prev = idx > 0 ? flat[idx - 1] : null
  const next = idx >= 0 && idx < flat.length - 1 ? flat[idx + 1] : null

  const { data: chapter, isLoading: chapterLoading } = useQuery({
    queryKey: ['study-chapter', path],
    queryFn: () => api.studyChapter(path),
    enabled: !!path,
  })

  if (isLoading)
    return (
      <div className="flex h-64 items-center justify-center text-ink-dim">
        <Spinner className="mr-2" /> Loading curriculum…
      </div>
    )

  if (!sections.length)
    return (
      <main className="mx-auto max-w-2xl p-10 text-center text-ink-dim">
        <BookOpen className="mx-auto mb-3" />
        No study content yet — add .mdx files under <code>study/</code>.
      </main>
    )

  return (
    <div className="mx-auto flex h-[calc(100vh-56px)] max-w-[1500px]">
      {/* sidebar */}
      <aside className="w-72 shrink-0 overflow-y-auto border-r border-line p-4">
        {sections.map((s) => (
          <div key={s.section} className="mb-5">
            <div className="mb-1.5 px-2 text-[11px] font-bold uppercase tracking-widest text-ink-faint">
              {s.section}
            </div>
            {s.chapters.map((c) => (
              <Link
                key={c.path}
                to={`/study/${c.path}`}
                className={cn(
                  'flex items-center gap-2 rounded-lg px-2.5 py-1.5 text-[13.5px] transition-colors',
                  c.path === path
                    ? 'bg-accent/14 font-semibold text-ink'
                    : 'text-ink-dim hover:bg-white/4 hover:text-ink',
                )}
              >
                <span className="truncate">{c.title}</span>
                {c.minutes && (
                  <span className="ml-auto flex shrink-0 items-center gap-1 text-[11px] text-ink-faint">
                    <Clock size={11} />
                    {c.minutes}m
                  </span>
                )}
              </Link>
            ))}
          </div>
        ))}
      </aside>

      {/* content */}
      <article className="min-w-0 flex-1 overflow-y-auto px-8 py-6 lg:px-14">
        {chapterLoading && (
          <div className="flex h-40 items-center justify-center text-ink-dim">
            <Spinner className="mr-2" /> Loading chapter…
          </div>
        )}
        {chapter && (
          <>
            <div className="mx-auto max-w-3xl">
              <Markdown>{chapter.content}</Markdown>
            </div>
            <nav className="mx-auto mt-10 flex max-w-3xl items-center justify-between border-t border-line pt-5">
              {prev ? (
                <Link
                  to={`/study/${prev.path}`}
                  className="text-sm text-ink-dim hover:text-accent"
                >
                  ← {prev.title}
                </Link>
              ) : (
                <span />
              )}
              {next && (
                <Link
                  to={`/study/${next.path}`}
                  className="flex items-center gap-1 text-sm font-semibold text-accent hover:underline"
                >
                  {next.title} <ChevronRight size={15} />
                </Link>
              )}
            </nav>
          </>
        )}
      </article>
    </div>
  )
}
