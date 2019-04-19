import Vue from "vue";

import { User } from "@/types";

export default Vue.extend({
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
