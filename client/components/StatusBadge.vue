<template>
  <span
    class="badge"
    :class="{
      'bg-green-200': stateInfo.color === 'green',
      'bg-red-200': stateInfo.color === 'red',
      'bg-yellow-200': stateInfo.color === 'yellow'
    }"
  >
    {{ value }}
  </span>
</template>

<script>
import { getStateInfo } from '../utils/status'

export default {
  props: {
    value: { type: String, required: true }
  },
  computed: {
    stateInfo() {
      return getStateInfo(this.value)
    }
  }
}
</script>
