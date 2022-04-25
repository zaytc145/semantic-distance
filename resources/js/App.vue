<template>
    <div>
        <h1>{{num}}</h1>
        <button @click="num+=31">increment</button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            num: 0
        };
    }
};
</script>

<style></style>
