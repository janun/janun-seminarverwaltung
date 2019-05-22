<template>
  <div v-if="$auth.user">
    <h2 class="text-gray-800 font-bold text-xl mb-3 mt-10">Deine Gruppen</h2>
    <div v-if="noGroupAccess" class="mb-4 max-w-sm text-red-500">
      Dein Konto wurde noch nicht überprüft, deswegen
      <strong>kannst Du noch keine Gruppenseiten besuchen.</strong>
    </div>
    <div v-if="$auth.user.janun_groups.length" class="flex flex-wrap -m-4">
      <div
        v-for="group in $auth.user.janun_groups"
        :key="group.pk"
        class="lg:w-1/3 sm:w-1/2 w-full p-4"
      >
        <nuxt-link
          class="seminar block bg-white rounded shadow hover:shadow-md p-4 no-underline flex flex-col"
          style="min-height: 75px;"
          :to="`/groups/${group.pk}`"
        >
          <h3 class="mt-1 mb-2 leading-tight text-gray-800">
            {{ group.name }}
          </h3>
        </nuxt-link>
      </div>
    </div>
    <div v-else>
      <p>Du bist nicht Mitglied in irgendwelchen JANUN-Gruppen.</p>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    noGroupAccess() {
      return this.$auth.user.janun_groups.length && !this.$auth.user.is_reviewed
    }
  }
}
</script>
