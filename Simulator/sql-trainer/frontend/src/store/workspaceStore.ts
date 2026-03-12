import { create } from 'zustand'
import type { ExecuteResponse, ValidateResponse } from '../types'

interface WorkspaceState {
  sql: string
  isExecuting: boolean
  isValidating: boolean
  executeResult: ExecuteResponse | null
  validateResult: ValidateResponse | null

  setSql: (sql: string) => void
  setExecuting: (v: boolean) => void
  setValidating: (v: boolean) => void
  setExecuteResult: (r: ExecuteResponse | null) => void
  setValidateResult: (r: ValidateResponse | null) => void
  resetResults: () => void
}

export const useWorkspaceStore = create<WorkspaceState>((set) => ({
  sql: '',
  isExecuting: false,
  isValidating: false,
  executeResult: null,
  validateResult: null,

  setSql: (sql) => set({ sql }),
  setExecuting: (isExecuting) => set({ isExecuting }),
  setValidating: (isValidating) => set({ isValidating }),
  setExecuteResult: (executeResult) => set({ executeResult }),
  setValidateResult: (validateResult) => set({ validateResult }),
  resetResults: () => set({
    executeResult: null,
    validateResult: null,
    isExecuting: false,
    isValidating: false,
  }),
}))
