import App from './App'
import store from './store'
import { startLocationTimer } from './utils/location.js'
// #ifndef VUE3
import Vue from 'vue'
import VueCompositionApi from '@vue/composition-api'
import uView from "uview-ui";
Vue.use(uView);
 
Vue.use(VueCompositionApi)
Vue.config.productionTip = false
App.mpType = 'app'

try {
	function isPromise(obj) {
		return (
			!!obj &&
			(typeof obj === "object" || typeof obj === "function") &&
			typeof obj.then === "function"
		);
	}

	// 统一 vue2 API Promise 化返回格式与 vue3 保持一致
	uni.addInterceptor({
		returnValue(res) {
			if (!isPromise(res)) {
				return res;
			}
			return new Promise((resolve, reject) => {
				res.then((res) => {
					if (res[0]) {
						reject(res[0]);
					} else {
						resolve(res[1]);
					}
				});
			});
		},
	});
} catch (error) {}

const app = new Vue({
	...App,
	store
})
app.$mount()
// startLocationTimer()
// #endif

// #ifdef VUE3
import {
	createSSRApp
} from 'vue'
export function createApp() {
	const app = createSSRApp(App)
	return {
		app
	}
}
// #endif

// 检查授权状态
// app.globalData.checkLocationPermission = async function() {
// 	const res = await uni.authorize({
// 		scope: 'scope.userLocation'
// 	});
// 	if (res.authResult === 'granted') {
// 		// 用户已授权
// 		this.globalData.isLocationAuthorized = true;
// 		this.startLocationUpdates();
// 	} else if (res.authResult === 'denied') {
// 		// 用户拒绝授权
// 		uni.showModal({
// 			title: '位置授权提示',
// 			content: '未授权位置信息将无法使用本小程序完整功能',
// 			showCancel: false,
// 			success: function(res) {
// 				if (res.confirm) {
// 					// 用户点击确认，重新引导授权
// 					uni.openSetting({
// 						success: function(res) {
// 							if (res.authSetting['scope.userLocation']) {
// 								// 用户已开启授权，可以执行相关操作
// 								this.globalData.isLocationAuthorized = true;
// 								this.startLocationUpdates();
// 							}
// 						}
// 					});
// 				}
// 			}
// 		});
// 	}
// }

// // 开始获取位置信息
// app.globalData.startLocationUpdates = function() {
// 	if (this.timer) {
// 		clearInterval(this.timer);
// 	}
// 	this.timer = setInterval(async () => {
// 		const location = await uni.getLocation({
// 			type: 'gcj02'
// 		});
// 		if (location) {
// 			// 处理位置信息
// 			console.log(location);
// 		}
// 	}, 60000); // 每隔5秒获取一次位置信息
// }

// // 在App启动时执行
// app.onLaunch = function() {
// 	// 展示本地存储能力
// 	const logs = uni.getStorageSync('logs') || []
// 	logs.unshift(Date.now())
// 	uni.setStorageSync('logs', logs)

// 	// 调用函数检查位置授权状态
// 	this.globalData.checkLocationPermission();
// }


import TabBar from "./components/TabBar.vue"
Vue.component('TabBar', TabBar);