import { lazy, Suspense } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const Mermaid = lazy(() =>
  import('@/components/Mermaid').then((m) => ({ default: m.Mermaid })),
)

export function Markdown({ children }: { children: string }) {
  return (
    <div className="md">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code({ className, children: kids, ...props }) {
            const text = String(kids ?? '')
            if (className?.includes('language-mermaid')) {
              return (
                <Suspense
                  fallback={<pre className="text-ink-faint">rendering diagram…</pre>}
                >
                  <Mermaid chart={text} />
                </Suspense>
              )
            }
            return (
              <code className={className} {...props}>
                {kids}
              </code>
            )
          },
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  )
}
