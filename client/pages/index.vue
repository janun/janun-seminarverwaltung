<template>
  <div>
    <h1 class="font-bold text-2xl text-green-500">
      Willkommen, {{ $auth.user.name }}!
    </h1>

    <nuxt-link class="my-5 btn btn-primary" to="/seminars/apply">
      Seminar anmelden
    </nuxt-link>

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
  }
}
</script>
