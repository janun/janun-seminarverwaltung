<template>
  <div>
    <DashboardStaff v-if="$auth.user.has_staff_role" />
    <DashboardTeamer v-else />
  </div>
</template>

<script>
import DashboardTeamer from '@/components/DashboardTeamer'
import DashboardStaff from '@/components/DashboardStaff'

export default {
  components: {
    DashboardTeamer,
    DashboardStaff
  },
  head() {
    return {
      title: 'Übersicht'
    }
  }
}
</script>
