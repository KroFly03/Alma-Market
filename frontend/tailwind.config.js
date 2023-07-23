/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    theme: {
        colors: {
            primary: "#0288D1",
            white: "white",
            black: "black",
            grey: "grey",
            error: "#C73E1D",
            transparent: "transparent",
        },
        container: {
            center: true,
            padding: "1rem",
        },
        screens: {
            xl: { min: "1400px" },
            lg: { max: "1399px" },
            md: { max: "1024px" },
            sm: { max: "769px" },
        },
    },
    plugins: [],
};
