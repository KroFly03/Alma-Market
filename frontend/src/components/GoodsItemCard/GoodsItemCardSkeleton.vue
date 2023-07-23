<template>
    <div class="goods-item-card-skeleton">
        <v-skeleton-image class="goods-item-card-skeleton__img"></v-skeleton-image>
        <div class="goods-item-card-skeleton__content">
            <v-skeleton-text class="sm:h-24" line-height="20px" :lines="2"></v-skeleton-text>
            <div class="goods-item-card-skeleton__actions">
                <v-skeleton-text line-height="20px" width="80px"></v-skeleton-text>
                <v-skeleton-btn class="ml-3 sm:mt-1"></v-skeleton-btn>
            </div>
        </div>
    </div>
</template>

<script setup>
import VSkeletonImage from "@/components/UI/VSkeleton/VSkeletonImage.vue";
import VSkeletonText from "@/components/UI/VSkeleton/VSkeletonText.vue";
import VSkeletonBtn from "@/components/UI/VSkeleton/VSkeletonBtn.vue";
</script>

<style lang="scss" scoped>
.goods-item-card-skeleton {
    @apply flex flex-col 
    rounded-md 
    bg-white 
    p-6 
    shadow-md
    sm:flex-row;

    &__img {
        @apply h-[250px] w-full 
        sm:mr-3 sm:h-[120px] sm:w-[100px];
    }

    &__content {
        @apply my-3 
        flex flex-col 
        sm:m-0 sm:grow sm:justify-between;
    }

    &__actions {
        @apply mt-3 
        flex items-center justify-end 
        sm:mt-auto sm:flex-col sm:items-end;
    }
}
</style>
