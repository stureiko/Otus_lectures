import Editor from '@monaco-editor/react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { fetchTaskFull, runSandbox } from '../../api/teacher'
import { createTask, updateTask } from '../../api/tasks'
import { Header } from '../../components/layout/Header'
import { SchemaViewer } from '../../components/task/SchemaViewer'
import { MiniSqlResult } from '../../components/workspace/MiniSqlResult'
import { Button } from '../../components/ui/Button'
import { Spinner } from '../../components/ui/Spinner'
import type { Difficulty, ExecuteResponse, TaskCreate } from '../../types'

// ─── утилита для парсинга схемы прямо во фронтенде ────────────────────────────
function parseSchemaPreview(ddl: string) {
  const tables: { name: string; columns: { name: string; type: string }[] }[] = []
  const re = /CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"']?(\w+)[`"']?\s*\(([^;]+)\)/gi
  let m: RegExpExecArray | null
  while ((m = re.exec(ddl)) !== null) {
    const cols = m[2]
      .split(',')
      .map((l) => l.trim())
      .filter((l) => l && !/^(PRIMARY|FOREIGN|UNIQUE|CHECK|CONSTRAINT)/i.test(l))
      .map((l) => {
        const parts = l.split(/\s+/)
        return { name: parts[0]?.replace(/[`"']/g, '') ?? '', type: parts[1]?.replace(/[`"'(),]/g, '') ?? '' }
      })
      .filter((c) => c.name)
    tables.push({ name: m[1], columns: cols })
  }
  return tables
}

// ─── переиспользуемые поля формы ──────────────────────────────────────────────
function Field({ label, required, children }: { label: string; required?: boolean; children: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-sm font-medium text-slate-700">
        {label} {required && <span className="text-red-500">*</span>}
      </label>
      {children}
    </div>
  )
}

function TextInput({ value, onChange, placeholder, required }: {
  value: string; onChange: (v: string) => void; placeholder?: string; required?: boolean
}) {
  return (
    <input
      type="text"
      value={value}
      required={required}
      placeholder={placeholder}
      onChange={(e) => onChange(e.target.value)}
      className="border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  )
}

function TextareaInput({ value, onChange, placeholder, rows = 3 }: {
  value: string; onChange: (v: string) => void; placeholder?: string; rows?: number
}) {
  return (
    <textarea
      value={value}
      rows={rows}
      placeholder={placeholder}
      onChange={(e) => onChange(e.target.value)}
      className="border border-slate-300 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y"
    />
  )
}

function SqlBlock({
  label, value, onChange, height = 140,
  extra,
}: {
  label: string; value: string; onChange: (v: string) => void
  height?: number; extra?: React.ReactNode
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <p className="text-sm font-medium text-slate-700">{label}</p>
      <div className="rounded-lg overflow-hidden border border-slate-300">
        <Editor
          height={`${height}px`}
          language="sql"
          value={value}
          onChange={(v) => onChange(v ?? '')}
          theme="vs"
          options={{
            minimap: { enabled: false },
            fontSize: 13,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            wordWrap: 'on',
            automaticLayout: true,
            tabSize: 2,
          }}
        />
      </div>
      {extra}
    </div>
  )
}

// ─── Блок секций ──────────────────────────────────────────────────────────────
function Section({ title, subtitle, children }: {
  title: string; subtitle?: string; children: React.ReactNode
}) {
  return (
    <section className="bg-white rounded-xl border border-slate-200 p-6 flex flex-col gap-5">
      <div>
        <h2 className="font-semibold text-slate-800">{title}</h2>
        {subtitle && <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>}
      </div>
      {children}
    </section>
  )
}

// ─── Основной компонент ────────────────────────────────────────────────────────
const INITIAL: TaskCreate = {
  title: '',
  description: '',
  difficulty: 'easy',
  topic: 'SELECT',
  order_num: 1,
  reference_sql: '',
  db_schema_sql: '',
  db_seed_sql: '',
  order_matters: false,
  hints: [],
}

const TOPICS = ['SELECT', 'WHERE', 'GROUP BY', 'JOIN', 'Subquery', 'Window', 'CTE', 'Other']

export function TaskFormPage() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { id } = useParams<{ id: string }>()
  const editId = id ? Number(id) : null
  const isEdit = editId !== null

  const [form, setForm] = useState<TaskCreate>(INITIAL)
  const [newHint, setNewHint] = useState('')

  // Результат тестирования SQL
  const [schemaTestRes, setSchemaTestRes] = useState<ExecuteResponse | null>(null)
  const [refTestRes, setRefTestRes] = useState<ExecuteResponse | null>(null)
  const [testingSchema, setTestingSchema] = useState(false)
  const [testingRef, setTestingRef] = useState(false)

  const set = <K extends keyof TaskCreate>(key: K, val: TaskCreate[K]) =>
    setForm((f) => ({ ...f, [key]: val }))

  // Загрузка полных данных задачи для редактирования (teacher-only endpoint)
  const { data: existingTask, isLoading: isLoadingTask } = useQuery({
    queryKey: ['teacher-task', editId],
    queryFn: () => fetchTaskFull(editId!),
    enabled: isEdit,
  })

  // Заполняем форму данными существующей задачи
  useEffect(() => {
    if (existingTask) {
      setForm(existingTask)
    }
  }, [existingTask])

  // Сохранение
  const saveMutation = useMutation({
    mutationFn: (data: TaskCreate) =>
      isEdit ? updateTask(editId!, data) : createTask(data),
    onSuccess: (task) => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      queryClient.invalidateQueries({ queryKey: ['task', editId] })
      navigate(`/tasks/${task.id}`)
    },
  })

  // Тест схемы + seed (SELECT 1 чтобы просто проверить, что DDL корректен)
  const handleTestSchema = async () => {
    setTestingSchema(true)
    setSchemaTestRes(null)
    const res = await runSandbox(form.db_schema_sql, form.db_seed_sql, 'SELECT 1 AS ok', false)
    setSchemaTestRes(res)
    setTestingSchema(false)
  }

  // Тест reference SQL
  const handleTestRef = async () => {
    setTestingRef(true)
    setRefTestRes(null)
    const res = await runSandbox(form.db_schema_sql, form.db_seed_sql, form.reference_sql, false)
    setRefTestRes(res)
    setTestingRef(false)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!form.title || !form.db_schema_sql || !form.db_seed_sql || !form.reference_sql) return
    saveMutation.mutate(form)
  }

  const schemaPreview = parseSchemaPreview(form.db_schema_sql)

  if (isEdit && isLoadingTask) {
    return (
      <div className="min-h-screen flex flex-col bg-slate-100">
        <Header />
        <div className="flex-1 flex items-center justify-center"><Spinner size="lg" /></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-100">
      <Header />

      <main className="max-w-3xl mx-auto w-full px-4 py-8">
        {/* Шапка */}
        <div className="flex items-center gap-3 mb-6">
          <button
            className="text-sm text-blue-600 hover:underline cursor-pointer"
            onClick={() => navigate('/teacher')}
          >
            ← Назад
          </button>
          <h1 className="text-2xl font-bold text-slate-800">
            {isEdit ? 'Редактировать задание' : 'Новое задание'}
          </h1>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-6">

          {/* ── 1. Основная информация ─────────────────────────── */}
          <Section title="Основная информация">
            <Field label="Название" required>
              <TextInput
                value={form.title}
                onChange={(v) => set('title', v)}
                placeholder="Выбрать все заказы пользователя"
                required
              />
            </Field>

            <Field label="Описание задания" required>
              <TextareaInput
                value={form.description}
                onChange={(v) => set('description', v)}
                placeholder={'Напишите запрос, который вернёт **все столбцы** из таблицы `orders`.\nПоддерживается **bold** и `code`.'}
                rows={4}
              />
            </Field>

            <div className="grid grid-cols-2 gap-4">
              <Field label="Сложность">
                <select
                  value={form.difficulty}
                  onChange={(e) => set('difficulty', e.target.value as Difficulty)}
                  className="border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="easy">Легко</option>
                  <option value="medium">Средне</option>
                  <option value="hard">Сложно</option>
                </select>
              </Field>

              <Field label="Тема">
                <select
                  value={form.topic}
                  onChange={(e) => set('topic', e.target.value)}
                  className="border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {TOPICS.map((t) => <option key={t}>{t}</option>)}
                </select>
              </Field>
            </div>

            <div className="grid grid-cols-2 gap-4 items-start">
              <Field label="Порядковый номер">
                <input
                  type="number"
                  min={1}
                  value={form.order_num}
                  onChange={(e) => set('order_num', Number(e.target.value))}
                  className="border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </Field>

              <Field label="Порядок строк">
                <label className="flex items-center gap-2 mt-2 cursor-pointer select-none">
                  <input
                    type="checkbox"
                    checked={form.order_matters}
                    onChange={(e) => set('order_matters', e.target.checked)}
                    className="w-4 h-4 rounded"
                  />
                  <span className="text-sm text-slate-700">Порядок строк важен</span>
                </label>
                <p className="text-xs text-slate-400 mt-0.5">
                  Включите, если в задании требуется ORDER BY
                </p>
              </Field>
            </div>
          </Section>

          {/* ── 2. Подсказки ──────────────────────────────────────── */}
          <Section
            title="Подсказки"
            subtitle="Показываются студенту по запросу. Добавьте 1–3 подсказки."
          >
            {form.hints.length > 0 && (
              <ul className="flex flex-col gap-2">
                {form.hints.map((hint, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-xs text-slate-400 mt-1 shrink-0">#{i + 1}</span>
                    <span className="flex-1 text-sm text-slate-700 bg-yellow-50 border border-yellow-200 rounded px-3 py-1.5">
                      {hint}
                    </span>
                    <button
                      type="button"
                      onClick={() => set('hints', form.hints.filter((_, j) => j !== i))}
                      className="text-red-400 hover:text-red-600 text-lg leading-none shrink-0 cursor-pointer"
                    >
                      ×
                    </button>
                  </li>
                ))}
              </ul>
            )}

            <div className="flex gap-2">
              <input
                type="text"
                value={newHint}
                onChange={(e) => setNewHint(e.target.value)}
                placeholder="Используйте WHERE для фильтрации..."
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault()
                    if (newHint.trim()) { set('hints', [...form.hints, newHint.trim()]); setNewHint('') }
                  }
                }}
                className="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <Button
                type="button"
                variant="ghost"
                onClick={() => { if (newHint.trim()) { set('hints', [...form.hints, newHint.trim()]); setNewHint('') } }}
              >
                + Добавить
              </Button>
            </div>
            <p className="text-xs text-slate-400">Нажмите Enter или кнопку «Добавить»</p>
          </Section>

          {/* ── 3. База данных ────────────────────────────────────── */}
          <Section
            title="База данных задания"
            subtitle="SQL-скрипты для создания изолированной sandbox-базы. Студент работает только с этими данными."
          >
            <SqlBlock
              label="Схема (CREATE TABLE ...)"
              value={form.db_schema_sql}
              onChange={(v) => { set('db_schema_sql', v); setSchemaTestRes(null) }}
              height={160}
            />

            <SqlBlock
              label="Начальные данные (INSERT INTO ...)"
              value={form.db_seed_sql}
              onChange={(v) => { set('db_seed_sql', v); setSchemaTestRes(null) }}
              height={130}
            />

            {/* Кнопка тест схемы */}
            <div className="flex items-center gap-3">
              <Button
                type="button"
                variant="ghost"
                loading={testingSchema}
                disabled={!form.db_schema_sql || !form.db_seed_sql}
                onClick={handleTestSchema}
              >
                ⚡ Проверить схему и данные
              </Button>
              {schemaTestRes?.success && (
                <span className="text-sm text-emerald-600">✅ Схема и данные корректны</span>
              )}
            </div>
            {schemaTestRes && !schemaTestRes.success && <MiniSqlResult res={schemaTestRes} />}

            {/* Превью схемы */}
            {schemaPreview.length > 0 && (
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">
                  Превью схемы
                </p>
                <SchemaViewer schema={schemaPreview} />
              </div>
            )}
          </Section>

          {/* ── 4. Эталонное решение ──────────────────────────────── */}
          <Section
            title="Эталонное решение"
            subtitle="Запрос, с которым будет сравниваться ответ студента. Студент его не видит."
          >
            <SqlBlock
              label="Reference SQL"
              value={form.reference_sql}
              onChange={(v) => { set('reference_sql', v); setRefTestRes(null) }}
              height={140}
            />

            <div className="flex items-center gap-3">
              <Button
                type="button"
                variant="ghost"
                loading={testingRef}
                disabled={!form.db_schema_sql || !form.db_seed_sql || !form.reference_sql}
                onClick={handleTestRef}
              >
                ▶ Выполнить эталонный запрос
              </Button>
              {refTestRes?.success && (
                <span className="text-sm text-emerald-600">
                  ✅ Вернул {refTestRes.result?.row_count} строк
                </span>
              )}
            </div>
            {refTestRes && <MiniSqlResult res={refTestRes} />}
          </Section>

          {/* ── Ошибка сохранения ─────────────────────────────────── */}
          {saveMutation.isError && (
            <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
              Ошибка при сохранении задания. Проверьте все поля.
            </div>
          )}

          {/* ── Кнопки действий ───────────────────────────────────── */}
          <div className="flex items-center gap-3 pb-8">
            <Button
              type="submit"
              variant="success"
              loading={saveMutation.isPending}
              disabled={!form.title || !form.db_schema_sql || !form.db_seed_sql || !form.reference_sql}
              className="px-6"
            >
              {isEdit ? 'Сохранить изменения' : 'Сохранить задание'}
            </Button>
            <Button
              type="button"
              variant="ghost"
              onClick={() => navigate('/teacher')}
            >
              Отмена
            </Button>
            {saveMutation.isPending && (
              <div className="flex items-center gap-2 text-sm text-slate-500">
                <Spinner size="sm" /> Сохраняется...
              </div>
            )}
          </div>
        </form>
      </main>
    </div>
  )
}
