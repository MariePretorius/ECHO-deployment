module.exports = {
  content: ['./src/**/*.{html,ts}'],
  darkMode: 'class', // or 'media'
  theme: {
    extend: {},
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      pink: {
        light: '#F6668F',
        DEFAULT: '#EE0258',
      },
      gray: {
        background: '#191716',
        component: '#252525' ,
        DEFAULT: '#323232',
        light: '#454549',
        verylight: '#D9D9D9',
      }
    }
  },
  variants: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}