import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 rounded-lg font-semibold transition-all cursor-pointer disabled:opacity-45 disabled:cursor-not-allowed focus-visible:outline-2 focus-visible:outline-accent active:translate-y-px whitespace-nowrap',
  {
    variants: {
      variant: {
        default:
          'bg-panel2 text-ink border border-line-bright hover:border-accent',
        primary:
          'grad-bg text-bg border-0 hover:shadow-[0_4px_18px_rgba(109,141,255,.4)]',
        success: 'bg-easy text-[#06130d] border-0 hover:brightness-110',
        destructive: 'bg-hard text-white border-0 hover:brightness-110',
        ghost: 'bg-transparent text-ink-dim hover:text-ink hover:bg-white/5',
        outline: 'bg-transparent border border-line-bright hover:border-accent',
      },
      size: {
        default: 'px-4 py-2 text-sm',
        sm: 'px-3 py-1.5 text-[13px]',
        lg: 'px-6 py-2.5 text-base',
        icon: 'size-9',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  },
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button className={cn(buttonVariants({ variant, size }), className)} {...props} />
  )
}
