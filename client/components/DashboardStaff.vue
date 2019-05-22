<template>
  <div class="mx-auto max-w-5xl">
    <h1 class="font-bold text-2xl text-green-500">
      Willkommen, {{ $auth.user.name }}!
    </h1>

    <GroupCardList />

    <SeminarCardList />
  </div>
</template>

<script>
import SeminarCardList from '@/components/SeminarCardList.vue'
import GroupCardList from '@/components/GroupCardList.vue'

export default {
  components: {
    SeminarCardList,
    GroupCardList
  }
}
</script>
