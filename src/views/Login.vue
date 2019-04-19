<template>
  <div class="mx-auto" style="max-width: 320px">
    <h1>Login</h1>
    <b-form @submit.prevent="login">
      <b-form-group label="Benutzername" label-for="username">
        <b-form-input ref="username" id="username" v-model="form.username" />
      </b-form-group>
      <b-form-group label="Passwort" label-for="password">
        <b-form-input id="password" v-model="form.password" type="password" />
      </b-form-group>
      <b-button
        type="submit"
        variant="primary"
        :disabled="!form.username || !form.password || loading"
      >
        <b-spinner small v-if="loading" label="Loading..."></b-spinner>
        Login
      </b-button>
    </b-form>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  data: () => ({
    loading: false,
    form: {
      username: "",
      password: ""
    }
  }),
  methods: {
    async login() {
      this.loading = true;
      try {
        await this.$store.dispatch("auth/login", this.form);
        this.$router.push("/");
      } catch (e) {
        alert("Anmelden fehlgeschlagen");
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    (this.$refs.username as HTMLInputElement).focus();
  }
});
</script>
