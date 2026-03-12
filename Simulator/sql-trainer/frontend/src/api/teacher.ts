import client from './client'
import type { ExecuteResponse, TaskCreate } from '../types'

export const runSandbox = (
  schema_sql: string,
  seed_sql: string,
  sql: string,
  validate_safety = true,
) =>
  client
    .post<ExecuteResponse>('/teacher/sandbox', { schema_sql, seed_sql, sql, validate_safety })
    .then((r) => r.data)

export const fetchTaskFull = (id: number) =>
  client.get<TaskCreate>(`/teacher/tasks/${id}`).then((r) => r.data)
