// vite.config.ts
// ---------------------------------------------------------
// This configures Vite, the tool that runs our dev server
// and bundles our code for production.
// ---------------------------------------------------------
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  // This plugin teaches Vite how to handle React's JSX syntax
  // and enables Fast Refresh (instant UI updates without losing state
  // when you save a file during development).
  plugins: [react()],
  server: {
    port: 5173, // the port our dev server runs on
  },
})
