<template>
  <div class="mx-auto max-w-4xl">
    <div class="flex flex-wrap items-start">
      <h1 class="text-xl text-green-500 font-bold mb-5">{{ group.name }}</h1>
      <div class="ml-auto">
        <GroupDeleteButton
          :group="group"
          class="btn btn-outline text-red-500"
        />
        <nuxt-link
          class="mt-2 btn btn-outline"
          :to="`/groups/${group.pk}/edit`"
        >
          Bearbeiten
        </nuxt-link>
      </div>
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
