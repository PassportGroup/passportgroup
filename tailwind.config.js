const colors = require('tailwindcss/colors');

module.exports = {
  mode: 'jit',
  purge: [
      './apps/battoh-vue/**/*.js',
      './apps/battoh-vue/**/*.vue',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
      danger: '#f14668',
      info: '#3298dc',
      warning: '#ffdd57',
      theme: {
        1: '#00bfa6',
        2: '#013C4B',
        3: '#fa8f05',
      },
      brand: {
        primary: "#1266F1",
        facebook: "#435F9B",
        twitter: "#55ACEE",
        linkedin: "#007BB5",
        pinterest: "#F93154",
      },
    },
      fontFamily:{
        'lato': ['Lato', 'sans-serif']
      },
      screens: {
         xs: "496px"
      },
    }
  },
  plugins: [],
}




