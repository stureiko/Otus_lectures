import { useState } from 'react'
import type { TableSchema } from '../../types'

export function SchemaViewer({ schema }: { schema: TableSchema[] }) {
  const [openTables, setOpenTables] = useState<Set<string>>(
    () => new Set(schema.map((t) => t.name))
  )

  const toggle = (name: string) =>
    setOpenTables((prev) => {
      const next = new Set(prev)
      next.has(name) ? next.delete(name) : next.add(name)
      return next
    })

  if (!schema.length) return null

  return (
    <div className="flex flex-col gap-1">
      {schema.map((table) => (
        <div key={table.name} className="border border-slate-200 rounded-lg overflow-hidden">
          <button
            className="w-full flex items-center gap-2 px-3 py-2 bg-slate-50 hover:bg-slate-100 text-left text-sm font-medium text-slate-800 cursor-pointer"
            onClick={() => toggle(table.name)}
          >
            <span className="text-slate-400">{openTables.has(table.name) ? '▾' : '▸'}</span>
            <span className="font-mono">{table.name}</span>
            <span className="ml-auto text-xs text-slate-400">{table.columns.length} col</span>
          </button>
          {openTables.has(table.name) && (
            <div className="bg-white divide-y divide-slate-100">
              {table.columns.map((col) => (
                <div key={col.name} className="flex items-center px-3 py-1.5 gap-2">
                  <span className="text-xs font-mono text-slate-700">{col.name}</span>
                  <span className="ml-auto text-xs text-slate-400 font-mono">{col.type}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
