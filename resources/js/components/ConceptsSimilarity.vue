<template>
    <div class="card">
        <div class="card-header">Concepts Similarity</div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-12">
                    <form @submit.prevent="search">
                        <div class="row g-3">
                            <div class="col">
                                <input
                                    v-model="concept1"
                                    type="text"
                                    class="form-control"
                                    placeholder="Concept 1"
                                    aria-label="Concept 1"
                                    required
                                />
                            </div>
                            <div class="col">
                                <input
                                    v-model="concept2"
                                    type="text"
                                    class="form-control"
                                    placeholder="Concept 2"
                                    aria-label="Concept 2"
                                    required
                                />
                            </div>
                            <div class="col">
                                <button type="submit" class="btn btn-primary">
                                    Compare
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="col-md-12" v-if="results">
                    <hr>
                    <div class="table-responsive">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">Concept 1</th>
                                    <th scope="col">Concept 2</th>
                                    <th scope="col">Sim</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>{{results.concept1.label}}</td>
                                    <td>{{results.concept2.label}}</td>
                                    <td>{{results.sim.toFixed(2) * 100}}%</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios"

export default {
    data() {
        return {
            concept1: 'сходимость',
            concept2: 'Ряд Фурье',
            results: null
        };
    },
    methods: {
        search() {
            axios.post('/concepts/compare',{
                label_1: this.concept1,
                label_2: this.concept2
            }).then(response =>{
                this.results = response.data
                console.log(this.results);
            })
        }
    }
};
</script>

<style></style>
