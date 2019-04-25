<template>
  <div class="container mx-auto px-4">
    <BaseWizard>
      <BaseWizardStep title="Test1">
        Test 1
      </BaseWizardStep>

      <BaseWizardStep title="Test2">
        Test 2
      </BaseWizardStep>
    </BaseWizard>
  </div>
</template>


<script lang="ts">
import Vue from 'vue';
import BaseWizard from '@/components/BaseWizard.vue';
import BaseWizardStep from '@/components/BaseWizardStep.vue';

export default Vue.extend({
  components: { BaseWizard, BaseWizardStep }
});
</script>
