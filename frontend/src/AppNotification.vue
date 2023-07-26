<template>
    <div class="notification-wrapper">
        <transition-group>
            <v-notification
                v-for="notification in notifications"
                :id="notification.id"
                :key="notification.id"
                :type="notification.type"
                :title="notification.title"
                :text="notification.text"
                :duration="notification.duration"
                @close="onClose"
            ></v-notification>
        </transition-group>
    </div>
</template>

<script setup>
import VNotification from "@/components/UI/VNotification.vue";
import { ref } from "vue";
import { v4 } from "uuid";

const notifications = ref([]);

const show = (type, title, text, duration = 8000) => {
    const id = v4();

    notifications.value.push({ id, type, title, text, duration });
    setTimeout(() => {
        onClose(id);
    }, duration);
};

const onClose = (id) => {
    const index = notifications.value.findIndex((x) => x.id === id);

    if (index === -1) return;

    notifications.value.splice(index, 1);
};

defineExpose({ show });
</script>

<style lang="scss" scoped>
.notification-wrapper {
    @apply pointer-events-none fixed left-0 right-0 top-0 z-50 px-2;
}

.v-enter-active,
.v-leave-active {
    transition: opacity 0.3s ease-out;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
}
</style>
