import { useRoute, useRouter } from "vue-router";
import { computed, customRef, nextTick } from "vue";

const _cache = new WeakMap();

export const useRouteQuery = (name, defaultValue, format = (val) => val) => {
    const route = useRoute();
    const router = useRouter();

    if (!_cache.has(route)) _cache.set(route, new Map());

    const query = _cache.get(route);

    query.set(name, route.query[name]);

    return computed({
        get: () => {
            return format(route.query[name]) || defaultValue;
        },
        set: (value) => {
            query.set(name, value === defaultValue || value === null ? undefined : value);

            nextTick(() => {
                router.push({
                    query: { ...route.query, ...Object.fromEntries(query.entries()) },
                });
            });
        },
    });
};
