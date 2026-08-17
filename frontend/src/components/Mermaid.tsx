import { useEffect, useId, useRef, useState } from 'react'
import mermaid from 'mermaid'

mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  darkMode: true,
  themeVariables: {
    background: '#151a26',
    primaryColor: '#1a2030',
    primaryTextColor: '#e6e9f0',
    primaryBorderColor: '#33405c',
    lineColor: '#6d8dff',
    secondaryColor: '#11151f',
    tertiaryColor: '#1a2030',
    fontFamily: 'ui-sans-serif, system-ui, sans-serif',
    fontSize: '14px',
  },
})

export function Mermaid({ chart }: { chart: string }) {
  const id = useId().replace(/[^a-zA-Z0-9]/g, '')
  const ref = useRef<HTMLDivElement>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    setError(null)
    mermaid
      .render(`mmd-${id}`, chart)
      .then(({ svg }) => {
        if (!cancelled && ref.current) ref.current.innerHTML = svg
      })
      .catch((e: Error) => {
        if (!cancelled) setError(e.message)
      })
    return () => {
      cancelled = true
    }
  }, [chart, id])

  if (error)
    return (
      <pre className="overflow-x-auto rounded-lg border border-hard/35 bg-hard/8 p-3 font-mono text-xs text-[#ffb4b4]">
        mermaid error: {error}\n{chart}
      </pre>
    )
  return (
    <div
      ref={ref}
      className="my-4 flex justify-center overflow-x-auto rounded-xl border border-line bg-bg2 p-4 [&_svg]:max-w-full"
    />
  )
}
