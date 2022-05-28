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
                    class="list-group-item d-flex align-items-center"
                >
                    <h5 class="mb-0">{{ name }}</h5>
                </li>
                <li
                    class="list-group-item d-flex justify-content-between align-items-center"
                >
                    <b>Status:</b>
                    <span class="badge" :class="statusesColors[status]">{{
                        status
                    }}</span>
                </li>
                <li class="list-group-item d-flex align-items-center flex-wrap">
                    <b class="me-2">keywords:</b>
                    <span
                        class="badge me-2 mb-1"
                        :class="{
                            'bg-secondary': !word.fromOntology,
                            'bg-primary': word.fromOntology
                        }"
                        v-for="word in keyWords"
                        :key="word.id"
                        >{{ word.name }}</span
                    >
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
import axios from "axios";
export default {
    data() {
        return {
            isLoading: false,
            name: "",
            keyWords: [],
            status: "",
            statusesColors: {
                processing: "bg-warning text-dark",
                complete: "bg-success",
                failed: "bg-danger"
            }
        };
    },
    created() {
        this.fetchData();
    },
    watch: {
        $route: "fetchData"
    },
    methods: {
        fetchData() {
            this.isLoading = true;
            axios
                .get(
                    import.meta.env.VITE_APP_BASE_URL +
                        "/docs/" +
                        this.$route.params.id
                )
                .then(response => {
                    this.isLoading = false;
                    const { name, status, keyWords } = response.data.doc;
                    this.name = name;
                    this.status = status;
                    this.keyWords = keyWords;
                })
                .catch(() => {
                    this.isLoading = false;
                });
        }
    }
};
</script>

<style></style>
