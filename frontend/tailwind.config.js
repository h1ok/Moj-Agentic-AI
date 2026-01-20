/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: "#0B1F42",
        secondary: "#0D2042",
        "navy-dark": "#0B1F43",
        "navy-medium": "#0D2042",
        "navy-light": "#1B3A6D",
        "background-light": "#F6F6F7",
        "background-dark": "#0B1F43",
        "sidebar-light": "#FFFFFF",
        "sidebar-dark": "#0D2042",
        "card-light": "#FFFFFF",
        "card-dark": "#1B3A6D",
        "border-light": "#D9D9D9",
        "border-dark": "#1B3A6D",
        "text-primary-light": "#0B1F43",
        "text-primary-dark": "#F6F6F7",
        "text-secondary-light": "#6B7280",
        "text-secondary-dark": "#AEAFAD",
        "accent-light": "#E1E1E1",
        "accent-dark": "#D9D9D9",
      },
      fontFamily: {
        display: ["Inter", "sans-serif"],
        mono: ["Fira Code", "monospace"],
      },
    },
  },
  plugins: [],
}
