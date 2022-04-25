import { createRouter, createWebHistory } from "vue-router";
import Main from "../pages/Main.vue";
import Docs from "../pages/Docs.vue";

const routerHistory = createWebHistory();

const routes = [
    { path: "/docs", component: Docs, name: "docs" },
    { path: "/", component: Main, name: "main" }
];

const router = createRouter({
    routes,
    history: routerHistory
});

export default router;
