<template>
  <div id="app">
    <TheNavbar />

    <div class="mt-10 px-2">
      <transition name="fade" mode="out-in">
        <router-view :key="$route.fullPath" />
      </transition>
    </div>

    <TheFooter />

    <TheToaster />

    <PortalTarget name="modals" multiple />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import TheNavbar from '@/components/TheNavbar.vue';
import TheToaster from '@/components/TheToaster.vue';
import TheFooter from '@/components/TheFooter.vue';

export default Vue.extend({
  components: { TheNavbar, TheToaster, TheFooter }
});
</script>

<style lang="postcss">
@import './assets/styles/tailwind.css';
</style>
