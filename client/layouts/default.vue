<template>
  <div>
    <TheNavbar />

    <div class="mx-auto px-4 mt-10">
      <nuxt />
    </div>

    <TheFooter />

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
