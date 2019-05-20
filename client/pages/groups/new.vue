<template>
  <div class="mx-auto max-w-4xl">
    <h1 class="text-xl text-green-500 font-bold mb-5">Neue Gruppe</h1>
    <GroupForm :saving="saving" @save="save" />
  </div>
</template>

<script>
import GroupForm from '@/components/GroupForm.vue'

export default {
  components: {
    GroupForm
  },
  data() {
    return {
      saving: false
    }
  },
  meta() {
    return {
      title: 'Neue Gruppe'
    }
  },
  methods: {
    async save(payload) {
      this.saving = true
      const data = await this.$axios.$post(`/groups/`, payload)
      this.$toast(`Gruppe ${data.name} erstellt`)
      this.$router.push(`/groups/${data.pk}`)
      this.saving = false
    }
  }
}
</script>
