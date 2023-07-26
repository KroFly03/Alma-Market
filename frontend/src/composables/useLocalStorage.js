import { ref, watch } from "vue";

export const useLocalStorage = (localStorageKey, initialValue = null, deep = false) => {
    const value = ref(null);

    const localStorageItem = localStorage.getItem(localStorageKey);
    if (localStorageItem) value.value = JSON.parse(localStorageItem);

    watch(
        value,
        (newValue) => {
            localStorage.setItem(localStorageKey, JSON.stringify(newValue));
        },
        { deep }
    );

    if (!localStorageItem) value.value = initialValue;

    return value;
};
