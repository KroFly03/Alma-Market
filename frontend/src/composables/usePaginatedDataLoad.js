import { useDataLoad } from "@/composables/useDataLoad.js";
import { usePagination } from "@/composables/usePagination.js";

const itemsKey = "results";
const totalPagesKey = "total_pages";

export const usePaginatedDataLoad = (initPage = 1) => {
    const { isLoading, data, loadData } = useDataLoad();
    const { currentPage, totalPages } = usePagination(initPage);

    const loadPaginatedData = async (query) => {
        await loadData(async () => {
            const response = await query();

            data.value = response[itemsKey];
            totalPages.value = response[totalPagesKey];
        });
    };

    return { isLoading, data, currentPage, totalPages, loadPaginatedData };
};
