<template>
  <div id="app">
    <Navbar />
    <b-container fluid>
      <Alerts />
      <router-view />
    </b-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Navbar from "@/components/Navbar.vue";
import Alerts from "@/components/Alerts.vue";

export default Vue.extend({
  components: { Navbar, Alerts }
});
</script>
