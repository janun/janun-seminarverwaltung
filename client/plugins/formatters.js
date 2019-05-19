import Vue from 'vue'
import {
  formatDate,
  formatEuro,
  formatNumber,
  formatDatetime
} from '@/utils/formatters.js'

Vue.filter('date', value => (value ? formatDate(value) : ''))
Vue.filter('datetime', value => (value ? formatDatetime(value) : ''))
Vue.filter('euro', formatEuro)
Vue.filter('number', formatNumber)
