import resolveConfig from "tailwindcss/resolveConfig.js";
import tailwindConfig from "tailwind.config.js";
import { computed, ref } from "vue";

const screenWidth = ref(window.innerWidth);

window.addEventListener("resize", () => {
    screenWidth.value = window.innerWidth;
});

export const useScreen = () => {
    const tailwindTheme = resolveConfig(tailwindConfig).theme;

    const breakpoints = tailwindTheme.screens;

    const currentBreakpoint = computed(() => {
        let breakpoint = Object.keys(breakpoints)[0];

        for (const key in breakpoints) {
            const breakpointMaxWidth = parseInt(breakpoints[key].max) || Number.MAX_VALUE;

            if (
                screenWidth.value < (parseInt(breakpoints[breakpoint].max) || Number.MAX_VALUE) &&
                breakpointMaxWidth > screenWidth.value
            ) {
                breakpoint = key;
            }
        }

        return breakpoint;
    });

    const isMobile = computed(() => currentBreakpoint.value === "sm");

    return { breakpoints, currentBreakpoint, isMobile };
};
