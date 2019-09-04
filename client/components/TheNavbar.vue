<template>
  <nav class="bg-white shadow-md px-4">
    <div class="mx-auto max-w-5xl flex justify-start items-stretch h-16">
      <nuxt-link to="/" class="flex items-center">
        <svg width="38" height="38" class="fill-current text-green-500">
          <path
            d="M34.9 28.3c.2-.1.4.2.3.6-.1.4-.3.7-.5.8-.3.1-.4-.2-.4-.5v-.1l-1.7-1C32 29.4 30 31 29 31.7l-.6.4.6-.4c2.5-1.9 4.5-5.4 3.4-8-1-2.4-4.6-3.5-7.1-1.1-6.9 6.7 1.8 9.2 4.4 5.9 2.7-3.5-1.3-6-2.8-2.6-.3.6 0 1 .5 1.1 0-.1-.1-.3 0-.4.1-.6.6-1.1 1.1-1.1.5 0 .9.4.8 1l-.2.6-.2.2c-1.5 1.6-4.9.1-1.8-3 2.4-2.4 5.9.8 3.1 4.7a5 5 0 0 1-6.4 1.3c-1.8.7-4 3-4.7 3.5l.1.4c0 .7-.9 1.5-1.9 1.9-1.1.4-2.1.1-2.1-.7 0-.8 1-1.7 2.2-2l.8-.1c.9-.8 4.4-3.4 4.2-4.3-.5-.8-.8-1.8-.6-3-2-2.6-10.8-6.2-12.6-7.3-.8.5-2 .7-3.5.5-2.8-.4-5.5-2-5.6-3.8-.1-1.7 2.4-2.5 5.4-1.8 2.6.7 4.5 2.3 4.5 3.7v.3c2.1.7 10.3 4.8 13.6 4.9l.8-.8c.5-.4 1-.8 1.6-1-.5-3.5-4.8-12.1-6.1-15l-.2-.1c-1.5-.9-2.8-2.9-2.7-4.2C17 0 18.4-.1 19.9 1c1.4 1.1 2.4 2.8 2.3 4l-.2.6h.1c.3.1 4.5 12.4 6.4 14.6.6 0 1.1.2 1.6.3 1.3-1.9 2.3-6.9 2.6-8.2l-.1-.8c.1-.7.5-1 1-.6.4.4.7 1.2.6 1.8-.1.5-.3.8-.6.8-.3 1.1-1.7 4.9-1.8 8 .4.3.7.7.9 1.1l3.7-2.4v-.3c.1-.5.4-.8.6-.7.3.1.4.6.3 1-.1.5-.3.8-.6.7l-.2-.1c-.7.6-3.1 2.3-3.4 3.1.2 1 .1 2.1-.2 3.1l1.7 1.3.2-.1"
          />
        </svg>
        <span class="ml-2 text-green-500 font-bold">Seminare</span>
      </nuxt-link>

      <div
        v-if="$auth.loggedIn && $auth.user.has_staff_role"
        class="sm:ml-10 flex"
      >
        <nuxt-link class="mx-2 flex items-center" to="/seminars/">
          Seminare
          <span
            v-if="$auth.user.has_verwalter_role && pendingSeminars > 0"
            class="relative flex items-center justify-center font-bold w-4 h-4 leading-none text-xs p-1 rounded-full bg-yellow-300 text-gray-700 shadow"
            style="top: -10px"
            :title="`${pendingSeminars} (neu) angemeldete Seminare`"
          >
            {{ pendingSeminars }}
          </span>
        </nuxt-link>
        <nuxt-link class="mx-2 flex items-center" to="/users/">
          Kontos
          <span
            v-if="$auth.user.has_verwalter_role && pendingAccounts > 0"
            class="relative flex items-center justify-center font-bold w-4 h-4 leading-none text-xs p-1 rounded-full bg-red-300 text-gray-700 shadow"
            style="top: -10px"
            :title="`${pendingAccounts} ungeprüfte Konten`"
          >
            {{ pendingAccounts }}
          </span>
        </nuxt-link>
        <nuxt-link class="mx-2 flex items-center" to="/groups/">
          Gruppen
        </nuxt-link>
      </div>

      <div v-if="$auth.loggedIn" class="ml-auto flex">
        <nuxt-link class="mx-2 flex items-center" to="/profile">
          {{ $auth.user.username }}
        </nuxt-link>
        <button class="mx-2 flex items-center" @click="logout">
          Logout
        </button>
      </div>

      <div v-if="!$auth.loggedIn" class="ml-auto flex">
        <nuxt-link class="mx-2 flex items-center" to="/login">
          Anmelden
        </nuxt-link>
        <nuxt-link class="mx-2 flex items-center" to="/signup">
          Konto Anlegen
        </nuxt-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  // data() {
  //   return {
  //     pendingSeminars: 0,
  //     pendingAccounts: 0
  //   }
  // },
  computed: {
    pendingSeminars() {
      return this.$store.state.seminars.seminars.filter(
        seminar => seminar.status === 'angemeldet'
      ).length
    },
    pendingAccounts() {
      return this.$store.state.users.users.filter(
        user => user.is_reviewed === false
      ).length
    }
  },
  // async created() {
  //   if (this.$auth.user.has_verwalter_role) {
  //     const data = await this.$axios.$get('/seminars/?status=angemeldet')
  //     this.pendingSeminars = data.length

  //     const data2 = await this.$axios.$get('/users/?is_reviewed=False')
  //     this.pendingAccounts = data2.length
  //   }
  // },
  methods: {
    async logout() {
      await this.$auth.logout()
      await this.$router.push('/login')
    }
  }
}
</script>

<style lang="postcss" scoped>
.nuxt-link-active {
  @apply font-bold text-green-500;
}
</style>
