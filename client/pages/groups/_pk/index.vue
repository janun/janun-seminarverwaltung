<template>
  <div class="mx-auto max-w-4xl">
    <div class="flex flex-wrap items-center">
      <h1 class="text-xl text-green-500 font-bold mb-5">{{ group.name }}</h1>
      <GroupDeleteButton
        :group="group"
        class="ml-auto btn btn-outline text-red-500"
      />
    </div>
  </div>
</template>

<script>
import GroupDeleteButton from '@/components/GroupDeleteButton.vue'

export default {
  components: {
    GroupDeleteButton
  },
  data() {
    return {
      saving: false,
      group: {}
    }
  },
  head() {
    return {
      title: this.group.name
    }
  },
  async asyncData({ $axios, params }) {
    const data = await $axios.$get(`/groups/${params.pk}/`)
    return { group: data }
  }
}
</script>
