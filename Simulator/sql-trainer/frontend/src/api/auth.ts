import client from './client'
import type { TokenResponse, User } from '../types'

export const login = (email: string, password: string) =>
  client.post<TokenResponse>('/auth/login', { email, password }).then((r) => r.data)

export const register = (email: string, name: string, password: string) =>
  client.post<User>('/auth/register', { email, name, password }).then((r) => r.data)
