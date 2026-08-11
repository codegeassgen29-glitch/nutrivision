// postcss.config.js
// ---------------------------------------------------------
// PostCSS is a tool that transforms CSS with plugins.
// Tailwind itself is a PostCSS plugin - this file is what
// wires Tailwind (and autoprefixer, which adds vendor
// prefixes like -webkit- automatically) into our build.
// ---------------------------------------------------------
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
