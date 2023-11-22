/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*"],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['"Jost"']
      },
      colors: {
        'mainGrey': "#EAEAEA",
        'mainColor': "#c68143",
        'secondayColor': "#616f67",
        'mainBlack': "#2F2F2F"
      }
    },
  },
  plugins: [],
}
