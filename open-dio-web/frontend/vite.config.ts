import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/DIO-v3/',  // GitHub Pages base path for the repository
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})
