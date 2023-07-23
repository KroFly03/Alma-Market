export default {
    mounted(el, binding) {
        const event = (e) => {
            if (el !== e.target && !el.contains(e.target)) {
                binding.value();
            }
        };

        el._outsideClick = event;
        window.addEventListener("click", event);
    },
    onmounted(el) {
        window.removeEventListener("click", el._outsideClick);
    },
};
