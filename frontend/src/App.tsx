import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'sonner'
import { Shell } from '@/components/Shell'
import { ProblemsPage } from '@/pages/ProblemsPage'
import { ProblemPage } from '@/pages/Workspace'
import { MockPage } from '@/pages/MockPage'
import { DashboardPage } from '@/pages/DashboardPage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { staleTime: 10_000, retry: 1, refetchOnWindowFocus: false },
  },
})

const router = createBrowserRouter([
  {
    element: <Shell />,
    children: [
      { path: '/', element: <ProblemsPage /> },
      { path: '/problems/:slug', element: <ProblemPage /> },
      { path: '/mock', element: <MockPage /> },
      { path: '/dashboard', element: <DashboardPage /> },
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
