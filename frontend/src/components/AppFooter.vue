<template>
    <footer class="bg-primary py-4 text-white">
        <div class="container">
            <div class="flex flex-row sm:flex-col">
                <div
                    class="d-flex flex-column mb-sm-0 mb-5 flex flex-col"
                    :style="{ 'min-width': '230px' }"
                >
                    <AppLogo />
                    <span class="mt-4 text-sm">© 2023 Alma Market</span>
                </div>
                <div class="flex flex-grow flex-wrap justify-between">
                    <div class="mb-3 mr-4">
                        <h3>Адрес</h3>
                        <p>194012, СПб, ул. Дрезденская 21/п</p>
                    </div>
                    <div class="mb-3 mr-4">
                        <h3>Телефон</h3>
                        <p>+7 (812) 970-61-94</p>
                    </div>
                    <div>
                        <h3>Email</h3>
                        <p>shop@nasgur.ru</p>
                    </div>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup>
import AppLogo from "@/components/AppLogo.vue";
</script>
