import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table'
import { useMemo } from 'react'
import type { QueryResult } from '../../types'

export function ResultTable({ result }: { result: QueryResult }) {
  const columnHelper = createColumnHelper<Record<string, unknown>>()

  const columns = useMemo(
    () =>
      result.columns.map((col) =>
        columnHelper.accessor(col, {
          header: col,
          cell: (info) => {
            const v = info.getValue()
            if (v === null || v === undefined)
              return <span className="text-slate-400 italic">NULL</span>
            return String(v)
          },
        })
      ),
    [result.columns]
  )

  const data = useMemo(
    () =>
      result.rows.map((row) =>
        Object.fromEntries(result.columns.map((col, i) => [col, row[i]]))
      ),
    [result.rows, result.columns]
  )

  const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() })

  return (
    <div className="flex flex-col gap-1">
      <div className="text-xs text-slate-500">
        Строк: <strong>{result.row_count}</strong>
      </div>
      <div className="overflow-auto rounded-lg border border-slate-200 max-h-64">
        <table className="w-full text-sm border-collapse">
          <thead>
            {table.getHeaderGroups().map((hg) => (
              <tr key={hg.id} className="bg-slate-100 sticky top-0">
                {hg.headers.map((header) => (
                  <th
                    key={header.id}
                    className="text-left px-3 py-2 text-xs font-semibold text-slate-600 border-b border-slate-200 whitespace-nowrap"
                  >
                    {flexRender(header.column.columnDef.header, header.getContext())}
                  </th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row, i) => (
              <tr
                key={row.id}
                className={i % 2 === 0 ? 'bg-white' : 'bg-slate-50'}
              >
                {row.getVisibleCells().map((cell) => (
                  <td
                    key={cell.id}
                    className="px-3 py-1.5 text-slate-700 border-b border-slate-100 font-mono text-xs whitespace-nowrap"
                  >
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {result.rows.length === 0 && (
          <div className="text-center py-6 text-sm text-slate-400">Запрос выполнен, результат пустой</div>
        )}
      </div>
    </div>
  )
}
