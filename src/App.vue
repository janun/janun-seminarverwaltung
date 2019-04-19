<template>
  <div id="app">
    <Navbar />
    <div class="section">
      <router-view />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Navbar from "@/components/Navbar.vue";

export default Vue.extend({
  components: { Navbar }
});
</script>

<style lang="sass">
  @import "@/assets/styles/bulma.scss"
</style>

