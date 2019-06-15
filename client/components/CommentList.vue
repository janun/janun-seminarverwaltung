<template>
  <div>
    <form class="mb-10 clearfix" @submit.prevent="addComment">
      <BaseTextarea v-model="newCommentText" @keypress.enter="addComment" />
      <button
        class="btn btn-primary mt-2 float-right"
        :class="{ 'btn-loading': sending }"
        :disabled="!newCommentText"
        type="submit"
      >
        Kommentieren
      </button>
    </form>

    <CommentListComment
      v-for="comment in comments"
      :key="comment.uuid"
      :comment="comment"
      @delete="onDelete(comment.uuid)"
      @update="onUpdate(comment.uuid, $event)"
    />
  </div>
</template>

<script>
import CommentListComment from '@/components/CommentListComment.vue'

export default {
  components: {
    CommentListComment
  },
  props: {
    seminarUuid: { type: String, required: true }
  },
  data: () => ({
    comments: [],
    newCommentText: '',
    sending: false
  }),
  computed: {
    baseURL() {
      return `seminars/${this.seminarUuid}/comments/`
    }
  },
  async created() {
    this.comments = await this.$axios.$get(this.baseURL)
  },
  methods: {
    async onDelete(uuid) {
      await this.$axios.$delete(`${this.baseURL}${uuid}/`)
      this.comments = this.comments.filter(obj => obj.uuid !== uuid)
      this.$emit('commentDeleted', uuid)
      this.$toast('Kommentar gelöscht.')
    },
    async onUpdate(uuid, payload) {
      const data = await this.$axios.$put(`${this.baseURL}${uuid}/`, payload)
      this.comments = this.comments.map(obj => (obj.uuid === uuid ? data : obj))
      this.$emit('commentUpdated', uuid)
      this.$toast('Kommentar bearbeitet.')
    },
    async addComment(event) {
      if (event.shiftKey) {
        return
      }
      event.preventDefault()

      this.sending = true
      const newComment = {
        text: this.newCommentText
      }
      const data = await this.$axios.$post(this.baseURL, newComment)
      this.comments.unshift(data)
      this.$toast('Kommentar erstellt.')
      this.newCommentText = ''
      this.sending = false
    }
  }
}
</script>
