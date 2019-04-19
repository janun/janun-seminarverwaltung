<template>
  <FormGroup :validator="validator" :label="label" :labelFor="'input_' + uuid">
    <b-form-textarea
      :id="'input_' + uuid"
      slot-scope="{ attrs, listeners }"
      v-bind="attrs"
      v-on="listeners"
      :value="value"
      @input="onInput"
      rows="3"
      max-rows="8"
    />
  </FormGroup>
</template>

<script lang="ts">
import Vue from "vue";
import { Validation } from "vuelidate";
import uuidMixin from "@/mixins/uuid.ts";

export default Vue.extend({
  mixins: [uuidMixin],
  props: {
    validator: { type: Object as () => Validation, default: undefined },
    label: { type: String, default: "" },
    value: { type: String, default: "" }
  },
  methods: {
    onInput(value: string) {
      this.$emit("input", value);
    }
  }
});
</script>
