import { createRouter, createWebHistory } from "vue-router";
import Docs from "../pages/Docs.vue";
import Doc from "../pages/Doc.vue";

const routerHistory = createWebHistory();

const routes = [
    {
        path: "/docs",
        component: Docs,
        name: "docs",
        children: [{ path: "/docs/:id", component: Doc, name: "docs.doc" }]
    },
    { path: "/", redirect: { name: 'docs' } }
];

const router = createRouter({
    routes,
    history: routerHistory
});

export default router;
