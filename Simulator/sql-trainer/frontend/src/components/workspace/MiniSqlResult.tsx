import type { ExecuteResponse } from '../../types'
import { ResultTable } from './ResultTable'

export function MiniSqlResult({ res }: { res: ExecuteResponse }) {
  if (!res.success || !res.result) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-3 mt-2">
        <p className="text-xs font-semibold text-red-600 mb-1">Ошибка</p>
        <pre className="text-xs text-red-700 whitespace-pre-wrap font-mono">{res.error}</pre>
      </div>
    )
  }
  return (
    <div className="mt-2">
      <ResultTable result={res.result} />
    </div>
  )
}
