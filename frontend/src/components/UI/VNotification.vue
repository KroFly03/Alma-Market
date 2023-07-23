<template>
    <div class="v-notification" :class="[`v-notification--${type}`]">
        <button class="absolute right-1.5 top-1.5" @click="onClose">
            <v-icon :mdi-icon="mdiClose"></v-icon>
        </button>
        <div class="mr-2">
            <v-icon class="v-notification__type-icon" :mdi-icon="iconByType"></v-icon>
        </div>
        <div class="v-notification__content">
            <h5 class="mb-0.5">{{ title }}</h5>
            <p class="m-0 text-sm">{{ text }}</p>
        </div>
    </div>
</template>

<script setup>
import VIcon from "@/components/UI/VIcon.vue";
import { mdiAlert, mdiAlertCircle, mdiCheckCircle, mdiClose, mdiCloseCircle } from "@mdi/js";
import { computed } from "vue";

const props = defineProps({
    id: {
        type: String,
        default: "",
    },
    type: {
        type: String,
        default: "info",
        validator: (value) => ["success", "error", "warn", "info"].includes(value),
    },
    title: {
        type: String,
        default: "",
    },
    text: {
        type: String,
        default: "",
    },
});

const emit = defineEmits(["close"]);

const onClose = () => {
    emit("close", props.id);
};

const iconByType = computed(() => {
    switch (props.type) {
        case "success":
            return mdiCheckCircle;
        case "error":
            return mdiCloseCircle;
        case "warn":
            return mdiAlert;
        default:
            return mdiAlertCircle;
    }
});
</script>

<style scoped lang="scss">
.v-notification {
    @apply pointer-events-auto 
    relative z-50 
    mx-auto mt-3 
    flex 
    w-full max-w-[450px] 
    items-center 
    rounded-md
    bg-white 
    p-5 
    shadow-md;

    &--success {
        @apply bg-[#b8dfc6];

        .v-notification__type-icon {
            color: #22a562;
        }
    }

    &--error {
        @apply bg-[#fde3de];

        .v-notification__type-icon {
            @apply text-error;
        }
    }

    &--warn {
        @apply bg-[#ffe4c6];

        .v-notification__type-icon {
            @apply text-[#fea11a];
        }
    }

    &--info {
        @apply bg-[#c4e8fa];

        .v-notification__type-icon {
            @apply text-[#416db8];
        }
    }

    &__content {
        word-break: break-word;
    }

    &__type-icon {
        @apply h-8 w-8;
    }
}
</style>
