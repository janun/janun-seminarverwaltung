<template>
  <BaseSelect
    :value="value"
    :options="options"
    @input="$emit('input', $event)"
  />
</template>

<script>
import BaseSelect from '@/components/forms/BaseSelect.vue'
import { getNextStates } from '@/utils/status.js'

export default {
  components: {
    BaseSelect
  },
  props: {
    value: { type: String, required: true },
    seminar: { type: Object, required: true }
  },
  computed: {
    options() {
      return [
        this.seminar.status,
        ...getNextStates(this.seminar.status, this.$auth.user.has_staff_role)
      ]
    }
  }
}
</script>
