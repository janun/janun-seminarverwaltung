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
      :key="comment.pk"
      :comment="comment"
      @delete="onDelete(comment.pk)"
      @update="onUpdate(comment.pk, $event)"
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
    seminarPk: { type: Number, required: true }
  },
  data: () => ({
    comments: [],
    newCommentText: '',
    sending: false
  }),
  computed: {
    baseURL() {
      return `seminars/${this.seminarPk}/comments/`
    }
  },
  async created() {
    this.comments = await this.$axios.$get(this.baseURL)
  },
  methods: {
    async onDelete(pk) {
      await this.$axios.$delete(`${this.baseURL}${pk}/`)
      this.comments = this.comments.filter(obj => obj.pk !== pk)
      this.$emit('commentDeleted', pk)
      this.$toast('Kommentar gelöscht.')
    },
    async onUpdate(pk, payload) {
      const data = await this.$axios.$put(`${this.baseURL}${pk}/`, payload)
      this.comments = this.comments.map(obj => (obj.pk === pk ? data : obj))
      this.$emit('commentUpdated', pk)
      this.$toast('Kommentar bearbeitet.')
    },
    async addComment(event) {
      if (event.shiftKey) {
        return
      }
      event.preventDefault()

      this.sending = true
      const newComment = {
        seminar: this.seminarPk,
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
