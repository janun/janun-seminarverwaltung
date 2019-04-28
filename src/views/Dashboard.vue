<script lang="ts">
import Vue from 'vue';
import store from '@/store/index.ts';
import DashboardTeamer from '@/views/DashboardTeamer.vue';
import DashboardStaff from '@/views/DashboardStaff.vue';

export default Vue.extend({
  functional: true,
  render(h) {
    const isStaff = store.getters['auth/isStaff'];
    if (isStaff) {
      return h(DashboardStaff);
    } else {
      return h(DashboardTeamer);
    }
  }
});
</script>
