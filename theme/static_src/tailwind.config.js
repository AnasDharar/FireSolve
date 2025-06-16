module.exports = {
  content: [
    "../templates/**/*.html",
    "../../**/templates/**/*.html",
    "../templates/**/*.html",
  ],
  safelist: [
    'mt-4', 'my-4', 'mb-4', 'ml-4', 'mr-4',
    'pt-4', 'pb-4', 'pl-4', 'pr-4', 'p-4',
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
}
// This file is used to configure Tailwind CSS for the theme.
// It specifies the paths to the HTML files that Tailwind should scan for class names.