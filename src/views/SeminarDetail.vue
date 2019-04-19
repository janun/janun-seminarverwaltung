<template>
  <div>
    <BSpinner v-if="loading" class="align-middle mr-2"></BSpinner>
    <div class="container" v-if="object">
      <h1>{{ object.title }}</h1>

      <div class="mb-4">
        Am {{ object.start_date | date }}
        <span v-if="object.location">in {{ object.location }}</span>
      </div>

      <div class="text-grey-darker text-sm">
        <div>
          angemeldet von
          <b-link :to="{ name: 'UserDetail', params: { pk: object.owner.pk } }">
            {{ object.owner.name }}
          </b-link>
          am {{ object.created_at | date }}
          <br />
          geändert am {{ object.updated_at | date }}
        </div>
        <div v-if="object.group">
          Gruppe:
          <b-link :to="{ name: 'GroupDetail', params: { pk: object.group.pk } }">
            {{ object.group.name }}
          </b-link>
        </div>
      </div>

      <hr />

      <SeminarForm ref="seminarForm" :saving="saving" :object="object" @submit="save" />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Seminar } from "@/types";

import SeminarForm from "@/components/SeminarForm.vue";

export default Vue.extend({
  components: {
    SeminarForm
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
  methods: {
    async save(formData: Seminar) {
      this.saving = true;
      try {
        await this.$store.dispatch("seminars/update", {
          pk: this.pk,
          data: formData
        });
        (this.$refs.seminarForm as any).copyFields();
        this.$store.commit("alerts/add", {
          variant: "success",
          text: "Änderungen am Seminar  gespeichert."
        });
      } catch (error) {
        alert("Fehler beim Speichern des Seminars.");
      }
      this.saving = false;
    }
  },
  async created() {
    this.loading = true;
    try {
      await this.$store.dispatch("seminars/fetchSingle", this.pk);
      (this.$refs.seminarForm as any).copyFields();
    } catch (error) {
      this.$store.commit("alerts/add", {
        variant: "danger",
        text: "Seminar konnte nicht geladen werden."
      });
    } finally {
      this.loading = false;
    }
  }
});
</script>
