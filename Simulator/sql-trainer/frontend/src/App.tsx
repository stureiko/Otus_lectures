import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import { LoginPage } from './pages/LoginPage'
import { TaskListPage } from './pages/TaskListPage'
import { WorkspacePage } from './pages/WorkspacePage'
import { TeacherPage } from './pages/teacher/TeacherPage'
import { TaskFormPage } from './pages/teacher/TaskFormPage'
import type { User } from './types'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 30_000 },
  },
})

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { token } = useAuthStore()
  return token ? <>{children}</> : <Navigate to="/login" replace />
}

function TeacherRoute({ children }: { children: React.ReactNode }) {
  const { token, user } = useAuthStore()
  if (!token) return <Navigate to="/login" replace />
  if ((user as User | null)?.role !== 'teacher') return <Navigate to="/tasks" replace />
  return <>{children}</>
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/tasks"
            element={<PrivateRoute><TaskListPage /></PrivateRoute>}
          />
          <Route
            path="/tasks/:id"
            element={<PrivateRoute><WorkspacePage /></PrivateRoute>}
          />
          <Route
            path="/teacher"
            element={<TeacherRoute><TeacherPage /></TeacherRoute>}
          />
          <Route
            path="/teacher/tasks/new"
            element={<TeacherRoute><TaskFormPage /></TeacherRoute>}
          />
          <Route
            path="/teacher/tasks/:id/edit"
            element={<TeacherRoute><TaskFormPage /></TeacherRoute>}
          />
          <Route path="*" element={<Navigate to="/tasks" replace />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  )
}
