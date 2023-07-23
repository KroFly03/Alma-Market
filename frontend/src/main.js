import App from "@/App.vue";
import NotificationApp from "@/AppNotification.vue";
import { createApp } from "vue";
import router from "@/router/router.js";
import { createPinia } from "pinia";

import "./index.scss";

const app = createApp(App);

app.use(router);
app.use(createPinia());

app.mount("#app");

export const notification = createApp(NotificationApp).mount("#app-notification");
