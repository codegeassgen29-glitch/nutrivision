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
      // We'll add custom colors, fonts, animations here in the UI milestone
    },
  },
  plugins: [],
}
