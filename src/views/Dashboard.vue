<script lang="ts">
import Vue from 'vue';
import store from '@/store/index.ts';
import TeamerDashboard from '@/views/TeamerDashboard.vue';
import StaffDashboard from '@/views/StaffDashboard.vue';

export default Vue.extend({
  functional: true,
  render(h) {
    const isStaff = store.getters['auth/isStaff'];
    if (isStaff) {
      return h(StaffDashboard);
    } else {
      return h(TeamerDashboard);
    }
  }
});
</script>
