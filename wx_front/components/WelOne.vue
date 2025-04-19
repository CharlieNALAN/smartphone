<template>
	<view>
		<view class="container" :style="'height:'+ show_screen_height + 'px;'">
			<image class="screen" :src="backimg_src"
				:style="'height:'+ show_screen_height + 'px;' +'width: 100%;z-index: -1;'" mode="scaleToFill"></image>
			<view class="choose_scenic">
				<view class="txt1">
					<text>请选择您所要游览的景区</text>
				</view>
				<uni-data-checkbox class="scenic_pick" mode="tag" v-model="selectedScenic" :localdata="scenics">
				</uni-data-checkbox>
				<button class="go_home" type="primary" @click="goToHome">开启旅程</button>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		name: "WelOne",
		data() {
			return {
				backimg_src: getApp().globalData.resourceURL + '/media/welcome.png',
				show_screen_height: getApp().globalData.windowHeight,
				scenics: [],
				selectedScenic: null,
			};
		},
		mounted() {
			// 在页面加载时获取景点数据
			this.getScenics();
		},
		methods: {
			getScenics() {
				uni.request({
					url: 'http://localhost:8000/scenic',
					method: 'GET',
					success: (res) => {
						if (res.statusCode === 200) {
							// 将从后端获取的数据存储到attractions中
							this.scenics = res.data.map(scenic => ({
								text: scenic.scenic_name,
								value: scenic.scenic_id,
							}));
							console.log(this.scenics);
						} else {
							console.error('Failed to fetch scenics data');
						}
					},
					fail: (err) => {
						console.error('Failed to fetch scenics data:', err);
					},
				});
			},
			goToHome() {
				// 获取全局变量对象  
				const app = getApp();
				// 将局部变量的值赋给全局变量  
				app.globalData.global_scenic_id = this.selectedScenic;
				console.log(app.globalData.global_scenic_id);
				// 跳转到 tabBar 页面  
				uni.switchTab({
					url: '/pages/home/home'
				});
			}
		},

	}
</script>

<style>
	.container {
		width: 100%;
	}

	.txt1 {
		margin-top: 10px;
		display: flex;
		justify-content: center;
		/* 水平居中 */
		align-items: center;
		/* 垂直居中 */
		height: 20px;
		font-size: 14px;
	}

	.choose_scenic {
		position: absolute;
		left: 50%;
		bottom: 20%;
		transform: translate(-50%, -50%);
		background-color: rgba(123, 123, 123, 0.5);
		width: 200px;
		height: 300px;
		border-radius: 20px;
	}

	.scenic_pick {
		margin-top: 5px;
		position: absolute;
		top: 45%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 130px;
		height: 200px;
	}
	
	.go_home {
		margin-top: 200px;
		width: 60%;
		background: linear-gradient(to right, #5ac7d1, #60e1c1);
	}
</style>
