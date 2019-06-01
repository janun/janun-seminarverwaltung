<template>
  <div>
    <BaseModal
      v-for="message in messages"
      :key="message.id"
      :show="true"
      :close-on-esc="false"
      :close-on-backdrop="false"
      @close="close(message.id)"
    >
      <h2 v-if="message.title" class="text-green-500 text-xl font-bold mb-4">
        {{ message.title }}
      </h2>

      <!-- eslint-disable-next-line vue/no-v-html -->
      <div v-html="message.text"></div>

      <div class="flex mt-4">
        <button class="ml-auto btn btn-primary" @click="close">Okay</button>
      </div>
    </BaseModal>
  </div>
</template>

<script>
import BaseModal from '@/components/BaseModal.vue'

export default {
  components: {
    BaseModal
  },
  computed: {
    messages() {
      return this.$store.state.messages.messages
    }
  },
  methods: {
    close(id) {
      this.$store.commit('messages/delete', id)
    }
  }
}
</script>
