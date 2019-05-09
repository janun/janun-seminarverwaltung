<template>
  <div class="mx-auto px-4 max-w-5xl">
    <h1 class="text-3xl text-green-500 font-bold">Profil</h1>
    <UserForm :object="user" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import UserForm from '@/components/UserForm.vue';
import userMixin from '@/mixins/user.ts';

export default Vue.extend({
  components: {
    UserForm
  },
  mixins: [userMixin]
});
</script>
