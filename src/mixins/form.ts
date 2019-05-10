import Vue from 'vue';

export default Vue.extend({
  props: {
    object: { type: Object, required: true }
  },
  data: () => ({
    serverErrors: [],
    form: {}
  }),
  methods: {
    setServerErrors(data: any) {
      this.serverErrors = [].concat.apply([], Object.values(data));
    },
    copyFields(): void {
      this.$v.$reset();
      if (!this.object) {
        return;
      }
      Object.keys(this.form).forEach((key) => Vue.set(this.form, key, this.object[key]));
    }
  }
});
