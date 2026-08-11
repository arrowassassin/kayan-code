import * as React from 'react'
import * as CheckboxPrimitive from '@radix-ui/react-checkbox'
import * as ProgressPrimitive from '@radix-ui/react-progress'
import { Check } from 'lucide-react'
import { cn } from '@/lib/utils'

export function Input({
  className,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      className={cn(
        'rounded-lg border border-line bg-bg2 px-3 py-2 text-sm text-ink outline-none transition-colors placeholder:text-ink-faint focus:border-accent',
        className,
      )}
      {...props}
    />
  )
}

export function Textarea({
  className,
  ...props
}: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      className={cn(
        'min-h-[90px] w-full resize-y rounded-lg border border-line bg-bg2 px-3 py-2 text-sm leading-relaxed text-ink outline-none transition-colors placeholder:text-ink-faint focus:border-accent',
        className,
      )}
      {...props}
    />
  )
}

export function Checkbox({
  className,
  ...props
}: React.ComponentProps<typeof CheckboxPrimitive.Root>) {
  return (
    <CheckboxPrimitive.Root
      className={cn(
        'flex size-[18px] shrink-0 cursor-pointer items-center justify-center rounded border border-line-bright bg-bg2 transition-colors data-[state=checked]:grad-bg data-[state=checked]:border-transparent',
        className,
      )}
      {...props}
    >
      <CheckboxPrimitive.Indicator>
        <Check size={13} strokeWidth={3.5} className="text-bg" />
      </CheckboxPrimitive.Indicator>
    </CheckboxPrimitive.Root>
  )
}

export function Progress({
  value,
  className,
}: {
  value: number
  className?: string
}) {
  return (
    <ProgressPrimitive.Root
      className={cn('h-2 overflow-hidden rounded-full bg-bg2', className)}
    >
      <ProgressPrimitive.Indicator
        className="h-full grad-bg rounded-full transition-all duration-500"
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </ProgressPrimitive.Root>
  )
}

export function Spinner({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        'inline-block size-4 animate-spin rounded-full border-2 border-white/25 border-t-accent2 align-[-2px]',
        className,
      )}
    />
  )
}
