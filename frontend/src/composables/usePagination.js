import { ref } from "vue";

export const usePagination = ({ page = 1 }) => {
    const currentPage = ref(page);
    const totalPages = ref(page);

    return { currentPage, totalPages };
};
