export function Spinner({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizeClass = { sm: 'w-4 h-4', md: 'w-6 h-6', lg: 'w-10 h-10' }[size]
  return (
    <div
      className={`${sizeClass} border-2 border-slate-300 border-t-blue-600 rounded-full animate-spin`}
    />
  )
}
