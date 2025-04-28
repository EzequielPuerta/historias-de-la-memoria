import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// https://vite.dev/config/
export default defineConfig({
  plugins: [svelte()],
  base: '/static/',
  build: {
    outDir: '../api/static/',
    assetsDir: '',
    rollupOptions: {
        input: 'src/main.js',
        output: {
            entryFileNames: 'assets/bundle.js',
            chunkFileNames: 'assets/bundle.js',
            assetFileNames: 'assets/bundle.styles.css',
        }
    },
  },
})
