<script>
	export default {
		data() {
			return {
				// global_strategy_id: null // 存放全局策略ID
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
			// setInterval(this.fetchRecommendationStrategy, 60000); // 每分钟发送一次请求
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
			
			// 尝试从本地存储获取用户信息
			try {
				const userInfoStr = uni.getStorageSync('userInfo');
				if (userInfoStr) {
					this.globalData.userInfo = JSON.parse(userInfoStr);
					console.log('从本地存储加载用户信息:', this.globalData.userInfo);
				}
			} catch (e) {
				console.error('读取用户信息失败:', e);
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
			// 			// 处理响应，更新全局状态或进行其他操作
			// 			if (res.data.strategy_id) {
			// 				this.global_strategy_id = res.data.strategy_id; // 将策略ID存储在全局状态中
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
	/*每个页面公共css */
	@import "uview-ui/index.scss";
	@import "/wxcomponents/vant/common/index.wxss";

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
		/* 使得子元素垂直排列 */
		justify-content: space-between;
		/* 子元素垂直均匀分布 */
	}
	
	.kaoyou {  
	    display: flex;  
	    justify-content: flex-end; /* 使子元素靠右对齐 */  
	} 
</style>
