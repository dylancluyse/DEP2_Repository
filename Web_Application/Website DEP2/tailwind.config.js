module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'oxford-blue': '#09306F',
        'lighter-oxford': "#0B3D8E",
      }
    },
  },
  plugins: [
    // ...
    require('@tailwindcss/forms'),
  ],
}