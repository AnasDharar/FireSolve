/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.{js,css}",
    "./*/templates/**/*.html",
  ],
  theme: {
    extend: {
      fontFamily: {
        gabarito: ['Gabarito', 'sans-serif'],
        poppins: ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [
    require("daisyui")
  ],
  daisyui: {
    themes: ["dark"],
  },
}