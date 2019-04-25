import Vue from 'vue';

let uuid = 0;

export default Vue.extend({
  beforeCreate() {
    (this as any).uuid = uuid.toString();
    uuid += 1;
  }
});
