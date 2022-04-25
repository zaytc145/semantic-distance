<template>
    <div
        class="sidebar d-flex flex-column flex-shrink-0 p-3 text-white bg-dark"
        style="width: 280px"
    >
        <span class="fs-4">Semantic Distance</span>
        <hr />
        <ul class="nav nav-pills flex-column mb-auto">
            <li class="nav-item">
                <router-link
                    :to="{ name: 'main' }"
                    class="nav-link text-white"
                    aria-current="page"
                    active-class="active"
                >
                    Search
                </router-link>
            </li>
            <li>
                <router-link
                    :to="{ name: 'docs' }"
                    active-class="active"
                    class="nav-link text-white"
                >
                    Files
                </router-link>
            </li>
        </ul>
        <hr />
    </div>
</template>

<script>
export default {};
</script>

<style>
.sidebar {
    height: 100%;
}
</style>
