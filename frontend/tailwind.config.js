/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#14181f",
        "ink-soft": "#2a2f3a",
        paper: "#f6f3ea",
        "paper-dim": "#ece6d6",
        line: "#d9d2bc",
        moss: {
          DEFAULT: "#2f5d50",
          dark: "#1f3f37",
          light: "#4f8f7d",
        },
        brass: "#b08d57",
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        mono: ["JetBrains Mono", "monospace"],
        body: ["Public Sans", "sans-serif"],
      },
      maxWidth: {
        prose: "68ch",
      },
    },
  },
  plugins: [],
};
