import client from './client'
import type { ExecuteResponse, ValidateResponse } from '../types'

export const executeSQL = (task_id: number, sql: string) =>
  client.post<ExecuteResponse>('/execute', { task_id, sql }).then((r) => r.data)

export const validateSQL = (task_id: number, sql: string) =>
  client.post<ValidateResponse>('/validate', { task_id, sql }).then((r) => r.data)
