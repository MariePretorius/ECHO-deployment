module.exports = {
    content: ["./src/**/*.{html,ts}", "./node_modules/flowbite/**/*.js"],
    darkMode: "class", // or 'media'
    theme: {
        extend: {
            fontFamily: {
                'sans': ['Noto Sans', 'sans-serif'] 
            },
            transitionProperty: {
                'mood': 'background-color, color', // Specify which properties to transition
              },
              transitionTimingFunction: {
                'mood': 'ease-in-out',
              },
              transitionDuration: {
                'mood': '1000ms', // Adjust the duration as needed
              },
            colors: {
                'dark-bg': '#191716',
                'light-bg': '#ffffff',
                'dark-text': '#EE0258',
                'light-text': '#EE0258',
                'desktop-bg': '#323232',
                pink: {
                    "white": '#E8D5DA',
                    "verylight": '#FFABC2',
                    "light": '#F6668F',
                    DEFAULT: '#EE0258',
                    "dark": '#C40047'
                },
                gray: {
                    "background": '#191716',
                    "component": '#252525',
                    "dark": '#323232',
                    "light": '#454549',
                    "verylight": '#D9D9D9',
                    "lightcomponent": '#9A9A9E',
                },
                default: {
                    DEFAULT: '#EE0258',
                    "text": '#ffffff',
                    "component": '#252525',
                    "dark": '#C40047',
                    "backgrounddark": '#323232',
                    "background": '#FFE1D2',
                },
                admiration: {
                    DEFAULT: '#FF5308',
                    "text": '#FFD700',
                    "component": '#252525',
                    "dark": '#D44000',
                    "backgrounddark": '#5F3625',
                    "background": '#FFEBCC',
                },
                anger:{
                    DEFAULT: '#A40014',
                    "text": '#FFB9B9',
                    "component": '#221113',
                    "dark": '#890817',
                    "backgrounddark": '#471C21',
                    "background": '#FFCCCC',
                },
                fear:{
                    DEFAULT: '#9A44CE',
                    "text": '#1dff3c',
                    "component": '#C639A2',
                    "dark": '#ff00d8',
                    "backgrounddark": '#462E5E',
                    "background": '#E6E6FA',
                },
                joy:{
                    DEFAULT: '#FFD700',
                    text: '#FFF8DC',
                    component: '#FFA500',
                    dark: '#FF8C00',
                    backgrounddark: '#FFFFE0',
                    background: '#FFFACD',
                },
                amusement: {
                    DEFAULT: '#FF6347',
                    text: '#FFF5EE',
                    component: '#FF7F50',
                    dark: '#CD5C5C',
                    backgrounddark: '#FFE4E1',
                    background: '#FFE4B5',
                },
                annoyance: {
                    DEFAULT: '#FF4500',
                    text: '#FFDAB9',
                    component: '#FF6347',
                    dark: '#CD3700',
                    backgrounddark: '#FFFAF0',
                    background: '#FFEFD5',
                },
                approval: {
                    DEFAULT: '#32CD32',
                    text: '#F0FFF0',
                    component: '#3CB371',
                    dark: '#228B22',
                    backgrounddark: '#E0FFE0',
                    background: '#F5FFF5',
                },
                caring: {
                    DEFAULT: '#FF69B4',
                    text: '#FFF0F5',
                    component: '#FF1493',
                    dark: '#C71585',
                    backgrounddark: '#FFD1DC',
                    background: '#FFB6C1',
                },
                confusion: {
                    DEFAULT: '#8B008B',
                    text: '#E6E6FA',
                    component: '#9932CC',
                    dark: '#4B0082',
                    backgrounddark: '#DDA0DD',
                    background: '#EE82EE',
                },
                curiosity: {
                    DEFAULT: '#FF8C00',
                    text: '#FFF5EE',
                    component: '#FFA500',
                    dark: '#FF7F50',
                    backgrounddark: '#FFD700',
                    background: '#FFEBCD',
                },
                desire: {
                    DEFAULT: '#FF69B4',
                    text: '#FFF0F5',
                    component: '#FF1493',
                    dark: '#C71585',
                    backgrounddark: '#FFE4E1',
                    background: '#FFB6C1',
                },
                disappointment: {
                    DEFAULT: '#708090',
                    text: '#F5F5F5',
                    component: '#778899',
                    dark: '#2F4F4F',
                    backgrounddark: '#DCDCDC',
                    background: '#D3D3D3',
                },
                disapproval: {
                    DEFAULT: '#FF0000',
                    text: '#FFE4E1',
                    component: '#FF6347',
                    dark: '#B22222',
                    backgrounddark: '#FFC0CB',
                    background: '#FFA07A',
                },
                disgust: {
                    DEFAULT: '#556B2F',
                    text: '#F5FFFA',
                    component: '#6B8E23',
                    dark: '#4B5320',
                    backgrounddark: '#8FBC8F',
                    background: '#98FB98',
                },
                embarrassment: {
                    DEFAULT: '#FFB6C1',
                    text: '#FFF0F5',
                    component: '#FF69B4',
                    dark: '#DB7093',
                    backgrounddark: '#FFDAB9',
                    background: '#FFC0CB',
                },
                excitement: {
                    DEFAULT: '#FF4500',
                    text: '#FFD700',
                    component: '#FF6347',
                    dark: '#DC143C',
                    backgrounddark: '#FFA07A',
                    background: '#FFDEAD',
                },
                gratitude: {
                    DEFAULT: '#FFD700',
                    text: '#FFF8DC',
                    component: '#FFA500',
                    dark: '#FF8C00',
                    backgrounddark: '#FFE4B5',
                    background: '#FFFACD',
                },
                grief: {
                    DEFAULT: '#2F4F4F',
                    text: '#F5F5F5',
                    component: '#696969',
                    dark: '#1C1C1C',
                    backgrounddark: '#A9A9A9',
                    background: '#D3D3D3',
                },
                love: {
                    DEFAULT: '#FF1493',
                    text: '#FFE4E1',
                    component: '#FF69B4',
                    dark: '#C71585',
                    backgrounddark: '#FFD1DC',
                    background: '#FFB6C1',
                },
                nervousness: {
                    DEFAULT: '#FF4500',
                    text: '#FFF5EE',
                    component: '#FF6347',
                    dark: '#B22222',
                    backgrounddark: '#FFE4E1',
                    background: '#FFDAB9',
                },
                optimism: {
                    DEFAULT: '#FFD700',
                    text: '#FFF8DC',
                    component: '#FFA500',
                    dark: '#FF8C00',
                    backgrounddark: '#FFFFE0',
                    background: '#FFFACD',
                },
                pride: {
                    DEFAULT: '#8A2BE2',
                    text: '#E6E6FA',
                    component: '#9370DB',
                    dark: '#4B0082',
                    backgrounddark: '#D8BFD8',
                    background: '#E6E6FA',
                },
                realisation: {
                    DEFAULT: '#00CED1',
                    text: '#E0FFFF',
                    component: '#20B2AA',
                    dark: '#008B8B',
                    backgrounddark: '#AFEEEE',
                    background: '#E0FFFF',
                },
                relief: {
                    DEFAULT: '#00FF7F',
                    text: '#F0FFF0',
                    component: '#32CD32',
                    dark: '#228B22',
                    backgrounddark: '#98FB98',
                    background: '#F5FFFA',
                },
                remorse: {
                    DEFAULT: '#8B0000',
                    text: '#FFE4E1',
                    component: '#B22222',
                    dark: '#800000',
                    backgrounddark: '#FA8072',
                    background: '#FF6347',
                },
                sadness: {
                    DEFAULT: '#4682B4',
                    text: '#F0F8FF',
                    component: '#87CEEB',
                    dark: '#4169E1',
                    backgrounddark: '#B0E0E6',
                    background: '#ADD8E6',
                },
                surprise: {
                    DEFAULT: '#FF4500',
                    text: '#FFD700',
                    component: '#FF6347',
                    dark: '#FF0000',
                    backgrounddark: '#FFDAB9',
                    background: '#FFE4B5',
                },                
            }
        },
    },
    variants: {
        extend: {
            backgroundColor: ['dark', 'hover', 'focus', 'transition'],
            textColor: ['dark', 'hover', 'focus', 'transition'],
        },
    },
    plugins: [require("@tailwindcss/forms"), require("flowbite/plugin")],
};