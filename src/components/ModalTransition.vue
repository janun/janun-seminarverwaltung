<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  functional: true,
  render(createElement, context) {
    const data = {
      props: {
        name: 'modal',
        mode: 'out-in'
      }
    };
    return createElement('transition', data, context.children);
  }
});
</script>

<style lang="postcss">
/* modal transition */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.2s;
}

.modal {
  transition: all 0.2s;
}

.modal-enter .modal,
.modal-leave-to .modal {
  transform: scale(0.7);
}

.modal-enter,
.modal-leave-to {
  opacity: 0;
}
</style>
