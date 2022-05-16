<template>
    <h1>Files</h1>
    <div class="row mb-3">
        <div class="col-md-12">
            <concepts-similarity />
        </div>
    </div>
    <div class="row">
        <div class="col-md-3">
            <div class="card">
                <div class="card-header">Files upload</div>
                <div class="card-body">
                    <file-pond
                        name="fileuploader"
                        ref="pond"
                        label-idle="Drop files here..."
                        :allow-multiple="true"
                        :instant-upload="false"
                        accepted-file-types="application/msword, text/plain"
                        :server="server"
                        :files="uploaderFiles"
                    />
                </div>
            </div>
        </div>
        <div class="col-md-9">
            <router-view />
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
                                            params: { id: file.id }
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
    </div>
</template>

<script>
import vueFilePond from "vue-filepond";
import "filepond/dist/filepond.min.css";
import ConceptsSimilarity from "../components/ConceptsSimilarity.vue";
import axios from "axios";
const FilePond = vueFilePond();

export default {
    components: {
        FilePond,
        ConceptsSimilarity
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
                this.$nextTick(()=>{
                    $("#myTable").DataTable();
                })
            });
    },
    computed: {
        server() {
            return {
                url: import.meta.env.VITE_APP_BASE_URL,
                process: {
                    url: "/docs",
                    onload: response => {
                        const data = JSON.parse(response);
                        this.files.push(data.document);
                        return data.document.id;
                    }
                }
            };
        }
    }
};
</script>

<style></style>
