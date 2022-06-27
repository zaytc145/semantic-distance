<template>
    <div class="document-form">
        <div class="card">
            <div class="card-header">Add document</div>
            <div class="card-body">
                <form @submit.prevent="submit">
                    <div class="mb-3">
                        <label class="form-label" for="">Название</label>
                        <input
                            type="text"
                            class="form-control"
                            v-model="name"
                        />
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="">Ключевые слова</label>
                        <input
                            type="text"
                            class="form-control"
                            v-model="keywords"
                        />
                    </div>
                    <button type="submit" class="btn btn-primary">
                        Добавить
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
export default {
    data() {
        return {
            name: "Test 1",
            keywords: "задача оптимального управления, принцип максимума, экстремальные процессы"
        };
    },
    methods: {
        submit() {
            axios
                .post("docs", {
                    name: this.name,
                    keywords: this.keywords.split(",").map(word => word.trim())
                })
                .then(response => {
                    this.name = "";
                    this.keywords = "";
                    this.$emit("created", response.data.doc);
                });
        }
    }
};
</script>

<style></style>
