<template>
  <div>
    <b-alert
      v-for="(alert, index) in alerts"
      :key="alert.id"
      :variant="alert.variant"
      show="10"
      fade
      dismissible
      @dismissed="deleteAlert(alert)"
    >
      {{ alert.text }}
    </b-alert>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { Alert } from "@/types";

export default Vue.extend({
  computed: {
    alerts(): Alert[] {
      return this.$store.getters["alerts/all"];
    }
  },
  methods: {
    deleteAlert(alert: Alert) {
      this.$store.commit("alerts/delete", alert.id);
    }
  }
});
</script>
