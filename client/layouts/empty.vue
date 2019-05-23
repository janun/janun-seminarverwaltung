<template>
  <div>
    <div class="mx-auto sm:mt-10">
      <nuxt />
    </div>

    <TheFooter />

    <TheToaster />

    <PortalTarget name="modals" multiple />
  </div>
</template>

<script>
import TheFooter from '@/components/TheFooter.vue'
import TheToaster from '@/components/TheToaster.vue'

export default {
  components: {
    TheFooter,
    TheToaster
  }
}
</script>
