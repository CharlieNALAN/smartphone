import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		userLocation: {
			latitude: '30.244667',
			longitude: '120.146465'
		}
	},
	mutations: {
		setUserLocation(state, location) {
			state.userLocation = location;
		}
	},
	actions: {
		async getUserLocation({
			commit
		}) {
			try {
				const res = await uni.getLocation({
					type: 'gcj02'
				});
				const userLocation = {
					latitude: res.latitude,
					longitude: res.longitude
				};
				commit('setUserLocation', userLocation);
			} catch (err) {
				console.error('Failed to get user location:', err);
			}
		}
	}
})
