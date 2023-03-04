import Vue from 'vue'
import App from './App.vue'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import axios from 'axios';
import router from "@/router";


Vue.use(Buefy);
Vue.use(router);
Vue.prototype.$http = axios

Vue.config.productionTip = false


new Vue({
  render: h => h(App),
  router
}).$mount('#app')
