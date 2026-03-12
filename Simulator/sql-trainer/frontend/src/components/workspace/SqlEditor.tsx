import Editor from '@monaco-editor/react'
import { useWorkspaceStore } from '../../store/workspaceStore'
import { Button } from '../ui/Button'

interface SqlEditorProps {
  onRun: () => void
  onValidate: () => void
}

export function SqlEditor({ onRun, onValidate }: SqlEditorProps) {
  const { sql, setSql, isExecuting, isValidating } = useWorkspaceStore()

  const handleKeyDown = (e: KeyboardEvent) => {
    // Ctrl/Cmd + Enter → Run
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault()
      onRun()
    }
  }

  return (
    <div className="flex flex-col gap-2">
      <div className="rounded-lg overflow-hidden border border-slate-300">
        <Editor
          height="180px"
          language="sql"
          value={sql}
          onChange={(v) => setSql(v ?? '')}
          theme="vs"
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            wordWrap: 'on',
            automaticLayout: true,
            tabSize: 2,
            suggestOnTriggerCharacters: true,
          }}
          onMount={(editor) => {
            editor.onKeyDown((e) => handleKeyDown(e.browserEvent))
          }}
        />
      </div>

      <div className="flex items-center gap-2">
        <Button
          variant="primary"
          onClick={onRun}
          loading={isExecuting}
          disabled={!sql.trim()}
        >
          ▶ Выполнить
        </Button>
        <Button
          variant="success"
          onClick={onValidate}
          loading={isValidating}
          disabled={!sql.trim()}
        >
          ✓ Проверить решение
        </Button>
        <span className="ml-auto text-xs text-slate-400">Ctrl+Enter — выполнить</span>
      </div>
    </div>
  )
}
