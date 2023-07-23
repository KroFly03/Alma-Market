<template>
    <div class="h-100 flex w-full sm:flex-col">
        <div class="mr-10 w-3/12 sm:mb-4 sm:mr-0 sm:w-full">
            <h3 v-if="title">{{ title }}</h3>
            <template v-if="!isMobile">
                <v-list-item
                    v-for="link in links"
                    :key="link.title"
                    :title="link.title"
                    :to="link.to"
                >
                </v-list-item>
            </template>
            <div v-else class="rounded-md bg-white p-3 shadow-md">
                <v-tabs v-model="tabs" class="mb-0">
                    <v-tab
                        v-for="link in links"
                        :key="link.title"
                        :value="link.title"
                        :to="link.to"
                    >
                        {{ link.title }}
                    </v-tab>
                </v-tabs>
            </div>
        </div>
        <div class="w-9/12 sm:h-full sm:w-full">
            <slot />
        </div>
    </div>
</template>

<script setup>
import VListItem from "@/components/UI/VListItem.vue";
import { useScreen } from "@/composables/useScreen.js";
import VTabs from "@/components/UI/VTabs/VTabs.vue";
import VTab from "@/components/UI/VTabs/VTab.vue";
import { ref } from "vue";
import { TabPanel } from "@headlessui/vue";

defineProps({
    title: {
        type: String,
        default: "",
    },
    links: {
        type: Array,
        default: () => [],
    },
});

const { isMobile } = useScreen();

const tabs = ref(0);
</script>

<style scoped lang="scss"></style>
