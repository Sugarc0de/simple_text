import Vue from 'vue'
import { Button, Slider } from 'element-ui'
import App from './App.vue'

Vue.config.productionTip = false

Vue.use(Button)
Vue.use(Slider)

new Vue({
  render: h => h(App),
}).$mount('#app')
