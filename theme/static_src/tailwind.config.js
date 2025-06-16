module.exports = {
  content: [
    "../templates/**/*.html",
    "../../**/templates/**/*.html",
    "../templates/**/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
}
// This file is used to configure Tailwind CSS for the theme.
// It specifies the paths to the HTML files that Tailwind should scan for class names.