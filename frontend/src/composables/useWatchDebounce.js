import { watch } from "vue";

export const useWatchDebounce = (watchObj, callback, { delayMs, deep = false }) => {
    let timerId;

    return watch(
        watchObj,
        () => {
            if (timerId) clearTimeout(timerId);
            timerId = setTimeout(callback, delayMs);
        },
        { deep }
    );
};
