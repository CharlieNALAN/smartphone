<script>
	export default {
		data() {
			return {
				// global_strategy_id: null // store global strategy ID
				global_strategy_id: 1,
				global_scenic_id: null,
				globalData: {
					userInfo: null,
					screenHeight: 0,
					statusBarHeight: 0,
					windowHeight: 0,
					windowWidth: 0,
					rpx_const: 0,
					resourceURL: ''
				}
			};
		},
		onLaunch: function() {
			// this.fetchRecommendationStrategy();
			// setInterval(this.fetchRecommendationStrategy, 60000); // Send request every minute
			setInterval(() => {
				this.$store.dispatch('getUserLocation');
			}, 60000);
			console.log('App Launch')
			uni.getSystemInfo({
				success: (res) => {
					console.log(res)
					console.log(res.screenHeight)
					this.globalData.screenHeight = res.screenHeight
					this.globalData.statusBarHeight = res.statusBarHeight
					this.globalData.windowHeight = res.windowHeight
					this.globalData.windowWidth = res.windowWidth
					this.globalData.rpx_const = 750 / res.windowWidth

				}
			})
			this.globalData.resourceURL = 'http://127.0.0.1:8000/'
			
			// Try to get user info from local storage
			try {
				const userInfoStr = uni.getStorageSync('userInfo');
				if (userInfoStr) {
					this.globalData.userInfo = JSON.parse(userInfoStr);
					console.log('Loading user info from local storage:', this.globalData.userInfo);
				}
			} catch (e) {
				console.error('Failed to read user info:', e);
			}
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		},
		methods: {

			// fetchRecommendationStrategy() {
			// 	uni.request({
			// 		url: 'http://localhost:8000/get_recommendation_strategy',
			// 		method: 'GET',
			// 		success: (res) => {
			// 			// Process response, update global state or perform other operations
			// 			if (res.data.strategy_id) {
			// 				this.global_strategy_id = res.data.strategy_id; // Store strategy ID in global state
			// 			} else {
			// 				console.error('Strategy ID not found in response.');
			// 			}
			// 		},
			// 		fail: (err) => {
			// 			console.error('Failed to fetch recommendation strategy:', err);
			// 		}
			// 	});
			// },
		}
	}
</script>

<style lang="scss">
	/*every page's common css */
	@import "uview-ui/index.scss";
	@import "/wxcomponents/vant/common/index.css";

	.col-horizontal-center {
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	
	.col-ver-center {
		display: flex;
		flex-direction: column;
		justify-content: center;
	}

	.hor-ver-center {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.uni-navbar .uni-navbar--border.data-v-6bda1a90 {
		border-bottom-style: none;
	}
	
	.junyun {
		display: flex;
		/* Make child elements arrange vertically */
		justify-content: space-between;
		/* Child elements distributed evenly vertically */
	}
	
	.kaoyou {  
	    display: flex;  
	    justify-content: flex-end; /* Make child elements align to the right */  
	} 
</style>
