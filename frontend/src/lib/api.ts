// Typed API client for the FastAPI backend.

export type Verdict = 'AC' | 'WA' | 'TLE' | 'RE'

export interface ProblemSummary {
  slug: string
  id: number
  title: string
  difficulty: 'Easy' | 'Medium' | 'Hard'
  topics: string[]
  snowflake_priority: 1 | 2 | 3
  follow_up_of?: string | null
  follow_up?: string | null
  solved: boolean
  attempted: boolean
  attempts: number
  last_submitted_at: string | null
  solve_seconds: number | null
  due_for_review: boolean
}

export interface TestCase {
  input: unknown[]
  expected?: unknown
}

export interface ProblemDetail extends ProblemSummary {
  statement: string
  starter: string
  visible_tests: TestCase[]
  hidden_count: number
  hints: string[]
  judge: { mode: string; entry: string }
}

export interface CaseResult {
  verdict: Verdict
  time_ms: number
  output: unknown
  expected: unknown
  stdout: string
  error: string | null
  hidden?: boolean
  input?: unknown[]
}

export interface JudgeResult {
  status: 'ok' | 'error'
  error?: string
  cases?: CaseResult[]
  passed?: number
  total?: number
  verdict?: Verdict
  runtime_ms?: number
  submission_id?: number
  transpiled_code?: string
}

export interface SubmissionRow {
  id: number
  slug: string
  verdict: Verdict
  passed: number
  total: number
  runtime_ms: number
  mode: string
  language: string
  mock_session_id: string | null
  created_at: string
  has_review: boolean
}

export interface MockSession {
  id: string
  warmup_slug: string
  followup_slug?: string
  stage: 'clarify' | 'approach' | 'coding' | 'done'
  clarify_text: string | null
  approach_text: string | null
  complexity_text: string | null
  followup_revealed: number
  started_at: string
  ends_at: string
  finished_at: string | null
  rubric_json: string | null
  remaining_seconds: number
}

export interface AIReview {
  correctness_verdict: string
  missed_edge_cases: string[]
  complexity_check: string
  code_cleanliness: string[]
  interviewer_follow_up: string
  drill_suggestion: string
}

export interface Stats {
  total_problems: number
  solved: number
  attempted: number
  submissions: number
  topics: Record<string, { total: number; solved: number; attempted: number }>
  review_queue: { slug: string; due_at: string; last_result: string }[]
  activity: Record<string, number>
  solve_times: { slug: string; seconds: number }[]
  median_solve_seconds: number | null
}

export interface Daily {
  date: string
  slug: string
  title: string
  difficulty: string
  done: boolean
  streak: number
}

class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      detail = body.detail ?? detail
    } catch {
      /* not json */
    }
    throw new ApiError(res.status, detail)
  }
  return res.json()
}

export const api = {
  problems: () => request<ProblemSummary[]>('/api/problems'),
  problem: (slug: string) => request<ProblemDetail>(`/api/problems/${slug}`),
  starter: (slug: string, language: string) =>
    request<{ language: string; starter: string }>(
      `/api/problems/${slug}/starter?language=${language}`,
    ),
  editorial: (slug: string) =>
    request<{ editorial: string }>(`/api/problems/${slug}/editorial`),
  run: (slug: string, code: string, cases?: TestCase[], language = 'python') =>
    request<JudgeResult>('/api/run', {
      method: 'POST',
      body: JSON.stringify({ slug, code, cases, language }),
    }),
  submit: (
    slug: string,
    code: string,
    mode = 'practice',
    mock_session_id?: string,
    language = 'python',
    elapsed_s?: number,
  ) =>
    request<JudgeResult>('/api/submit', {
      method: 'POST',
      body: JSON.stringify({
        slug,
        code,
        mode,
        mock_session_id,
        language,
        elapsed_s,
      }),
    }),
  submissions: (slug?: string) =>
    request<SubmissionRow[]>(`/api/submissions${slug ? `?slug=${slug}` : ''}`),
  submission: (id: number) =>
    request<SubmissionRow & { code: string; result: JudgeResult }>(
      `/api/submissions/${id}`,
    ),
  mockStart: (slug?: string) =>
    request<MockSession>('/api/mock/start', {
      method: 'POST',
      body: JSON.stringify({ slug }),
    }),
  mock: (id: string) => request<MockSession>(`/api/mock/${id}`),
  mockClarify: (id: string, text: string) =>
    request<MockSession>(`/api/mock/${id}/clarify`, {
      method: 'POST',
      body: JSON.stringify({ text }),
    }),
  mockApproach: (id: string, text: string, complexity: string) =>
    request<MockSession>(`/api/mock/${id}/approach`, {
      method: 'POST',
      body: JSON.stringify({ text, complexity }),
    }),
  mockFinish: (id: string, rubric: Record<string, boolean>) =>
    request<MockSession>(`/api/mock/${id}/finish`, {
      method: 'POST',
      body: JSON.stringify({ rubric }),
    }),
  mockHistory: () => request<MockSession[]>('/api/mock'),
  review: (submissionId: number) =>
    request<{ cached: boolean; model: string; review: AIReview }>(
      `/api/review/${submissionId}`,
      { method: 'POST' },
    ),
  stats: () => request<Stats>('/api/stats'),
  daily: () => request<Daily>('/api/daily'),
}
