import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { executeSQL, validateSQL } from '../api/execute'
import { fetchTask } from '../api/tasks'
import { Header } from '../components/layout/Header'
import { SchemaViewer } from '../components/task/SchemaViewer'
import { TaskDescription } from '../components/task/TaskDescription'
import { ComparePanel } from '../components/workspace/ComparePanel'
import { ErrorPanel } from '../components/workspace/ErrorPanel'
import { ResultTable } from '../components/workspace/ResultTable'
import { SqlEditor } from '../components/workspace/SqlEditor'
import { useWorkspaceStore } from '../store/workspaceStore'
import { DifficultyBadge } from '../components/ui/Badge'
import { Spinner } from '../components/ui/Spinner'

export function WorkspacePage() {
  const { id } = useParams<{ id: string }>()
  const taskId = Number(id)
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const {
    sql, resetResults,
    setExecuting, setValidating,
    setExecuteResult, setValidateResult,
    executeResult, validateResult,
    isExecuting, isValidating,
  } = useWorkspaceStore()

  const { data: task, isLoading } = useQuery({
    queryKey: ['task', taskId],
    queryFn: () => fetchTask(taskId),
    enabled: !!taskId,
  })

  // Сбрасываем результаты при переходе между задачами
  useEffect(() => { resetResults() }, [taskId])

  const handleRun = async () => {
    setExecuteResult(null)
    setValidateResult(null)
    setExecuting(true)
    try {
      const result = await executeSQL(taskId, sql)
      setExecuteResult(result)
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })
        ?.response?.data?.detail ?? 'Ошибка соединения с сервером'
      setExecuteResult({ success: false, result: null, error: msg })
    } finally {
      setExecuting(false)
    }
  }

  const handleValidate = async () => {
    setExecuteResult(null)
    setValidateResult(null)
    setValidating(true)
    try {
      const result = await validateSQL(taskId, sql)
      setValidateResult(result)
      if (result.is_correct) {
        queryClient.invalidateQueries({ queryKey: ['progress'] })
      }
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })
        ?.response?.data?.detail ?? 'Ошибка соединения с сервером'
      setValidateResult({
        is_correct: false,
        student_result: null,
        error: msg,
        diff: [],
        message: 'Не удалось выполнить проверку.',
      })
    } finally {
      setValidating(false)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen flex flex-col bg-slate-100">
        <Header />
        <div className="flex-1 flex items-center justify-center"><Spinner size="lg" /></div>
      </div>
    )
  }

  if (!task) return null

  return (
    <div className="min-h-screen flex flex-col bg-slate-100">
      <Header />

      <div className="flex-1 flex overflow-hidden" style={{ height: 'calc(100vh - 56px)' }}>
        {/* ── Sidebar ─────────────────────────────────────────── */}
        <aside className="w-80 shrink-0 bg-white border-r border-slate-200 flex flex-col overflow-hidden">
          {/* Навигация */}
          <div className="px-4 py-3 border-b border-slate-100 flex items-center gap-2">
            <button
              className="text-sm text-blue-600 hover:underline cursor-pointer"
              onClick={() => navigate('/tasks')}
            >
              ← Задания
            </button>
          </div>

          {/* Скроллируемая область */}
          <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-5">
            {/* Заголовок задачи */}
            <div>
              <div className="flex items-center gap-2 mb-2">
                <DifficultyBadge difficulty={task.difficulty} />
              </div>
              <h2 className="font-bold text-slate-800 leading-snug">{task.title}</h2>
            </div>

            {/* Описание */}
            <div>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">Задание</p>
              <TaskDescription task={task} />
            </div>

            {/* Схема */}
            {task.schema.length > 0 && (
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">
                  Схема базы данных
                </p>
                <SchemaViewer schema={task.schema} />
              </div>
            )}
          </div>
        </aside>

        {/* ── Main area ───────────────────────────────────────── */}
        <main className="flex-1 flex flex-col overflow-hidden p-5 gap-4">
          {/* Редактор */}
          <div className="bg-white rounded-xl border border-slate-200 p-4">
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-3">
              SQL-редактор
            </p>
            <SqlEditor onRun={handleRun} onValidate={handleValidate} />
          </div>

          {/* Результаты */}
          <div className="flex-1 overflow-y-auto flex flex-col gap-4">
            {/* Результат выполнения */}
            {(isExecuting || executeResult) && (
              <div className="bg-white rounded-xl border border-slate-200 p-4">
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-3">
                  Результат
                </p>
                {isExecuting ? (
                  <div className="flex items-center gap-2 text-sm text-slate-500">
                    <Spinner size="sm" /> Выполняется...
                  </div>
                ) : executeResult?.success && executeResult.result ? (
                  <ResultTable result={executeResult.result} />
                ) : (
                  <ErrorPanel message={executeResult?.error ?? 'Неизвестная ошибка'} />
                )}
              </div>
            )}

            {/* Результат проверки */}
            {(isValidating || validateResult) && (
              <div className="bg-white rounded-xl border border-slate-200 p-4">
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-3">
                  Проверка решения
                </p>
                {isValidating ? (
                  <div className="flex items-center gap-2 text-sm text-slate-500">
                    <Spinner size="sm" /> Проверяется...
                  </div>
                ) : validateResult ? (
                  <div className="flex flex-col gap-3">
                    <ComparePanel result={validateResult} />
                    {validateResult.student_result && !validateResult.error && (
                      <ResultTable result={validateResult.student_result} />
                    )}
                  </div>
                ) : null}
              </div>
            )}

            {/* Начальное состояние */}
            {!isExecuting && !executeResult && !isValidating && !validateResult && (
              <div className="flex-1 flex items-center justify-center text-slate-400 text-sm">
                Напишите SQL-запрос и нажмите «Выполнить» или «Проверить решение»
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  )
}
