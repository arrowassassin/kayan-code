import { useMemo } from 'react'
import CodeMirror, { EditorView } from '@uiw/react-codemirror'
import { python } from '@codemirror/lang-python'
import { oneDark } from '@codemirror/theme-one-dark'

export type EditorMode = 'practice' | 'interview'

/**
 * practice: full CodeMirror basic setup (bracket matching, close brackets…).
 * interview: ALL assists off — no autocomplete, no bracket aids, no
 * highlighting of matches — mirroring CoderPad with assists disabled.
 */
export function CodeEditor({
  value,
  onChange,
  mode,
  readOnly = false,
}: {
  value: string
  onChange: (v: string) => void
  mode: EditorMode
  readOnly?: boolean
}) {
  const basicSetup = useMemo(
    () =>
      mode === 'interview'
        ? {
            lineNumbers: true,
            highlightActiveLine: true,
            highlightActiveLineGutter: true,
            history: true,
            autocompletion: false,
            closeBrackets: false,
            bracketMatching: false,
            indentOnInput: false,
            highlightSelectionMatches: false,
            searchKeymap: false,
            foldGutter: false,
            allowMultipleSelections: false,
            completionKeymap: false,
            closeBracketsKeymap: false,
          }
        : {
            lineNumbers: true,
            highlightActiveLine: true,
            autocompletion: false, // even practice mode: no autocomplete (train for it)
            bracketMatching: true,
            closeBrackets: true,
            indentOnInput: true,
            foldGutter: true,
          },
    [mode],
  )

  return (
    <div className="cm-fill h-full min-h-0">
      <CodeMirror
        value={value}
        onChange={onChange}
        height="100%"
        theme={oneDark}
        readOnly={readOnly}
        basicSetup={basicSetup}
        extensions={[python(), EditorView.lineWrapping]}
      />
    </div>
  )
}
