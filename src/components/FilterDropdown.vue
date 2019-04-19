<template>
  <BDropdown class="m-md-2" :variant="active ? 'secondary' : 'outline-secondary'">
    <template slot="button-content">
      {{ label }}:
      <span v-if="!active">Alle</span>
      <span class="d-inline-flex" style="font-size: 0.9rem;" v-else>
        {{ value.slice(0, 3).join(", ") }}
        <template v-if="value.length > 3">
          , …
        </template>
      </span>
    </template>
    <BDropdownForm>
      <BFormCheckboxGroup stacked :checked="value" :name="label" @input="onInput">
        <BFormCheckbox class="text-nowrap" v-for="option in options" :key="option" :value="option">
          {{ option }}
        </BFormCheckbox>
      </BFormCheckboxGroup>
    </BDropdownForm>
  </BDropdown>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  props: {
    label: { type: String, required: true },
    value: { type: Array as () => string[], required: true },
    options: { type: Array as () => string[], required: true }
  },
  methods: {
    onInput(selectedValues: string[]) {
      this.$emit("input", selectedValues);
    }
  },
  computed: {
    active(): boolean {
      return this.value.length !== 0;
    }
  }
});
</script>
