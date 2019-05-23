<template>
  <div
    class="absolute bottom-0 h-48 mt-16 w-full text-center pb-10 pt-8"
    style="background: rgba(0,0,0,0.03)"
  >
    <h3 class="text-green-500 font-normal text-2xl">
      Hilfe
    </h3>
    <p>Irgendwas geht nicht oder Du hast Fragen?</p>
    <div class="flex flex-col flex-wrap items-center justify-center">
      <a class="mx-1 link" :href="'tel:' + helpPhone">
        Telefon: {{ helpPhone }}
      </a>
      <a class="mx-1 link" :href="'mailto:' + helpMail">
        E-Mail: {{ helpMail }}
      </a>
      <a class="mx-1 link" target="_blank" :href="seminarPolicyURL">
        Download Seminarrichtlinie
      </a>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      helpPhone: '+49 511 3940515',
      helpMail: 'seminar@janun.de',
      seminarPolicyURL: 'https://www.janun.de/downloads'
    }
  }
}
</script>
