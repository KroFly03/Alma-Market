export default {
    mounted(el, binding) {
        const observer = new IntersectionObserver((entries) => {
            const isIntersecting = entries.some((entry) => entry.isIntersecting);

            binding.value(isIntersecting);
        }, {});

        observer.observe(el);

        el._observe = observer;
    },
    onmounted(el) {
        el._observe.unobserve(el);
    },
};
