import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'node:path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  server: {
    proxy: { '/api': 'http://localhost:8000' },
  },
  build: {
    outDir: 'dist',
    chunkSizeWarningLimit: 900,
    rollupOptions: {
      output: {
        manualChunks(id: string) {
          if (id.includes('codemirror') || id.includes('@lezer')) return 'codemirror'
          if (id.includes('recharts') || id.includes('d3-')) return 'charts'
          if (id.includes('react-markdown') || id.includes('remark') || id.includes('micromark'))
            return 'markdown'
        },
      },
    },
  },
})
