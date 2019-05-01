<template>
  <div class="mx-auto px-4 max-w-5xl">
    <div class="fullspinner" v-if="loading" />

    <div v-if="object">
      <DeleteSeminarButton v-if="isStaff" :seminar="object" class="float-right" />
      <!-- <button @click="applySuccessModal = true" class="float-right mx-2">Show Success Modal</button> -->

      <h1 class="text-3xl text-green-500 font-bold">
        {{ object.title }}
      </h1>

      <div class="mb-5">
        Am {{ object.start_date | date }}
        <span v-if="object.location">in {{ object.location }}</span>
      </div>

      <!-- <StatusBadge :value="object.status" class="mb-5" /> -->

      <div class="text-gray-700 text-sm">
        <div class="">Deadline zur Abrechnung: {{ object.deadline | date }}</div>
        <div>
          angemeldet von
          <router-link
            class="text-green-500"
            :to="{ name: 'UserDetail', params: { pk: object.owner.pk } }"
          >
            {{ object.owner.name }}
          </router-link>
          am {{ object.created_at | date }}
          <br />
          zuletzt geändert am {{ object.updated_at | date }}
        </div>
        <div v-if="object.group">
          Gruppe:
          <router-link
            class="text-green-500"
            :to="{ name: 'GroupDetail', params: { pk: object.group.pk } }"
          >
            {{ object.group.name }}
          </router-link>
        </div>
      </div>

      <SeminarForm ref="seminarForm" :object="object" />

      <div class="flex flex-wrap mt-20">
        <div class="w-full md:w-1/3 mb-5">
          <h2 class="text-green-500 font-bold">Kommentare</h2>
        </div>

        <div class="w-full md:w-2/3">
          <CommentList class="w-full" :seminarId="pk" />
        </div>
      </div>
    </div>

    <BaseModal :show="applySuccessModal" @close="applySuccessModal = false">
      <h1 class="text-green-500 font-bold text-2xl mb-6 flex items-center justify-center">
        <svg class="fill-current h-6 w-6 mr-2" viewBox="0 0 20 20">
          <path
            d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM6.7 9.29L9 11.6l4.3-4.3 1.4 1.42L9 14.4l-3.7-3.7 1.4-1.42z"
          />
        </svg>
        Seminar angemeldet.
      </h1>

      <ul class="list-disc pl-5">
        <li class="my-3">
          Es wurde eine <strong>Bestätigungsmail</strong> an {{ user.email }} geschickt.
        </li>
        <li class="my-3">
          Wir werden Dein Seminar jetzt prüfen. Die <strong>Zusage</strong> solltest Du
          <strong>in den nächsten Tagen</strong> erhalten.
        </li>
        <li class="my-3">
          Solange, der Status des Seminars noch nicht zugesagt ist, kannst Du das Seminar
          <strong>noch bearbeiten</strong>.
        </li>
      </ul>

      <div class="card-footer flex">
        <button class="ml-auto btn btn-primary bg-gray-700" @click="applySuccessModal = false">
          Schließen
        </button>
      </div>
    </BaseModal>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { Seminar } from '@/types';
import userMixin from '@/mixins/user.ts';

import SeminarForm from '@/components/SeminarForm.vue';
import SeminarStatus from '@/components/SeminarStatus.vue';
import CommentList from '@/components/CommentList.vue';
import StatusBadge from '@/components/StatusBadge.vue';
import DeleteSeminarButton from '@/components/DeleteSeminarButton.vue';
import BaseModal from '@/components/BaseModal.vue';

export default Vue.extend({
  mixins: [userMixin],
  components: {
    SeminarForm,
    SeminarStatus,
    CommentList,
    StatusBadge,
    DeleteSeminarButton,
    BaseModal
  },
  props: {
    pk: { type: Number, required: true }
  },
  data: () => ({
    applySuccessModal: true,
    loading: true,
    saving: false
  }),
  computed: {
    object(): Seminar | undefined {
      return this.$store.getters['seminars/byPk'](this.pk);
    }
  },
  async created() {
    this.loading = true;
    try {
      await this.$store.dispatch('seminars/fetchSingle', this.pk);
      if (this.object) {
        document.title = this.object.title;
      }
    } catch (error) {
      alert('Fehler beim Laden des Seminars');
    } finally {
      this.loading = false;
    }
  }
});
</script>
