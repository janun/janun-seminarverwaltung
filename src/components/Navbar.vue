<template>
  <nav class="navbar has-shadow" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" to="/">
        <svg width="38" height="38">
          <path
            fill="#3a9d00"
            d="M34.9 28.3c.2-.1.4.2.3.6-.1.4-.3.7-.5.8-.3.1-.4-.2-.4-.5v-.1l-1.7-1C32 29.4 30 31 29 31.7l-.6.4.6-.4c2.5-1.9 4.5-5.4 3.4-8-1-2.4-4.6-3.5-7.1-1.1-6.9 6.7 1.8 9.2 4.4 5.9 2.7-3.5-1.3-6-2.8-2.6-.3.6 0 1 .5 1.1 0-.1-.1-.3 0-.4.1-.6.6-1.1 1.1-1.1.5 0 .9.4.8 1l-.2.6-.2.2c-1.5 1.6-4.9.1-1.8-3 2.4-2.4 5.9.8 3.1 4.7a5 5 0 0 1-6.4 1.3c-1.8.7-4 3-4.7 3.5l.1.4c0 .7-.9 1.5-1.9 1.9-1.1.4-2.1.1-2.1-.7 0-.8 1-1.7 2.2-2l.8-.1c.9-.8 4.4-3.4 4.2-4.3-.5-.8-.8-1.8-.6-3-2-2.6-10.8-6.2-12.6-7.3-.8.5-2 .7-3.5.5-2.8-.4-5.5-2-5.6-3.8-.1-1.7 2.4-2.5 5.4-1.8 2.6.7 4.5 2.3 4.5 3.7v.3c2.1.7 10.3 4.8 13.6 4.9l.8-.8c.5-.4 1-.8 1.6-1-.5-3.5-4.8-12.1-6.1-15l-.2-.1c-1.5-.9-2.8-2.9-2.7-4.2C17 0 18.4-.1 19.9 1c1.4 1.1 2.4 2.8 2.3 4l-.2.6h.1c.3.1 4.5 12.4 6.4 14.6.6 0 1.1.2 1.6.3 1.3-1.9 2.3-6.9 2.6-8.2l-.1-.8c.1-.7.5-1 1-.6.4.4.7 1.2.6 1.8-.1.5-.3.8-.6.8-.3 1.1-1.7 4.9-1.8 8 .4.3.7.7.9 1.1l3.7-2.4v-.3c.1-.5.4-.8.6-.7.3.1.4.6.3 1-.1.5-.3.8-.6.7l-.2-.1c-.7.6-3.1 2.3-3.4 3.1.2 1 .1 2.1-.2 3.1l1.7 1.3.2-.1"
          />
        </svg>
        <span class="has-text-primary">Seminarverwaltung</span>
      </a>

      <a
        role="button"
        class="navbar-burger burger"
        aria-label="menu"
        aria-expanded="false"
        data-target="navbarBasicExample"
        @click="mobileActive = !mobileActive"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <div id="navbarBasicExample" class="navbar-menu" :class="{ 'is-active': mobileActive }">
      <div class="navbar-start" v-if="isAuthenticated">
        <router-link exact active-class="is-active" class="navbar-item" to="/">
          Übersicht
        </router-link>
        <router-link active-class="is-active" class="navbar-item" to="/seminare">
          Seminare
        </router-link>
        <router-link active-class="is-active" class="navbar-item" to="/groups">
          Gruppen
        </router-link>
        <router-link active-class="is-active" class="navbar-item" to="/users">
          Benutzer_innen
        </router-link>
      </div>

      <div class="navbar-end" v-if="isAuthenticated">
        <router-link class="navbar-item" to="/profile">{{ user.username }}</router-link>
        <div class="navbar-item">
          <div class="buttons">
            <button @click="logout" class="button">Logout</button>
          </div>
        </div>
      </div>
      <div class="navbar-end" v-else>
        <router-link class="navbar-item" to="/login">Login</router-link>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
import Vue from "vue";
import { User, UserRole } from "@/types";
import userMixin from "@/mixins/user.ts";

export default Vue.extend({
  mixins: [userMixin],
  data: () => ({
    mobileActive: false
  }),
  methods: {
    logout() {
      this.$store.dispatch("auth/logout");
    }
  }
});
</script>
