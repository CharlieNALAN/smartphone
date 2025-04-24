<template>
	<view>
		<NavBar>
			<template slot="title">
				<view>地图导览</view>
			</template>
		</NavBar>
		<view class="container map-container">
			<map class="map" show-location :scale="scale" :longitude="longitude" :latitude="latitude" :markers="markers"
				@markertap="showAttractionInfo">
			</map>
			<canvas canvas-id="heatmapCanvas" class="heatmap-canvas"
				style="position: absolute; top: 0; left: 0;"></canvas>
			<view v-if="showInfo" class="attraction-info">
				<uni-card>
					<template v-slot:title>
						<view class="select_attraction">
							<image class="attraction-image" :src="selectedAttraction.image" mode="aspectFill" />
							<view class="select_info">
								<view class="name_info">
									<text style="color: black;">{{ selectedAttraction.attraction_name }}</text>
								</view>
								<view class="other-info">
									<uni-icons type="paperplane-filled" size="16" color="#a9dbd0"></uni-icons>
									<text>{{ distanceToAttraction }}</text>
								</view>
								<view class="other-info">
									<uni-icons type="location-filled" size="16" color="#a9dbd0"></uni-icons>
									<text> {{selectedAttraction.address}}</text>
								</view>
							</view>
						</view>
					</template>
					<view class="select_nav">
						<view>
							<uni-tag text="查看详情" circle="true" type="warning" style="margin-left: 15px;"
								@click="navto_detail"></uni-tag>
							<uni-tag v-if="!isChecked" text="标记为已打卡" circle="true" type="success"
								style="margin-left: 15px;" @click="markChecked"></uni-tag>
							<uni-tag v-if="isChecked" text="已打卡" circle="true" type="success"
								style="margin-left: 15px;"></uni-tag>
						</view>
						<view class="select_nav_box" @click="navigateToNavigationPage(selectedAttraction)">
							<uni-icons type="paperplane-filled" size="16" color="#a9dbd0"></uni-icons>
							<text>导航</text>
						</view>
					</view>
				</uni-card>
			</view>

		</view>
		<uni-popup ref="popup" type="bottom" background-color="#fff" border-radius="10px 10px 0 0">
			<view class="time-picker">
				<text>请选择打卡此景点的时间</text>
				<u-line margin="10px 0" color="white" />
				<uni-datetime-picker type="datetime" returnType="date" v-model="selectedDateTime"
					@change="handleChange" />
			</view>
		</uni-popup>
	</view>
</template>

