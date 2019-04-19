<template>
  <div
    class="container"
    style="position: relative; max-width: 960px; margin-left: auto; margin-right: auto"
  >
    <b-loading :is-full-page="false" :active="loading" />

    <div v-if="object">
      <h1 class="title has-text-primary" style="margin-bottom:0.5rem">{{ object.title }}</h1>

      <div style="font-weight:bold; margin-bottom: 1rem">
        Am {{ object.start_date | date }}
        <span v-if="object.location">in {{ object.location }}</span>
      </div>

      <div>
        <div>
          angemeldet von
          <router-link :to="{ name: 'UserDetail', params: { pk: object.owner.pk } }">
            {{ object.owner.name }}
          </router-link>
          am {{ object.created_at | date }}
          <br />
          geändert am {{ object.updated_at | date }}
        </div>
        <div v-if="object.group">
          Gruppe:
          <router-link :to="{ name: 'GroupDetail', params: { pk: object.group.pk } }">
            {{ object.group.name }}
          </router-link>
        </div>
      </div>

      <SeminarStatus :value="object.status" :seminar="object" class="is-pulled-right" />
      <hr />
      <SeminarForm ref="seminarForm" :object="object" />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Seminar } from "@/types";

import SeminarForm from "@/components/SeminarForm.vue";
import SeminarStatus from "@/components/SeminarStatus.vue";

export default Vue.extend({
  components: {
    SeminarForm,
    SeminarStatus
  },
  props: {
    pk: { type: [Number], required: true }
  },
  data: () => ({
    loading: true,
    saving: false
  }),
  computed: {
    object(): Seminar | undefined {
      return this.$store.getters["seminars/byPk"](this.pk);
    }
  },
  async created() {
    this.loading = true;
    try {
      await this.$store.dispatch("seminars/fetchSingle", this.pk);
      (this.$refs.seminarForm as any).copyFields();
    } catch (error) {
      alert("Fehler beim Laden des Seminars");
    } finally {
      this.loading = false;
    }
  }
});
</script>
