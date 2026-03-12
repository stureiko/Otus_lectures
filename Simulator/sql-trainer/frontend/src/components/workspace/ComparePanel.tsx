import type { ValidateResponse } from '../../types'

export function ComparePanel({ result }: { result: ValidateResponse }) {
  if (result.error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-4">
        <p className="text-sm font-semibold text-red-700 mb-1">Ошибка выполнения</p>
        <pre className="text-xs text-red-600 whitespace-pre-wrap font-mono">{result.error}</pre>
      </div>
    )
  }

  return (
    <div
      className={`rounded-lg border p-4 flex flex-col gap-3 ${
        result.is_correct
          ? 'border-emerald-200 bg-emerald-50'
          : 'border-red-200 bg-red-50'
      }`}
    >
      {/* Статус */}
      <div className="flex items-center gap-2">
        <span className="text-xl">{result.is_correct ? '✅' : '❌'}</span>
        <span
          className={`font-semibold ${
            result.is_correct ? 'text-emerald-700' : 'text-red-700'
          }`}
        >
          {result.message}
        </span>
      </div>

      {/* Diff таблица */}
      {!result.is_correct && result.diff.length > 0 && result.student_result && (
        <div className="flex flex-col gap-1">
          <p className="text-xs font-medium text-slate-600">Расхождение с эталоном:</p>
          <div className="overflow-auto rounded border border-slate-200 max-h-40">
            <table className="w-full text-xs border-collapse">
              <thead>
                <tr className="bg-slate-100">
                  <th className="px-2 py-1 text-left text-slate-500 border-b border-slate-200">Статус</th>
                  {result.student_result.columns.map((col) => (
                    <th key={col} className="px-2 py-1 text-left font-mono text-slate-600 border-b border-slate-200">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {result.diff.map((d, i) => (
                  <tr
                    key={i}
                    className={d.status === 'missing' ? 'bg-red-100' : 'bg-yellow-100'}
                  >
                    <td className="px-2 py-1 font-medium">
                      {d.status === 'missing' ? (
                        <span className="text-red-600">− не хватает</span>
                      ) : (
                        <span className="text-yellow-700">+ лишняя</span>
                      )}
                    </td>
                    {d.row.map((v, j) => (
                      <td key={j} className="px-2 py-1 font-mono text-slate-700">
                        {v === null ? <span className="text-slate-400 italic">NULL</span> : String(v)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
