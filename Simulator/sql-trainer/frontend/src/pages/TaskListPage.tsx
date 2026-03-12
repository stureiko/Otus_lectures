import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { fetchProgress } from '../api/progress'
import { fetchTasks } from '../api/tasks'
import { Header } from '../components/layout/Header'
import { DifficultyBadge, TopicBadge } from '../components/ui/Badge'
import { Spinner } from '../components/ui/Spinner'
import type { ProgressItem, TaskListItem } from '../types'

export function TaskListPage() {
  const navigate = useNavigate()

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: fetchTasks,
  })

  const { data: progress } = useQuery({
    queryKey: ['progress'],
    queryFn: fetchProgress,
  })

  const progressMap = new Map<number, ProgressItem>(
    progress?.map((p) => [p.task_id, p]) ?? []
  )

  const solved = progress?.filter((p) => p.solved).length ?? 0
  const total = tasks?.length ?? 0

  return (
    <div className="min-h-screen flex flex-col bg-slate-100">
      <Header />

      <main className="flex-1 max-w-3xl mx-auto w-full px-4 py-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-slate-800">Задания</h1>
            <p className="text-sm text-slate-500 mt-0.5">
              Решено: <strong>{solved}</strong> из <strong>{total}</strong>
            </p>
          </div>
          {total > 0 && (
            <div className="w-32">
              <div className="h-2 bg-slate-200 rounded-full overflow-hidden">
                <div
                  className="h-full bg-emerald-500 rounded-full transition-all"
                  style={{ width: `${(solved / total) * 100}%` }}
                />
              </div>
              <p className="text-xs text-slate-400 mt-1 text-right">
                {Math.round((solved / total) * 100)}%
              </p>
            </div>
          )}
        </div>

        {isLoading ? (
          <div className="flex justify-center py-16"><Spinner size="lg" /></div>
        ) : (
          <div className="flex flex-col gap-3">
            {tasks?.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                progress={progressMap.get(task.id)}
                onClick={() => navigate(`/tasks/${task.id}`)}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  )
}

function TaskCard({
  task,
  progress,
  onClick,
}: {
  task: TaskListItem
  progress?: ProgressItem
  onClick: () => void
}) {
  return (
    <div
      className="bg-white rounded-xl border border-slate-200 px-5 py-4 flex items-center gap-4 hover:border-blue-400 hover:shadow-sm transition-all cursor-pointer group"
      onClick={onClick}
    >
      {/* Статус */}
      <div className="shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm border-2
        ${progress?.solved ? 'border-emerald-400 bg-emerald-50' : 'border-slate-200 bg-slate-50'}">
        {progress?.solved ? '✅' : <span className="text-slate-400 text-xs">{task.order_num}</span>}
      </div>

      {/* Инфо */}
      <div className="flex-1 min-w-0">
        <p className="font-medium text-slate-800 group-hover:text-blue-600 transition-colors truncate">
          {task.title}
        </p>
        {progress && (
          <p className="text-xs text-slate-400 mt-0.5">
            {progress.solved
              ? `Решено с ${progress.attempts_count} попытки`
              : `Попыток: ${progress.attempts_count}`}
          </p>
        )}
      </div>

      {/* Теги */}
      <div className="flex items-center gap-2 shrink-0">
        <TopicBadge topic={task.topic} />
        <DifficultyBadge difficulty={task.difficulty} />
      </div>

      <span className="text-slate-300 group-hover:text-blue-400 text-lg shrink-0">›</span>
    </div>
  )
}
