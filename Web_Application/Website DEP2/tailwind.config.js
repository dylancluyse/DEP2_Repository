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
        'blue-de-france': "#3083dc",
        "DonkerBlauw": "#000B4F",
        "ZeeBlauw": "#20368F",
        "lichtblauw": "#829CD0",
        "Grijs": "#EBEBEB",
        "DonkerGrijs": "#6D6D6D",
        "DonkerDonkerGrijs": "323232",
        "viesgroen": "#92B1B6",
        "Granny": "#9ecb88",
        "glauscous": "#6883BA",
      }

    },
  },
  plugins: [
    // ...
    require('@tailwindcss/forms'),
  ],
}