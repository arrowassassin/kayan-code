import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { toast } from 'sonner'
import { api, type AIReview } from '@/lib/api'
import { Button } from '@/components/ui/button'
import { Spinner } from '@/components/ui/inputs'

export function AIReviewButton({ submissionId }: { submissionId: number }) {
  const [open, setOpen] = useState(false)
  const mut = useMutation({
    mutationFn: () => api.review(submissionId),
    onSuccess: () => setOpen(true),
    onError: (e: Error) => toast.error(e.message, { duration: 8000 }),
  })
  return (
    <>
      <Button
        size="sm"
        variant="outline"
        onClick={() => mut.mutate()}
        disabled={mut.isPending}
        title="Correctness beyond the tests, missed edges, complexity check, the interviewer's next question, and one drill. Cached per submission."
      >
        {mut.isPending ? <Spinner className="size-3.5" /> : '✨'} AI review
      </Button>
      {mut.data && open && (
        <AIReviewModal
          review={mut.data.review}
          model={mut.data.model}
          onClose={() => setOpen(false)}
        />
      )}
    </>
  )
}

export function AIReviewModal({
  review,
  model,
  onClose,
}: {
  review: AIReview
  model: string
  onClose: () => void
}) {
  const sections: [string, React.ReactNode][] = [
    ['Correctness beyond the tests', review.correctness_verdict],
    [
      'Missed edge cases',
      review.missed_edge_cases?.length ? (
        <ul className="ml-4 list-disc">
          {review.missed_edge_cases.map((e, i) => (
            <li key={i}>{e}</li>
          ))}
        </ul>
      ) : (
        'None flagged.'
      ),
    ],
    ['Complexity: claimed vs actual', review.complexity_check],
    [
      'Code cleanliness',
      review.code_cleanliness?.length ? (
        <ul className="ml-4 list-disc">
          {review.code_cleanliness.map((e, i) => (
            <li key={i}>{e}</li>
          ))}
        </ul>
      ) : (
        'Clean.'
      ),
    ],
    ["The follow-up an interviewer would ask", review.interviewer_follow_up],
    ['One concrete drill', review.drill_suggestion],
  ]
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
    >
      <div
        className="max-h-[84vh] w-[92%] max-w-2xl overflow-auto rounded-2xl border border-line-bright bg-panel p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-4 flex items-baseline gap-3">
          <h2 className="text-lg font-bold">✨ AI Review</h2>
          <span className="font-mono text-xs text-ink-faint">{model}</span>
          <button
            onClick={onClose}
            className="ml-auto cursor-pointer text-ink-dim hover:text-ink"
            aria-label="Close"
          >
            ✕
          </button>
        </div>
        <div className="grid gap-3">
          {sections.map(([title, body]) => (
            <div
              key={title as string}
              className="rounded-lg border-l-[3px] border-accent bg-panel2 p-4"
            >
              <h4 className="mb-1.5 text-xs font-bold uppercase tracking-wider text-accent2">
                {title}
              </h4>
              <div className="text-[14px] leading-relaxed">{body}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
