<template>
<div class="user">
    <img alt="User profile picture" src="{{ user.picture }}">

</div>
</template>

<style scoped>
.avatar {
    vertical-align: middle;
    width: 50px;
    height: 50px;
    border-radius: 50%;
}
.user {
    display: inline-block;
    margin: 10px 10px 10px 10px;
}
</style>

<script setup lang="ts">
import user from "./User.vue";
</script>