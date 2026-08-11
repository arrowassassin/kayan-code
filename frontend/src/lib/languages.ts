import type { Extension } from '@uiw/react-codemirror'
import { python } from '@codemirror/lang-python'
import { java } from '@codemirror/lang-java'
import { cpp } from '@codemirror/lang-cpp'
import { javascript } from '@codemirror/lang-javascript'
import { go } from '@codemirror/lang-go'
import { rust } from '@codemirror/lang-rust'

export interface LanguageDef {
  id: string
  label: string
  extension: () => Extension
  comment: string // line-comment prefix for generated stubs
}

export const LANGUAGES: LanguageDef[] = [
  { id: 'python', label: 'Python 3', extension: python, comment: '#' },
  { id: 'java', label: 'Java', extension: java, comment: '//' },
  { id: 'cpp', label: 'C++', extension: cpp, comment: '//' },
  { id: 'javascript', label: 'JavaScript', extension: () => javascript(), comment: '//' },
  { id: 'typescript', label: 'TypeScript', extension: () => javascript({ typescript: true }), comment: '//' },
  { id: 'go', label: 'Go', extension: go, comment: '//' },
  { id: 'rust', label: 'Rust', extension: rust, comment: '//' },
]

export const langById = (id: string) =>
  LANGUAGES.find((l) => l.id === id) ?? LANGUAGES[0]

/** Non-Python starter: a comment block carrying the Python signature as the
 * contract, since the judge (after AI translation) targets that shape. */
export function starterFor(lang: LanguageDef, pythonStarter: string) {
  if (lang.id === 'python') return pythonStarter
  const c = lang.comment
  const sig = pythonStarter
    .split('\n')
    .filter((l) => l.trim())
    .map((l) => `${c}   ${l}`)
    .join('\n')
  return [
    `${c} Write your solution in ${lang.label}.`,
    `${c} On Run/Submit it is AI-translated to Python and judged — keep the`,
    `${c} same class/method names and parameter order as this contract:`,
    sig,
    '',
    '',
  ].join('\n')
}
