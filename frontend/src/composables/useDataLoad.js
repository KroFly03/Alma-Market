import { ref } from "vue";

export const useDataLoad = () => {
    const isLoading = ref(false);
    const data = ref([]);

    const loadData = async (callback) => {
        isLoading.value = true;
        try {
            await callback(data);
        } finally {
            isLoading.value = false;
        }
    };

    return { isLoading, data, loadData };
};
