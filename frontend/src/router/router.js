import { createRouter, createWebHistory } from "vue-router";

import Home from "@/pages/Home.vue";
import GoodsItem from "@/pages/GoodsItem.vue";
import Cart from "@/pages/Cart/Cart.vue";
import AccountOrders from "@/pages/Account/AccountOrders.vue";
import AccountSettings from "@/pages/Account/AccountSettings/AccountSettings.vue";
import AdminGoods from "@/pages/Admin/AdminGoods.vue";
import AdminOrders from "@/pages/Admin/AdminOrders.vue";
import AdminUsers from "@/pages/Admin/AdminUsers.vue";
import AdminGoodsItem from "@/pages/Admin/AdminGoodsItem.vue";
import NotFound from "@/pages/NotFound.vue";
import Privacy from "@/pages/SitePrivacy.vue";
import AccountActivation from "@/pages/AccountActivation.vue";
import ResetPassword from "@/pages/ResetPassword.vue";
import BaseLayout from "@/layouts/AppLayout.vue";
import AccountLayout from "@/layouts/AccountLayout.vue";
import AdminLayout from "@/layouts/AdminLayout.vue";

const routes = [
    {
        path: "/",
        component: BaseLayout,
        children: [
            {
                path: "/",
                name: "Home",
                component: Home,
                children: [
                    {
                        path: "/reset_password/:uid/:token",
                        name: "ResetPassword",
                        component: ResetPassword,
                        props: true,
                    },
                ],
                props: (route) => ({
                    search: route.query.search,
                    category: parseInt(route.query.category) || null,
                    manufacturer: parseInt(route.query.manufacturer) || null,
                    priceMin: parseInt(route.query.priceMin) || null,
                    priceMax: parseInt(route.query.priceMax) || null,
                }),
            },
            {
                path: "/goods/:id(\\d+)/:tab?",
                name: "GoodsItem",
                component: GoodsItem,
                props: true,
            },
            {
                path: "/cart",
                name: "Cart",
                component: Cart,
            },
            {
                path: "/activate/:uid/:token",
                name: "AccountActivation",
                component: AccountActivation,
                props: true,
            },
            {
                path: "/privacy",
                name: "Privacy",
                component: Privacy,
            },
            {
                path: "/account",
                name: "Account",
                component: AccountLayout,
                redirect: { name: "AccountOrders" },
                meta: {
                    requiredAuth: true,
                },
                children: [
                    {
                        path: "orders",
                        name: "AccountOrders",
                        component: AccountOrders,
                    },
                    {
                        path: "settings",
                        name: "AccountSettings",
                        component: AccountSettings,
                    },
                ],
            },
            {
                path: "/admin",
                name: "Admin",
                component: AdminLayout,
                redirect: { name: "AdminGoods" },
                meta: {
                    requiredAuth: true,
                    role: "admin",
                },
                children: [
                    {
                        path: "goods",
                        name: "AdminGoods",
                        component: AdminGoods,
                    },
                    {
                        path: "goods/:id(\\d+)",
                        name: "AdminGoodsItem",
                        component: AdminGoodsItem,
                        props: (route) => ({ isEdit: true, id: route.params.id }),
                    },
                    {
                        path: "goods/new",
                        name: "AdminGoodsItemNew",
                        component: AdminGoodsItem,
                    },
                    {
                        path: "orders",
                        name: "AdminOrders",
                        component: AdminOrders,
                    },
                    {
                        path: "users",
                        name: "AdminUsers",
                        component: AdminUsers,
                    },
                ],
            },
            {
                path: "/:pathMatch(.*)*",
                name: "NotFound",
                component: NotFound,
            },
        ],
    },
];

const router = createRouter({
    routes,
    scrollBehavior: (to, from, savedPosition) => {
        if (savedPosition) return savedPosition;
        if (to.name === from.name) return;

        return { top: 0 };
    },
    history: createWebHistory(),
});

export default router;
