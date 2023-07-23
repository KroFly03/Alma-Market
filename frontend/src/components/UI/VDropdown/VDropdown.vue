<template>
    <Menu v-slot="{ close }" as="div" class="v-dropdown">
        <MenuButton as="template">
            <slot name="target"></slot>
        </MenuButton>

        <transition
            enter-active-class="transition duration-100 ease-out"
            enter-from-class="transform scale-95 opacity-0"
            enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0"
        >
            <!--                class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"-->
            <MenuItems class="v-dropdown__menu" @click="close">
                <slot></slot>
            </MenuItems>
        </transition>
    </Menu>
</template>

<script setup>
import { Menu, MenuButton, MenuItems, MenuItem } from "@headlessui/vue";
import VBtn from "@/components/UI/VBtn.vue";
</script>

<style scoped lang="scss">
.v-dropdown {
    @apply relative inline-block text-left;

    &__menu {
        @apply absolute right-0 z-10 
        mt-2 
        w-56 
        origin-top-right 
        rounded-md 
        bg-white 
        p-1
        shadow-lg 
        focus:outline-none;
    }

    &__item {
        @apply flex w-full justify-start rounded bg-white px-2 py-2;
    }
}
</style>
