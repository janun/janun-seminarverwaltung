<template>
  <div class="relative min-h-screen">
    <TheNavbar />

    <div class="mx-auto px-4 mt-5 pb-64">
      <nuxt />
    </div>

    <TheFooter class="absolute bottom-0 h-48 mt-16" />

    <TheToaster />

    <PortalTarget name="modals" multiple />
  </div>
</template>

<script>
import TheNavbar from '@/components/TheNavbar.vue'
import TheFooter from '@/components/TheFooter.vue'
import TheToaster from '@/components/TheToaster.vue'

export default {
  components: {
    TheNavbar,
    TheFooter,
    TheToaster
  }
}
</script>
