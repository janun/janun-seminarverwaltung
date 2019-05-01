<template>
  <div class="bg-white shadow max-w-lg my-5 px-4 pt-2 pb-4 rounded">
    <div class="text-xs my-2">
      <span>
        {{ comment.owner.name }},
        {{ comment.created_at | datetime }}
      </span>
      <div v-if="user.pk === comment.owner.pk || isStaff" class="float-right">
        <button type="button" class="hover:text-gray-900 mx-1 select-none" @click="toggleEdit">
          bearbeiten
        </button>
        <button type="button" class="hover:text-gray-900 mx-1 select-none" @click="onDelete">
          löschen
        </button>
      </div>
    </div>

    <form v-if="editing" class="clearfix" @submit.prevent="onChange">
      <BaseTextarea v-model="form.text" @keypress.enter="onChange" />
      <span class="float-right mt-1">
        <button class="btn btn-tertiary text-xs mx-1" type="button" @click="toggleEdit">
          Abbrechen
        </button>
        <button class="btn btn-secondary text-xs mx-1" type="submit">Speichern</button>
      </span>
    </form>

    <p v-if="!editing" class="whitespace-pre" v-text="comment.text" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import userMixin from '@/mixins/user.ts';
import BaseTextarea from '@/components/BaseTextarea.vue';

export interface Comment {
  pk?: number;
  seminar: number;
  text: string;
}

export default Vue.extend({
  components: {
    BaseTextarea
  },
  mixins: [userMixin],
  props: {
    comment: { type: Object, required: true }
  },
  data: () => ({
    editing: false,
    form: {
      text: ''
    }
  }),
  methods: {
    copyFields(): void {
      if (this.comment) {
        for (const key in this.form) {
          if (this.form.hasOwnProperty(key)) {
            Vue.set(this.form, key, this.comment[key as keyof Comment]);
          }
        }
      }
    },
    onDelete() {
      this.$emit('delete');
    },
    toggleEdit() {
      if (this.editing) {
        this.editing = false;
      } else {
        this.copyFields();
        this.editing = true;
      }
    },
    onChange(event: KeyboardEvent) {
      if (event.shiftKey) {
        return;
      }
      event.preventDefault();

      this.editing = false;
      if (this.form.text === '') {
        this.onDelete();
      } else {
        this.$emit('update', this.form);
      }
    }
  }
});
</script>
