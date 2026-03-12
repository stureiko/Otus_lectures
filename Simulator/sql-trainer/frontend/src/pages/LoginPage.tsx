import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login, register } from '../api/auth'
import { useAuthStore } from '../store/authStore'
import { Button } from '../components/ui/Button'

type Mode = 'login' | 'register'

export function LoginPage() {
  const [mode, setMode] = useState<Mode>('login')
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const { setAuth } = useAuthStore()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      if (mode === 'login') {
        const data = await login(email, password)
        setAuth(data.user, data.access_token)
      } else {
        await register(email, name, password)
        const data = await login(email, password)
        setAuth(data.user, data.access_token)
      }
      navigate('/tasks')
    } catch (err: unknown) {
      const msg =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        'Произошла ошибка. Проверьте данные.'
      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-sm">
        <h1 className="text-2xl font-bold text-slate-800 mb-1">SQL Trainer</h1>
        <p className="text-sm text-slate-500 mb-6">
          {mode === 'login' ? 'Войдите в аккаунт' : 'Создайте аккаунт'}
        </p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {mode === 'register' && (
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Имя</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Иван Иванов"
              />
            </div>
          )}
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Email</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Пароль</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="••••••••"
            />
          </div>

          {error && (
            <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
              {error}
            </p>
          )}

          <Button type="submit" loading={loading} className="w-full justify-center">
            {mode === 'login' ? 'Войти' : 'Зарегистрироваться'}
          </Button>
        </form>

        <p className="mt-4 text-sm text-center text-slate-500">
          {mode === 'login' ? 'Нет аккаунта?' : 'Уже есть аккаунт?'}{' '}
          <button
            className="text-blue-600 hover:underline cursor-pointer"
            onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError('') }}
          >
            {mode === 'login' ? 'Зарегистрироваться' : 'Войти'}
          </button>
        </p>

        <div className="mt-4 pt-4 border-t border-slate-100 text-xs text-slate-400">
          <p>Демо-аккаунт преподавателя:</p>
          <p>teacher@example.com / teacher123</p>
        </div>
      </div>
    </div>
  )
}
