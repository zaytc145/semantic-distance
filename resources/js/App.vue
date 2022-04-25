<template>
    <div class="main">
        <div class="main-sidebar">
            <sidebar />
        </div>
        <div class="main-content">
            <navbar />
            <div class="container">
                <router-view />
            </div>
        </div>
    </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";
import Sidebar from "./components/Sidebar.vue";
import axios from "axios"

export default {
    components: { Sidebar, Navbar },
    data() {
        return {
            num: 0
        };
    },
};
</script>

<style>
#app {
    height: 100vh;
    max-height: 100vh;
}
.main {
    height: 100%;
    display: flex;
    flex-wrap: nowrap;
}

.main-content {
    width: 100%;
}
</style>
