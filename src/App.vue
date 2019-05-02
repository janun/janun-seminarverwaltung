<template>
  <div id="app" class="antialiased font-sans text-gray-700 text-base leading-normal">
    <TheNavbar />

    <div class="mt-10 px-2">
      <router-view />
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
