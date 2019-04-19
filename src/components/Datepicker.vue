<template>
  <b-datepicker
    :date-parser="parseDate"
    :value="dateValue"
    @input="onInput"
    icon="calendar-today"
    editable
  ></b-datepicker>
</template>

<script lang="ts">
// TODO: Lots of problems with this datepicker:
//  * submits form accidentally
//  * starts with touched validator
//  * needs multi clicks to select date
//  * emits one day before entered value
import Vue from "vue";

export default Vue.extend({
  props: {
    value: { type: String, default: "" }
  },
  methods: {
    onInput(dateValue: Date) {
      this.$emit("input", dateValue.toISOString().split("T")[0]);
    },
    parseDate(input: string): Date | undefined {
      const parts = input.match(/(\d+)/g);
      if (!parts) {
        return undefined;
      }
      return new Date(parseInt(parts[2], 10), parseInt(parts[1], 10) - 1, parseInt(parts[0], 10));
    }
  },
  computed: {
    dateValue(): Date | undefined {
      return this.value ? new Date(this.value) : undefined;
    }
  }
});
</script>
