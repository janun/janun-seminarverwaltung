<template>
  <div class="container">
    <div class="box" style="max-width: 320px">
      <h1 class="title">Login</h1>
      <form @submit.prevent="login">
        <b-field label="Benutzername">
          <b-input ref="username" v-model="form.username" />
        </b-field>
        <b-field label="Passwort">
          <b-input v-model="form.password" type="password" />
        </b-field>

        <b-button
          native-type="submit"
          variant="primary"
          :disabled="!form.username || !form.password || loading"
        >
          <b-spinner small v-if="loading" label="Loading..."></b-spinner>
          Login
        </b-button>
      </form>
    </div>
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
