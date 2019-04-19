<template>
  <b-navbar toggleable="lg" class="shadow mb-5">
    <b-navbar-brand to="/">
      <svg width="38" height="38">
        <path
          fill="#3a9d00"
          d="M34.9 28.3c.2-.1.4.2.3.6-.1.4-.3.7-.5.8-.3.1-.4-.2-.4-.5v-.1l-1.7-1C32 29.4 30 31 29 31.7l-.6.4.6-.4c2.5-1.9 4.5-5.4 3.4-8-1-2.4-4.6-3.5-7.1-1.1-6.9 6.7 1.8 9.2 4.4 5.9 2.7-3.5-1.3-6-2.8-2.6-.3.6 0 1 .5 1.1 0-.1-.1-.3 0-.4.1-.6.6-1.1 1.1-1.1.5 0 .9.4.8 1l-.2.6-.2.2c-1.5 1.6-4.9.1-1.8-3 2.4-2.4 5.9.8 3.1 4.7a5 5 0 0 1-6.4 1.3c-1.8.7-4 3-4.7 3.5l.1.4c0 .7-.9 1.5-1.9 1.9-1.1.4-2.1.1-2.1-.7 0-.8 1-1.7 2.2-2l.8-.1c.9-.8 4.4-3.4 4.2-4.3-.5-.8-.8-1.8-.6-3-2-2.6-10.8-6.2-12.6-7.3-.8.5-2 .7-3.5.5-2.8-.4-5.5-2-5.6-3.8-.1-1.7 2.4-2.5 5.4-1.8 2.6.7 4.5 2.3 4.5 3.7v.3c2.1.7 10.3 4.8 13.6 4.9l.8-.8c.5-.4 1-.8 1.6-1-.5-3.5-4.8-12.1-6.1-15l-.2-.1c-1.5-.9-2.8-2.9-2.7-4.2C17 0 18.4-.1 19.9 1c1.4 1.1 2.4 2.8 2.3 4l-.2.6h.1c.3.1 4.5 12.4 6.4 14.6.6 0 1.1.2 1.6.3 1.3-1.9 2.3-6.9 2.6-8.2l-.1-.8c.1-.7.5-1 1-.6.4.4.7 1.2.6 1.8-.1.5-.3.8-.6.8-.3 1.1-1.7 4.9-1.8 8 .4.3.7.7.9 1.1l3.7-2.4v-.3c.1-.5.4-.8.6-.7.3.1.4.6.3 1-.1.5-.3.8-.6.7l-.2-.1c-.7.6-3.1 2.3-3.4 3.1.2 1 .1 2.1-.2 3.1l1.7 1.3.2-.1"
        />
      </svg>
      Seminare
    </b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav v-if="isStaff">
        <b-nav-item to="/seminare">Seminare</b-nav-item>
        <b-nav-item to="/users">Benutzer_innen</b-nav-item>
        <b-nav-item to="/groups">Gruppen</b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav v-if="isAuthenticated" class="ml-auto">
        <b-nav-item to="/profile">{{ user.username }}</b-nav-item>
        <b-nav-item @click="logout">Logout</b-nav-item>
      </b-navbar-nav>
      <b-navbar-nav v-else class="ml-auto">
        <b-nav-item to="/login">Login</b-nav-item>
        <b-nav-item to="/signup">Signup</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script lang="ts">
import Vue from "vue";
import { User, UserRole } from "@/types";

export default Vue.extend({
  methods: {
    logout() {
      this.$store.dispatch("auth/logout");
    }
  },
  computed: {
    user(): User {
      return this.$store.getters["auth/user"];
    },
    isAuthenticated(): boolean {
      return this.$store.getters["auth/isAuthenticated"];
    },
    isStaff(): boolean {
      return this.$store.getters["auth/isStaff"];
    }
  }
});
</script>
