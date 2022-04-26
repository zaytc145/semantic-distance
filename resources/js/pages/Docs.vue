<template>
    <h1>Files</h1>
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
                        accepted-file-types="application/msword"
                        :server="serverUrl"
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
                    <table class="table" id="myTable">
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
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import vueFilePond from "vue-filepond";
import "filepond/dist/filepond.min.css";
const FilePond = vueFilePond();

export default {
    components: {
        FilePond
    },
    data() {
        return {
            statusesColors: {
                processing: "bg-warning text-dark",
                complete: "bg-success",
                failed: "bg-danger"
            },
            uploaderFiles: [],
            files: [
                {
                    id: 1,
                    name: "file 1",
                    status: "processing"
                },
                {
                    id: 2,
                    name: "file 2",
                    status: "complete"
                },
                {
                    id: 3,
                    name: "file 3",
                    status: "failed"
                }
            ]
        };
    },
    mounted() {
        $("#myTable").DataTable();
    },
    computed: {
        serverUrl() {
            return import.meta.env.VITE_APP_BASE_URL + "/docs";
        }
    }
};
</script>

<style></style>
