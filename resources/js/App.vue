<template>
    <div class="main">
        <navbar />
        <div class="container pt-5">
            <router-view />
        </div>
    </div>
</template>

<script>
import Navbar from "./components/Navbar.vue";

export default {
    components: { Navbar },
    data() {
        return {
            num: 0
        };
    }
};
</script>

<style>
#app {
    height: 100vh;
    max-height: 100vh;
}
.main {
    height: 100%;
}

.main-content {
    width: 100%;
}
</style>
