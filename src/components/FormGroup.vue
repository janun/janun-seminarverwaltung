<template>
  <b-field
    :horizontal="horizontal"
    :label="label"
    :custom-class="customClass"
    :type="type"
    :message="[message, firstErrorMessage]"
    :label-for="labelFor"
  >
    <slot />
  </b-field>
</template>

<script lang="ts">
import Vue from "vue";
import { singleErrorExtractorMixin } from "vuelidate-error-extractor";

export default Vue.extend({
  extends: singleErrorExtractorMixin,
  props: {
    horizontal: { type: Boolean, default: false },
    labelFor: { type: String, default: "" },
    message: { type: String, default: "" }
  },
  computed: {
    type(): string | null {
      return (this as any).hasErrors ? "is-danger" : (this as any).isValid ? "is-success" : null;
    },
    customClass(): string | null {
      return (this as any).hasErrors
        ? "has-text-danger"
        : (this as any).isValid
        ? "has-text-success"
        : null;
    }
  }
});
</script>