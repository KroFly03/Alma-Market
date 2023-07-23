import { ref, watch } from "vue";

export const useLocalStorage = (localStorageKey, initialValue = null) => {
    const value = ref(null);

    const localStorageItem = localStorage.getItem(localStorageKey);
    if (localStorageItem) value.value = JSON.parse(localStorageItem);

    watch(
        () => value,
        (newValue) => {
            if (newValue.value === null || newValue.value === undefined)
                localStorage.removeItem(localStorageKey);
            else localStorage.setItem(localStorageKey, JSON.stringify(newValue.value));
        },
        { deep: true }
    );

    if (!localStorageItem) value.value = initialValue;

    return value;
};
