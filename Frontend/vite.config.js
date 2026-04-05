import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        cookieDomainRewrite: 'localhost',
      },
      '/accounts': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        cookieDomainRewrite: 'localhost',
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
