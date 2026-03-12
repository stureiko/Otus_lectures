import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { deleteTask, fetchTasks } from '../../api/tasks'
import { Header } from '../../components/layout/Header'
import { DifficultyBadge, TopicBadge } from '../../components/ui/Badge'
import { Button } from '../../components/ui/Button'
import { Spinner } from '../../components/ui/Spinner'

export function TeacherPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: fetchTasks,
  })

  const deleteMutation = useMutation({
    mutationFn: deleteTask,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['tasks'] }),
  })

  const handleDelete = (id: number, title: string) => {
    if (!confirm(`Удалить задание «${title}»? Это действие нельзя отменить.`)) return
    deleteMutation.mutate(id)
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-100">
      <Header />

      <main className="max-w-4xl mx-auto w-full px-4 py-8 flex flex-col gap-6">
        {/* Заголовок */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-slate-800">Управление заданиями</h1>
            <p className="text-sm text-slate-500 mt-0.5">
              Всего заданий: <strong>{tasks?.length ?? 0}</strong>
            </p>
          </div>
          <Button onClick={() => navigate('/teacher/tasks/new')}>
            + Создать задание
          </Button>
        </div>

        {/* Список */}
        {isLoading ? (
          <div className="flex justify-center py-16"><Spinner size="lg" /></div>
        ) : (
          <div className="flex flex-col gap-3">
            {tasks?.map((task) => (
              <div
                key={task.id}
                className="bg-white rounded-xl border border-slate-200 px-5 py-4 flex items-center gap-4"
              >
                <span className="text-slate-400 text-sm w-6 shrink-0 text-center">
                  {task.order_num}
                </span>

                <div className="flex-1 min-w-0">
                  <p className="font-medium text-slate-800 truncate">{task.title}</p>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <TopicBadge topic={task.topic} />
                  <DifficultyBadge difficulty={task.difficulty} />
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <Button
                    variant="ghost"
                    onClick={() => navigate(`/tasks/${task.id}`)}
                    className="text-xs"
                  >
                    Просмотр
                  </Button>
                  <Button
                    variant="ghost"
                    onClick={() => navigate(`/teacher/tasks/${task.id}/edit`)}
                    className="text-xs"
                  >
                    Редактировать
                  </Button>
                  <button
                    onClick={() => handleDelete(task.id, task.title)}
                    disabled={deleteMutation.isPending}
                    className="text-xs px-3 py-1.5 rounded-lg text-red-600 hover:bg-red-50 border border-red-200 transition-colors cursor-pointer disabled:opacity-50"
                  >
                    Удалить
                  </button>
                </div>
              </div>
            ))}

            {tasks?.length === 0 && (
              <div className="text-center py-16 text-slate-400">
                <p className="text-lg mb-2">Заданий пока нет</p>
                <Button onClick={() => navigate('/teacher/tasks/new')}>
                  Создать первое задание
                </Button>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
