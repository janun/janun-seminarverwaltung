import Vue from 'vue';
import { objectCompare } from '@/utils/utils';

export default Vue.extend({
  props: {
    object: { type: Object, required: true }
  },
  data: () => ({
    serverErrors: [],
    form: {}
  }),
  computed: {
    hasChanges(): boolean {
      if (!this.object) {
        return false;
      }
      return Object.entries(this.form).some(
        ([key, formValue]) => !objectCompare(formValue, this.object[key as keyof object])
      );
    }
  },
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
