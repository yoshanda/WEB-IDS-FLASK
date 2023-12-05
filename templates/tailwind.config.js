/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['index.html'],
  theme: {
    container: {
      center: true,
      padding: '16px',
    },
    extend: {
      colors: {
        primary: '#265073',
        secondary: '#64748b',
        dark: '#0f172a',
        vintage: '#1e40af',
        warm: '#FAF7F0',
      },
      screens: {
        'xl':'1260px',
      },
    },
  },
  plugins: [],
}