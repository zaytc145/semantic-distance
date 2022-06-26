<template>
    <h1>Files</h1>
    <div class="row mb-3">
        <!-- <div class="col-md-12">
            <concepts-similarity />
        </div> -->
        <div class="col-md-12">
            <document-form @created="addDoc" />
        </div>
    </div>
    <div class="row">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">Files list</div>
                <div class="card-body">
                    <table class="table" id="myTable" v-if="!isLoading">
                        <thead>
                            <tr>
                                <th scope="col">File name</th>
                                <th scope="col">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="file in files" :key="file.id">
                                <td>
                                    <router-link
                                        :to="{
                                            name: 'docs.doc',
                                            params: { id: file.id },
                                            query: { page: $route.query.page }
                                        }"
                                        >{{ file.name }}</router-link
                                    >
                                </td>
                                <td>
                                    <span
                                        class="badge"
                                        :class="statusesColors[file.status]"
                                        >{{ file.status }}</span
                                    >
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <div class="d-flex justify-content-center" v-else>
                        <div class="spinner-border" role="status">
                            <span class="visually-hidden">Loading...</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <router-view />
        </div>
    </div>
</template>

<script>
import "filepond/dist/filepond.min.css";
import ConceptsSimilarity from "../components/ConceptsSimilarity.vue";
import DocumentForm from "../components/DocumentForm.vue";
import axios from "axios";

export default {
    components: {
        ConceptsSimilarity,
        DocumentForm
    },
    data() {
        return {
            isLoading: false,
            statusesColors: {
                processing: "bg-warning text-dark",
                complete: "bg-success",
                failed: "bg-danger"
            },
            uploaderFiles: [],
            files: []
        };
    },
    mounted() {
        this.isLoading = true;
        axios
            .get(import.meta.env.VITE_APP_BASE_URL + "/docs")
            .then(response => {
                this.isLoading = false;
                this.files = response.data.docs;
                this.$nextTick(() => {
                    const table = $("#myTable").DataTable({
                        order: []
                    });
                    const { page } = this.$route.query;
                    if (page) {
                        table.page(page - 1).draw("page");
                    }
                    $("#myTable").on("page.dt", e => {
                        console.log(e);
                        console.log(table.page.info().page);
                        this.$router.replace({
                            query: {
                                page: table.page.info().page + 1
                            }
                        });
                    });
                });
            });
    },
    methods: {
        addDoc(doc) {
            this.files.push(doc);
        }
    }
};
</script>

<style></style>
