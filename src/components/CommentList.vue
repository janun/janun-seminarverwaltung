<template>
  <div>
    <form class="mb-10 clearfix" @submit.prevent="addComment">
      <BaseTextarea v-model="newCommentText" @keypress.enter="addComment" />
      <button
        class="btn primary mt-2 float-right"
        :class="{ loading: sending }"
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

<script lang="ts">
import Vue from 'vue';
import api from '@/services/api';
import BaseTextarea from '@/components/BaseTextarea.vue';
import CommentListComment from '@/components/CommentListComment.vue';

import { Comment } from '@/components/CommentListComment.vue';

export default Vue.extend({
  components: {
    CommentListComment,
    BaseTextarea
  },
  props: {
    seminarId: { type: Number, required: true }
  },
  data: () => ({
    comments: [] as Comment[],
    newCommentText: '',
    loading: false,
    sending: false
  }),
  computed: {
    baseURL(): string {
      return `seminars/${this.seminarId}/comments/`;
    }
  },
  created() {
    this.fetchComments();
  },
  methods: {
    async onDelete(pk: Comment['pk']) {
      try {
        await api.delete(`${this.baseURL}${pk}/`);
        this.$emit('commentDeleted', pk);
        this.$toast('Kommentar gelöscht.');
        this.comments = this.comments.filter((obj) => obj.pk !== pk);
      } catch (error) {
        this.$toast('Fehler beim Löschen des Kommentars', { type: 'error' });
      }
    },
    async onUpdate(pk: Comment['pk'], payload: Comment) {
      try {
        const response = await api.patch(`${this.baseURL}${pk}/`, payload);
        this.$emit('commentUpdated', pk);
        this.$toast('Kommentar bearbeitet.');
        this.comments = this.comments.map((obj) => (obj.pk === pk ? response.data : obj));
      } catch (error) {
        this.$toast('Fehler beim Ändern des Kommentars', { type: 'error' });
      }
    },
    async addComment(event: KeyboardEvent) {
      if (event.shiftKey) {
        return;
      }
      event.preventDefault();

      this.sending = true;
      const newComment: Comment = {
        seminar: this.seminarId,
        text: this.newCommentText
      };
      try {
        const response = await api.post(this.baseURL, newComment);
        this.comments.unshift(response.data);
        this.$toast('Kommentar erstellt.');
      } catch (error) {
        this.$toast('Fehler beim Speichern des Kommentars.', { type: 'error' });
      }
      this.newCommentText = '';
      this.sending = false;
    },
    async fetchComments() {
      this.loading = true;
      try {
        const response = await api.get(this.baseURL);
        this.comments = response.data;
      } catch (error) {
        this.$toast('Fehler beim Laden der Kommentare.', { type: 'error' });
      } finally {
        this.loading = false;
      }
    }
  }
});
</script>
