import Vue from 'vue';
import { Toast } from '@/types.ts';

declare module 'vue/types/vue' {
  interface Vue {
    $toast: (text: string, options?: Toast) => void;
  }
}
