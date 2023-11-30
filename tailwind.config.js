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
        'mainColor': "#ee6c4d",
        'clearMainColor': "#fce1c7",
        'secondayColor': "#354f52",
        'mainBlack': "#2F2F2F"
      }
    },
  },
  plugins: [],
}
