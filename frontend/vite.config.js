import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    allowedHosts: ['.googleusercontent.com', '.colab.dev', '.codatalab-user-runtimes.internal'],
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8001',
        changeOrigin: true,
      },
    },
    hmr: {
      protocol: 'wss',
      clientPort: 443,
    },
  },
})
