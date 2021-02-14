import Vue from 'vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import 'default-passive-events'
import VueLazyload from 'vue-lazyload'

Vue.use(ElementUI)
Vue.use(VueLazyload)
Vue.directive('title', {
  inserted: function (el) {
    document.title = el.dataset.title
  }
})
Vue.config.productionTip = false

import App from './App.vue'

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
