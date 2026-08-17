import { lazy, Suspense } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeHighlight from 'rehype-highlight'

const Mermaid = lazy(() =>
  import('@/components/Mermaid').then((m) => ({ default: m.Mermaid })),
)

// flatten React children to plain text (defensive if a plugin wraps content)
function extractText(node: unknown): string {
  if (node == null) return ''
  if (typeof node === 'string' || typeof node === 'number') return String(node)
  if (Array.isArray(node)) return node.map(extractText).join('')
  if (typeof node === 'object' && 'props' in (node as { props?: unknown })) {
    return extractText(
      (node as { props: { children?: unknown } }).props.children,
    )
  }
  return ''
}

export function Markdown({ children }: { children: string }) {
  return (
    <div className="md">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{
          code({ className, children: kids, ...props }) {
            // mermaid fences: hljs doesn't know the language so children stay
            // a plain string — render the diagram instead of code
            const text = extractText(kids)
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
