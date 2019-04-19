<template>
  <FormGroup :labelFor="'input_' + uuid" :validator="validator" :label="label">
    <BFormInput
      :id="'input_' + uuid"
      slot-scope="{ attrs, listeners }"
      v-bind="{ ...attrs, ...$attrs }"
      v-on="listeners"
      :value="value"
      @input="onInput"
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
    value: { type: [String, Number], default: "" }
  },
  methods: {
    onInput(value: string) {
      this.$emit("input", value);
    }
  }
});
</script>
