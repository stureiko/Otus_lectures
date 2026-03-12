import { useState } from 'react'
import type { TaskDetail } from '../../types'
import { DifficultyBadge, TopicBadge } from '../ui/Badge'

export function TaskDescription({ task }: { task: TaskDetail }) {
  const [hintsOpen, setHintsOpen] = useState(false)

  return (
    <div className="flex flex-col gap-3">
      <div className="flex items-center gap-2 flex-wrap">
        <DifficultyBadge difficulty={task.difficulty} />
        <TopicBadge topic={task.topic} />
      </div>

      <div
        className="text-sm text-slate-700 leading-relaxed prose prose-sm max-w-none"
        dangerouslySetInnerHTML={{ __html: formatDescription(task.description) }}
      />

      {task.hints.length > 0 && (
        <div>
          <button
            className="text-xs text-blue-600 hover:underline cursor-pointer"
            onClick={() => setHintsOpen((v) => !v)}
          >
            {hintsOpen ? 'Скрыть подсказки' : `Подсказки (${task.hints.length})`}
          </button>
          {hintsOpen && (
            <ul className="mt-2 space-y-1">
              {task.hints.map((hint, i) => (
                <li key={i} className="text-xs text-slate-600 bg-yellow-50 border border-yellow-200 rounded px-3 py-1.5">
                  💡 {hint}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}

// Минимальный markdown: **bold** → <strong>, `code` → <code>
function formatDescription(text: string): string {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.+?)`/g, '<code class="bg-slate-100 px-1 rounded text-xs font-mono">$1</code>')
    .replace(/\n/g, '<br/>')
}
