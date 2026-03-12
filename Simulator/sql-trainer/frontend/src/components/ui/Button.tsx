import type { ButtonHTMLAttributes } from 'react'
import { Spinner } from './Spinner'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'success' | 'ghost'
  loading?: boolean
}

const VARIANTS = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white',
  success: 'bg-emerald-600 hover:bg-emerald-700 text-white',
  ghost: 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-300',
}

export function Button({
  variant = 'primary',
  loading = false,
  children,
  disabled,
  className = '',
  ...props
}: ButtonProps) {
  return (
    <button
      {...props}
      disabled={disabled || loading}
      className={`
        inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium
        transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed
        ${VARIANTS[variant]} ${className}
      `}
    >
      {loading && <Spinner size="sm" />}
      {children}
    </button>
  )
}
