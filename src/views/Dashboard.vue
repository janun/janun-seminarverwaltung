<template>
  <div>
    <h1 class="title">Willkommen, {{ user.name }}</h1>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import userMixin from "@/mixins/user.ts";

export default Vue.extend({
  mixins: [userMixin]
});
</script>
