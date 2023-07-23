<template>
    <MenuItem>
        <v-list-item :title="title" :to="to"></v-list-item>
    </MenuItem>
</template>

<script setup>
import { MenuItem } from "@headlessui/vue";
import VListItem from "@/components/UI/VListItem.vue";

defineProps({
    to: {
        type: [null, String, Object],
        default: null,
    },
    title: {
        type: String,
        default: "",
    },
});
</script>

<style scoped lang="scss"></style>
