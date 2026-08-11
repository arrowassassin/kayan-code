import { lazy, Suspense } from 'react'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'sonner'
import { Shell } from '@/components/Shell'
import { Spinner } from '@/components/ui/inputs'

const ProblemsPage = lazy(() =>
  import('@/pages/ProblemsPage').then((m) => ({ default: m.ProblemsPage })),
)
const ProblemPage = lazy(() =>
  import('@/pages/Workspace').then((m) => ({ default: m.ProblemPage })),
)
const MockPage = lazy(() =>
  import('@/pages/MockPage').then((m) => ({ default: m.MockPage })),
)
const DashboardPage = lazy(() =>
  import('@/pages/DashboardPage').then((m) => ({ default: m.DashboardPage })),
)

function Loading() {
  return (
    <div className="flex h-[70vh] items-center justify-center text-ink-dim">
      <Spinner className="mr-2" /> Loading…
    </div>
  )
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 10_000, retry: 1, refetchOnWindowFocus: false },
  },
})

function withSuspense(node: React.ReactNode) {
  return <Suspense fallback={<Loading />}>{node}</Suspense>
}

const router = createBrowserRouter([
  {
    element: <Shell />,
    children: [
      { path: '/', element: withSuspense(<ProblemsPage />) },
      { path: '/problems/:slug', element: withSuspense(<ProblemPage />) },
      { path: '/mock', element: withSuspense(<MockPage />) },
      { path: '/dashboard', element: withSuspense(<DashboardPage />) },
    ],
  },
])

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <Toaster
        theme="dark"
        position="bottom-right"
        toastOptions={{
          style: {
            background: '#1a2030',
            border: '1px solid #33405c',
            color: '#e6e9f0',
          },
        }}
      />
    </QueryClientProvider>
  )
}
