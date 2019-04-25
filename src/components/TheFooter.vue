<template>
  <div
    class="text-center pb-10 pt-5 mt-20 absolute bottom-0 h-48 w-full"
    style="background:#f2f5f0"
  >
    <h3 class="text-green-500 font-normal text-2xl">
      Hilfe
    </h3>
    <p>Irgendwas geht nicht oder Du hast Fragen?</p>
    <p>
      Telefon: <a :href="'tel:' + helpPhone">{{ helpPhone }}</a>
      <br />
      E-Mail: <a :href="'mailto:' + helpMail">{{ helpMail }}</a>
      <br />
      <a target="_blank" :href="seminarPolicyURL">Download Seminarrichtlinie</a>
    </p>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  data: () => ({
    helpPhone: '12312312312',
    helpMail: 'seminar@janun.de',
    seminarPolicyURL: 'https://www.janun.de/downloads'
  })
});
</script>

<style lang="postcss">
html {
  height: 100%;
}

body {
  position: relative;
  min-height: 100%;
  padding-bottom: 16.25rem;
}
</style>
