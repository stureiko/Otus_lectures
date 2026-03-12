import type { Difficulty } from '../../types'

const DIFFICULTY_STYLES: Record<Difficulty, string> = {
  easy: 'bg-green-100 text-green-800',
  medium: 'bg-yellow-100 text-yellow-800',
  hard: 'bg-red-100 text-red-800',
}

const DIFFICULTY_LABELS: Record<Difficulty, string> = {
  easy: 'Легко',
  medium: 'Средне',
  hard: 'Сложно',
}

export function DifficultyBadge({ difficulty }: { difficulty: Difficulty }) {
  return (
    <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${DIFFICULTY_STYLES[difficulty]}`}>
      {DIFFICULTY_LABELS[difficulty]}
    </span>
  )
}

export function TopicBadge({ topic }: { topic: string }) {
  return (
    <span className="text-xs font-medium px-2 py-0.5 rounded-full bg-blue-100 text-blue-800">
      {topic}
    </span>
  )
}
