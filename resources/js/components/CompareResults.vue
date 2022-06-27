<template>
    <div class="row">
        <div class="col-md-6">
            <h5>No concepts</h5>
            <h5>Articles num: {{ noConceptsNum }}</h5>
            <table class="table" v-if="!isLoading">
                <thead>
                    <tr>
                        <th scope="col">File name</th>
                        <th scope="col">Cos sim</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="file in noConcepts" :key="file.id">
                        <td>
                            {{ file.doc.name }}
                        </td>
                        <td>{{ Math.round(file.value * 100) }} %</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="col-md-6">
            <h5>With concepts</h5>
            <h5>Articles num: {{ withConceptsNum }}</h5>
            <table class="table" v-if="!isLoading">
                <thead>
                    <tr>
                        <th scope="col">File name</th>
                        <th scope="col">Cos sim</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="file in withConcepts" :key="file.id">
                        <td>
                            {{ file.doc.name }}
                        </td>
                        <td>{{ Math.round(file.value * 100) }} %</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            noConcepts: [],
            withConcepts: [],
            noConceptsNum: 0,
            withConceptsNum: 0
        };
    },
    mounted() {
        axios.get("/comparison").then(response => {
            this.noConcepts = response.data.noConcepts;
            this.withConcepts = response.data.withConcepts;
            this.noConceptsNum = response.data.noConceptsNum;
            this.withConceptsNum = response.data.withConceptsNum;
        });
    }
};
</script>

<style></style>
