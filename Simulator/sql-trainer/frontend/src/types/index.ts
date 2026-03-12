export type UserRole = 'student' | 'teacher'
export type Difficulty = 'easy' | 'medium' | 'hard'

export interface User {
  id: number
  email: string
  name: string
  role: UserRole
  created_at: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
  user: User
}

// ── Tasks ────────────────────────────────────────────────────────────────────

export interface TableColumn {
  name: string
  type: string
}

export interface TableSchema {
  name: string
  columns: TableColumn[]
}

export interface TaskListItem {
  id: number
  title: string
  difficulty: Difficulty
  topic: string
  order_num: number
}

export interface TaskDetail extends TaskListItem {
  description: string
  hints: string[]
  order_matters: boolean
  schema: TableSchema[]
}

export interface TaskCreate {
  title: string
  description: string
  difficulty: Difficulty
  topic: string
  order_num: number
  reference_sql: string
  db_schema_sql: string
  db_seed_sql: string
  order_matters: boolean
  hints: string[]
}

// ── Execution ────────────────────────────────────────────────────────────────

export interface QueryResult {
  columns: string[]
  rows: unknown[][]
  row_count: number
}

export interface ExecuteResponse {
  success: boolean
  result: QueryResult | null
  error: string | null
}

export interface DiffRow {
  row: unknown[]
  status: 'missing' | 'extra'
}

export interface ValidateResponse {
  is_correct: boolean
  student_result: QueryResult | null
  error: string | null
  diff: DiffRow[]
  message: string
}

// ── Progress ─────────────────────────────────────────────────────────────────

export interface ProgressItem {
  task_id: number
  task_title: string
  solved: boolean
  attempts_count: number
  first_solved_at: string | null
}

export interface LeaderboardItem {
  user_id: number
  user_name: string
  solved_count: number
  total_attempts: number
}
