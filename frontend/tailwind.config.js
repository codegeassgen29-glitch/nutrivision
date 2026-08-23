// tailwind.config.js
// ---------------------------------------------------------
// Tailwind CSS works by scanning our files for class names
// like "bg-blue-500" and generating only the CSS actually used.
// The `content` array tells it WHICH files to scan.
// ---------------------------------------------------------
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // scan every JS/TS/JSX/TSX file in src/
  ],
  darkMode: 'class', // we control dark mode by toggling a "dark" class, not just OS preference
   theme: {
    extend: {
      keyframes: {
        blob: {
          '0%, 100%': { transform: 'translate(0px, 0px) scale(1)' },
          '33%': { transform: 'translate(30px, -50px) scale(1.1)' },
          '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
        },
      },
      animation: {
        blob: 'blob 12s infinite ease-in-out',
      },
    },
  },
  plugins: [],
}
