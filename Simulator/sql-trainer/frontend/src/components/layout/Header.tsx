import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { Button } from '../ui/Button'

export function Header() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="h-14 bg-white border-b border-slate-200 flex items-center px-6 gap-4 shrink-0">
      <span
        className="font-bold text-blue-600 text-lg cursor-pointer"
        onClick={() => navigate('/tasks')}
      >
        SQL Trainer
      </span>
      <span className="flex-1" />
      {user && (
        <>
          {user.role === 'teacher' && (
            <button
              className="text-sm text-purple-700 bg-purple-50 hover:bg-purple-100 border border-purple-200 px-3 py-1.5 rounded-lg transition-colors cursor-pointer"
              onClick={() => navigate('/teacher')}
            >
              Панель преподавателя
            </button>
          )}
          <span className="text-sm text-slate-600">{user.name}</span>
          <Button variant="ghost" onClick={handleLogout}>
            Выйти
          </Button>
        </>
      )}
    </header>
  )
}
