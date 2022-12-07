module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'oxford-blue': '#3083dc',
        'lighter-oxford': "#3083dc",
        'light-yellow': "#f8ffe5",
        'blue-de-france': "#3083dc"
      }
    },
  },
  plugins: [
    // ...
    require('@tailwindcss/forms'),
  ],
}