import client from './client'
import type { LeaderboardItem, ProgressItem } from '../types'

export const fetchProgress = () =>
  client.get<ProgressItem[]>('/progress').then((r) => r.data)

export const fetchLeaderboard = () =>
  client.get<LeaderboardItem[]>('/progress/leaderboard').then((r) => r.data)
