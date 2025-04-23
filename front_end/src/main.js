import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueAMap from 'vue-amap'; // 引入vue-amap库
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import * as echarts from 'echarts';
import 'echarts-gl';

Vue.config.productionTip = false
// 初始化vue-amap
Vue.use(VueAMap);
VueAMap.initAMapApiLoader({
  key: 'aca19a4ead9cdf2e6676cca82f0a3065',
  plugin: [
    'AMap.Heatmap', // 高德地图热力图插件
    'Amap.Geolocation',
  ],
});
Vue.prototype.$echarts = echarts
Vue.use(ElementUI);
new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')
