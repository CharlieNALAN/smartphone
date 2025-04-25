import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
	state: {
		userLocation: null // 初始值为null，而不是固定坐标
	},
	mutations: {
		setUserLocation(state, location) {
			state.userLocation = location;
		}
	},
	actions: {
		// 获取一次用户位置
		async getUserLocation({
			commit
		}) {
			try {
				const res = await uni.getLocation({
					type: 'gcj02',
					success: (res) => {
						console.log('获取位置成功:', res);
						const userLocation = {
							latitude: res.latitude,
							longitude: res.longitude
						};
						commit('setUserLocation', userLocation);
						return userLocation;
					},
					fail: (err) => {
						console.error('获取位置失败:', err);
						// 失败时尝试使用默认位置
						if (!this.state.userLocation) {
							const defaultLocation = {
								latitude: 22.280121,
								longitude: 114.142718
							};
							commit('setUserLocation', defaultLocation);
						}
					}
				});
			} catch (err) {
				console.error('Failed to get user location:', err);
			}
		},
		
		// 开始监听用户位置变化
		startLocationWatch({ commit }) {
			// 先获取一次当前位置
			this.dispatch('getUserLocation');
			
			// 开始监听位置变化
			this.locationWatcherId = uni.onLocationChange((res) => {
				console.log('位置变化:', res);
				const userLocation = {
					latitude: res.latitude,
					longitude: res.longitude
				};
				commit('setUserLocation', userLocation);
			});
		},
		
		// 停止监听位置
		stopLocationWatch() {
			if (this.locationWatcherId) {
				uni.offLocationChange(this.locationWatcherId);
				this.locationWatcherId = null;
			}
		}
	}
})

// 在APP启动时开始监听位置
uni.getSystemInfo({
	success: function(res) {
		// 确保是在真机环境才开始监听位置
		if (res.platform !== 'devtools') {
			setTimeout(() => {
				store.dispatch('startLocationWatch');
			}, 1000);
		}
	}
});

export default store
