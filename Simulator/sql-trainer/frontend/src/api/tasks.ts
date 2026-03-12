import client from './client'
import type { TaskCreate, TaskDetail, TaskListItem } from '../types'

export const fetchTasks = () =>
  client.get<TaskListItem[]>('/tasks').then((r) => r.data)

export const fetchTask = (id: number) =>
  client.get<TaskDetail>(`/tasks/${id}`).then((r) => r.data)

export const createTask = (data: TaskCreate) =>
  client.post<TaskDetail>('/tasks', data).then((r) => r.data)

export const updateTask = (id: number, data: TaskCreate) =>
  client.put<TaskDetail>(`/tasks/${id}`, data).then((r) => r.data)

export const deleteTask = (id: number) =>
  client.delete(`/tasks/${id}`)
