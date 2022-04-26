<template>
    <div class="card mb-5">
        <div class="card-header d-flex justify-content-between">
            Sing doc {{ this.$route.params.id }}
            <router-link
                :to="{ name: 'docs' }"
                type="button"
                class="btn-close"
                aria-label="Close"
            ></router-link>
        </div>
        <div class="card-body">Sing doc</div>
    </div>
</template>

<script>
export default {};
</script>

<style></style>
