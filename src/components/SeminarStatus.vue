<template>
  <b-dropdown :value="value" position="is-bottom-left" aria-role="list">
    <button class="button is-primary" type="button" slot="trigger">
      <span>{{ value }}</span>
      <b-icon icon="menu-down"></b-icon>
    </button>

    <b-dropdown-item v-for="state in statesInfo" :value="state.title" aria-role="listitem">
      {{ state.title }}
    </b-dropdown-item>
  </b-dropdown>
</template>


<script lang="ts">
import Vue from "vue";
import { SeminarStatus, Seminar } from "@/types.ts";

interface StateInfo {
  title: SeminarStatus;
  description: string;
  sources: SeminarStatus[];
  color: string;
}

export default Vue.extend({
  props: {
    value: { type: String as () => SeminarStatus, required: true },
    seminar: { type: Object as () => Seminar, required: true }
  },
  computed: {
    isStaff(): boolean {
      return this.$store.getters["auth/isStaff"];
    },
    statesInfo(): StateInfo[] {
      return [
        {
          title: "angemeldet",
          description: "Das Seminar wurde angemeldet.",
          sources: ["zurückgezogen", "abgesagt"],
          color: "green"
        },
        {
          title: "zurückgezogen",
          description: "Der Antrag auf Förderung wurde zurückgezogen",
          color: "red",
          sources: ["angemeldet", "zugesagt"]
        },
        {
          title: "zugesagt",
          description: "Die Förderung wurde von JANUN zugesagt.",
          color: "green",
          sources: ["angemeldet", "abgelehnt", "abgesagt", "zurückgezogen"],
          visible: this.isStaff
        },
        {
          title: "abgesagt",
          description: "Das Seminar findet nicht statt.",
          color: "red",
          sources: ["zugesagt", "angemeldet"]
        },
        {
          title: "abgelehnt",
          description: "Die Förderung wurde von JANUN abgelehnt.",
          color: "red",
          sources: ["angemeldet", "zugesagt"],
          visible: this.isStaff
        },
        {
          title: "stattgefunden",
          description: "Das Seminar hat tatsächlich stattgefunden.",
          color: "green",
          disabled: new Date(this.seminar.start_date) > new Date(),
          sources: ["zugesagt"],
          tooltip:
            new Date(this.seminar.start_date) > new Date()
              ? "Erst möglich, wenn das Datum in der Vergangenheit liegt"
              : ""
        },
        {
          title: "ohne Abrechnung",
          description: "",
          color: "red",
          sources: ["stattgefunden"],
          visible: this.isStaff
        },
        {
          title: "Abrechnung abgeschickt",
          description: "Die Abrechnung wurde per Post abgeschickt",
          color: "green",
          sources: ["stattgefunden"]
        },
        {
          title: "Abrechnung angekommen",
          description: "Die Abrechnung ist bei JANUN angekommen",
          color: "green",
          visible: this.isStaff,
          sources: ["Abrechnung abgeschickt", "stattgefunden"]
        },
        {
          title: "Abrechnung unmöglich",
          description: "",
          color: "red",
          visible: this.isStaff,
          sources: ["Abrechnung angekommen", "Nachprüfung", "inhaltliche Prüfung"]
        },
        {
          title: "rechnerische Prüfung",
          description: "",
          color: "green",
          visible: this.isStaff,
          sources: ["Abrechnung angekommen"]
        },
        {
          title: "inhaltliche Prüfung",
          description: "",
          color: "green",
          visible: this.isStaff,
          sources: ["rechnerische Prüfung"]
        },
        {
          title: "Nachprüfung",
          description: "",
          color: "green",
          visible: this.isStaff,
          sources: ["inhaltliche Prüfung"]
        },
        {
          title: "fertig geprüft",
          description: "",
          color: "green",
          visible: this.isStaff,
          sources: ["Nachprüfung"]
        },
        {
          title: "überwiesen",
          description: "",
          color: "green",
          visible: this.isStaff,
          sources: ["fertig geprüft"]
        }
      ];
    }
  }
});
</script>
