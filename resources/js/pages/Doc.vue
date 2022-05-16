<template>
    <div class="card mb-3">
        <div class="card-header d-flex justify-content-between">
            File information
            <router-link
                :to="{ name: 'docs' }"
                type="button"
                class="btn-close"
                aria-label="Close"
            ></router-link>
        </div>
        <div class="card-body">
            <ul class="list-group mb-3">
                <li
                    class="list-group-item d-flex justify-content-between align-items-center"
                >
                    <b>Document name:</b>
                    <h5 class="mb-0">file {{ this.$route.params.id }}</h5>
                </li>
                <li
                    class="list-group-item d-flex justify-content-between align-items-center"
                >
                    <b>Status:</b>
                    <span class="badge bg-success">complete</span>
                </li>
            </ul>
            <div v-if="status === 'complete'">
                <h5>Related files:</h5>
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col">File name</th>
                                <th scope="col">Cos sim</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="num in 3" :key="num">
                                <td>File {{ num * 2 }}</td>
                                <td>{{ Math.round(Math.random() * 100) }} %</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            status: "complete"
        };
    }
};
</script>

<style></style>
