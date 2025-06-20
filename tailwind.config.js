/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.{js,css}",
    "./*/templates/**/*.html",
  ],
  theme: {
    extend: {
      gabarito : ['Gabarito', 'sans-serif'],
    },
  },
  plugins: [
    require("daisyui")
  ],
  daisyui: {
    themes: ["dark"],
  },
}