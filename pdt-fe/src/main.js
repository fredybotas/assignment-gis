import Vue from 'vue'
import App from './App.vue'
import VueResource from 'vue-resource';
import BootstrapVue from 'bootstrap-vue'


Vue.config.productionTip = false;
Vue.use(VueResource);
Vue.use(BootstrapVue);

new Vue({
  render: h => h(App),
}).$mount('#app')
