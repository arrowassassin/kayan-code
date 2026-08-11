import * as React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const badgeVariants = cva(
  'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold',
  {
    variants: {
      variant: {
        default: 'bg-white/6 text-ink-dim font-medium',
        easy: 'text-easy bg-easy/12',
        medium: 'text-medium bg-medium/12',
        hard: 'text-hard bg-hard/12',
        priority: 'grad-bg text-bg',
        outline: 'border border-line-bright text-ink-dim',
        due: 'text-medium border border-medium/40',
      },
    },
    defaultVariants: { variant: 'default' },
  },
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />
}

export function DifficultyBadge({ difficulty }: { difficulty: string }) {
  const v =
    difficulty === 'Easy' ? 'easy' : difficulty === 'Hard' ? 'hard' : 'medium'
  return <Badge variant={v}>{difficulty}</Badge>
}
