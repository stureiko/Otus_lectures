export function ErrorPanel({ message }: { message: string }) {
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-3">
      <p className="text-xs font-semibold text-red-600 mb-1">Ошибка SQL</p>
      <pre className="text-xs text-red-700 whitespace-pre-wrap font-mono">{message}</pre>
    </div>
  )
}
