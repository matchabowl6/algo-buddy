import { defineConfig } from 'vite'

export default defineConfig({
    server: {
        proxy: {
            '/api': "localhost:5000"
        }
    }
})
