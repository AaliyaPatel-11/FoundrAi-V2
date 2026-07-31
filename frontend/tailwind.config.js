/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        founder: {
          50: '#f4f7fb',
          100: '#e8eff7',
          200: '#cbddec',
          300: '#a3c2dd',
          400: '#75a0cb',
          500: '#5382b6',
          600: '#406898',
          700: '#34547c',
          800: '#2d4767',
          900: '#293d56',
          950: '#0f172a', // deep slate/dark mode base
        },
        accent: {
          teal: '#0ea5e9', // vivid startup cyan
          violet: '#8b5cf6', // premium co-founder violet
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