<script>
	import NavBar from "../../components/NavBar.vue";
	import {
		mapState
	} from 'vuex';
	export default {
		components: {
			NavBar
		},
		data() {
			return {
				global_scenic_id: null,
				resource_url: getApp().globalData.resourceURL,
				scenic_info: [],
				title: 'map',
				latitude: 30.244917207446186,
				longitude: 120.14621247265623,
				scale: 13.8,
				attractions: [], // 存储从后端获取的景点数据
				markers: [], // 地图标记点
				showInfo: false, // 是否显示景点信息卡片
				selectedAttraction: {}, // 当前选中的景点信息
				isChecked: false,
				selectedDateTime: '',
				// userLocation: {}, // 用户当前位置
				distanceToAttraction: null,
			};
		},
		onShow() {
			this.fetchGlobalScenicId();
			this.fetchScenic();
			// 在页面加载时获取景点数据
			this.getAttractions();
		},
		computed: {
			...mapState({
				userLocation: state => state.userLocation
			})
		},
		methods: {
			fetchGlobalScenicId() {
				this.global_scenic_id = getApp().globalData.global_scenic_id;
			},
			markChecked() {
				// const now = new Date();
				this.$refs.popup.open()
			},
			addFootprint(selectedDateTime) {
				// 假设这里调用了后端接口，将景点加入用户的历史足迹信息中，并且设置 manual_check 为 true
				// 获取当前用户ID
				let userId = null;
				const app = getApp();
				
				// 从全局变量获取用户信息
				if (app.globalData && app.globalData.userInfo) {
					userId = app.globalData.userInfo.id || app.globalData.userInfo.user_id;
				}
				
				// 如果全局变量中没有，尝试从本地存储获取
				if (!userId) {
					try {
						const userInfoStr = uni.getStorageSync('userInfo');
						if (userInfoStr) {
							const userInfo = JSON.parse(userInfoStr);
							userId = userInfo.id || userInfo.user_id;
						}
					} catch (e) {
						console.error('获取用户信息失败', e);
					}
				}
				
				// 如果没有获取到用户ID，提示用户登录
				if (!userId) {
					uni.showToast({
						title: '请先登录',
						icon: 'none'
					});
					return;
				}
				
				uni.request({
					url: `${this.resource_url}footprint/`,
					method: 'POST',
					data: {
						user: userId,
						scenic: this.global_scenic_id,
						attraction: this.selectedAttraction.attraction_id,
						check_in_time: selectedDateTime, // 用户选择的日期时间
						manual_check: true // 设置 manual_check 为 true
					},
					success: (res) => {
						// 成功添加足迹
						console.log('足迹添加成功');
						this.$refs.popup.close();
						this.isChecked = true;
					},
					fail: (err) => {
						// 处理错误
						console.error('足迹添加失败:', err);
					}
				});
			},
			handleChange(event) {
				// 选择日期时间后的处理逻辑
				console.log(this.selectedDateTime);
				this.addFootprint(this.selectedDateTime); // 标记打卡后添加足迹
			},
			fetchScenic() {
				uni.request({
					url: `http://localhost:8000/scenic/${this.global_scenic_id}`,
					method: 'GET',
					success: (res) => {
						if (res.statusCode === 200) {
							// 将从后端获取的数据存储到attractions中
							this.scenic_info = res.data;
							this.longitude = res.data.scenic_lng;
							this.latitude = res.data.scenic_lat;
							this.scale = res.data.scale;
						} else {
							console.error('Failed to fetch attractions data');
						}
					},
				})
			},
			// 从后端获取景点数据
			getAttractions() {
				uni.request({
					url: `http://localhost:8000/attraction?scenic=${this.global_scenic_id}`,
					method: 'GET',
					success: (res) => {
						if (res.statusCode === 200) {
							// 将从后端获取的数据存储到attractions中
							this.attractions = res.data.results;
							console.log('获取到的景点数据:', JSON.stringify(this.attractions));
							console.log('景点数量:', this.attractions.length);
							// 渲染地图标记点
							this.renderMarkers();
						} else {
							console.error('Failed to fetch attractions data');
						}
					},
					fail: (err) => {
						console.error('Failed to fetch attractions data:', err);
					},
				});
			},
			// 渲染地图标记点
			renderMarkers() {
				const markers = this.attractions.map((attraction, index) => ({
					id: attraction.attraction_id,
					latitude: attraction.attraction_lat,
					longitude: attraction.attraction_lng,
					name: attraction.attraction_name,
					title: attraction.attraction_name,
					callout: {
						content: attraction.attraction_name,
						color: '#000000',
						fontSize: 12,
						borderRadius: 4,
						padding: 5,
						bgColor: '#ffffff',
						display: 'ALWAYS'
					},
					iconPath: '/static/tabbar_icon/location.png', // 使用已有图标
					width: 32, // 增大标记宽度
					height: 32, // 增大标记高度
					zIndex: index + 1, // 为每个标记点设置不同的层级，避免重叠问题
					anchor: {
						x: 0.5,
						y: 1
					}
				}));
				this.markers = markers;
				console.log('标记点数量:', markers.length);
				console.log('标记点详情:', JSON.stringify(markers));
			},
			// 显示景点信息卡片
			showAttractionInfo(e) {
				const markerId = e.markerId;
				const selectedAttraction = this.attractions.find(attraction => attraction.attraction_id === markerId);
				console.log(this.userLocation);
				if (selectedAttraction) {
					// 计算距离
					// const distance = this.calculateDistance(this.userLocation.latitude, this.userLocation.longitude,
					// 	selectedAttraction.attraction_lat, selectedAttraction.attraction_lng);
					// console.log(distance);
					const {
						value,
						unit
					} = this.calculateDistance(this.userLocation.latitude, this.userLocation.longitude,
						selectedAttraction.attraction_lat, selectedAttraction.attraction_lng);
					this.distanceToAttraction = `距您约 ${value.toFixed(2)} ${unit}`;
					console.log(this.distanceToAttraction);
					// 设置选中的景点信息
					this.selectedAttraction = selectedAttraction;
					// 显示信息卡片
					this.showInfo = true;
					this.isChecked = false;
				}
			},
			// 计算距离
			calculateDistance(lat1, lon1, lat2, lon2) {
				var R = 6371; // 地球半径，单位：千米  
				var dLat = this.deg2rad(lat2 - lat1); // 纬度差转换为弧度  
				var dLon = this.deg2rad(lon2 - lon1); // 经度差转换为弧度  
				var a =
					Math.sin(dLat / 2) * Math.sin(dLat / 2) +
					Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) *
					Math.sin(dLon / 2) * Math.sin(dLon / 2);
				var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
				var distanceKm = R * c; // 距离，单位：千米  
				var distanceUnit = 'km';
				var distanceValue = distanceKm;
				if (distanceKm < 1) {
					distanceValue = distanceKm * 1000; // 转换为米  
					distanceUnit = 'm';
				}

				// 返回包含距离值和单位的对象，或者仅返回距离值（如果需要）  
				return {
					value: distanceValue,
					unit: distanceUnit
				};
			},
			deg2rad(deg) {
				return deg * (Math.PI / 180);
			},
			// 跳转至景点详细信息页面
			navto_detail() {
				console.log('Navigate to ' + this.selectedAttraction.attraction_id);
				uni.navigateTo({
					url: '/pages/detail/detail?attraction_id=' + this.selectedAttraction.attraction_id,
				})
			},
			// 跳转至导航页面
			navigateToNavigationPage(selectedAttraction) {
				// 实现地图导航的逻辑
				uni.openLocation({
					latitude: selectedAttraction.attraction_lat,
					longitude: selectedAttraction.attraction_lng,
					name: selectedAttraction.attraction_name,
					address: selectedAttraction.address,
					success: (res) => {
						console.log(res)
					},
					fail: (res) => {
						console.log(res)
					}
				})
			},
		},
		beforeRouteEnter(to, from, next) {
			next(vm => {
				vm.fetchGlobalScenicId(); // 在路由进入前获取一次 global_scenic_id
				vm.fetchScenic(); // 在路由进入前获取景点信息
				vm.getAttractions(); // 在路由进入前获取景点数据
			});
		},
	};
</script>

<style scoped>
	.container {
		width: 100vw;
		display: flex;
		justify-content: center;
	}

	.map-container {
		position: relative;
		height: 100vh;
		/* 根据需求调整容器宽度 */
		overflow: hidden;
	}

	.map {
		position: absolute;
		width: 100%;
		height: 100%;
	}

	.attraction-image {
		width: 60px;
		height: 60px;
		margin-right: 10px;
		border-radius: 10px;
	}

	.time-picker {
		width: 300px;
		height: 100px;
		margin-top: 20px;
		margin-left: 50px;
	}

	.attraction-info {
		position: absolute;
		width: 400px;
		border-radius: 10rpx;
		bottom: 100px;
		z-index: 10;
	}

	.select_attraction {
		display: flex;
		align-items: center;
		padding: 10px;
	}

	.other-info {
		font-size: 12px;
		color: gray;
	}

	.select_nav {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.select_nav_box {
		display: flex;
		align-items: center;
		padding: 0px 10px 0px 8px;
		border-radius: 20px;
		border: 0.5px solid #a9dbd0;
		color: #a9dbd0;
		font-size: 12px;
	}

	.select_nav_box text {
		color: #a9dbd0;
		font-size: 12px;
	}
</style>
