<template>
  <BDropdown>
    <button class="button" slot="trigger">
      <div>
        {{ label }}:
        <span v-if="value.length === 0 || value.length === options.length">Alle</span>
        <span v-else>
          {{ value.slice(0, 3).join(", ") }}
          <template v-if="value.length > 3">
            , …
          </template>
        </span>
      </div>
      <b-icon icon="menu-down"></b-icon>
    </button>

    <BDropdownItem custom v-for="option in options" :key="option">
      <BCheckbox v-model="selectedValues" @input="onInput" :native-value="option">
        <span style="white-space: nowrap">{{ option }}</span>
      </BCheckbox>
    </BDropdownItem>
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
  data() {
    return {
      selectedValues: this.value
    };
  },
  watch: {
    value(value) {
      this.selectedValues = value;
    }
  },
  methods: {
    onInput() {
      this.$emit("input", this.selectedValues);
    }
  }
});
</script>
