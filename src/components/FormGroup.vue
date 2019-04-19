<template>
  <BFormGroup
    :invalid-feedback="firstErrorMessage"
    :state="isValid"
    :label="label"
    :labelFor="labelFor"
  >
    <slot :attrs="{ state: isValid }" :listeners="{ input: () => preferredValidator.$touch() }" />
  </BFormGroup>
</template>

<script lang="ts">
import { singleErrorExtractorMixin } from "vuelidate-error-extractor";

export default {
  name: "FormGroup",
  extends: singleErrorExtractorMixin,
  props: {
    labelFor: { type: String, default: "" }
  }
};
</script>