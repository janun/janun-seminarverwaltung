<template>
  <div class="mx-auto max-w-4xl">
    <div class="flex flex-wrap items-center">
      <h1 class="text-xl text-green-500 font-bold mb-5">{{ group.name }}</h1>
      <GroupDeleteButton :group="group" class="ml-auto" />
    </div>
    <GroupForm :object="group" :saving="saving" @save="save" />
  </div>
</template>

<script>
import GroupDeleteButton from '@/components/GroupDeleteButton.vue'
import GroupForm from '@/components/GroupForm.vue'

export default {
  components: {
    GroupDeleteButton,
    GroupForm
  },
  data() {
    return {
      saving: false,
      group: {}
    }
  },
  head() {
    return {
      title: `${this.group.name} bearbeiten`
    }
  },
  middleware: 'staffOnly',
  async asyncData({ $axios, params }) {
    const data = await $axios.$get(`/groups/${params.slug}/`)
    return { group: data }
  },
  methods: {
    async save(payload) {
      this.saving = true
      try {
        this.group = await this.$axios.$put(
          `/groups/${this.group.slug}/`,
          payload
        )
        this.$toast(`Änderungen an ${this.group.name} gespeichert.`)
      } catch (error) {
        this.$nuxt.error(error)
      } finally {
        this.saving = false
      }
    }
  }
}
</script>
