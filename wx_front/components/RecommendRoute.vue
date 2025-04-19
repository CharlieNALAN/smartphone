<template>
	<view class="route-container">
		<swiper class="route-cards-swiper" :circular="true" :previous-margin="'50rpx'" :next-margin="'50rpx'" @change="handleSwiperChange">
			<swiper-item v-for="(route, index) in routes" :key="index" class="route-card-item">
				<view class="route-card" :class="{ 'card-active': currentIndex === index }">
					<image src="http://localhost:8000/media/attraction_images雷峰夕照.jpeg" mode="aspectFill" class="route-image"></image>
					<view class="route-card-content">
						<view class="route-tag">推荐路线</view>
						<view class="route-name">{{route.route_name}}</view>
						<view class="route-info-row">
							<view class="route-info">
								<uni-icons type="flag" size="14" color="#ffc107"></uni-icons>
								<text>{{route.custom_lists ? route.custom_lists.length : 0}} 个景点</text>
							</view>
							<text class="route-duration">约{{route.duration || '2'}}小时</text>
						</view>
						<view class="route-description-text">{{route.route_description || '暂无描述'}}</view>
						<view class="see-more-btn" @click="showRouteDetail(route)">
							<text>查看路线</text>
							<uni-icons type="right" size="14" color="#ffffff"></uni-icons>
						</view>
					</view>
				</view>
			</swiper-item>
		</swiper>

		<!-- 底部弹出面板 -->
		<view class="popup-mask" v-if="showPopup" @click="closePopup"></view>
		<view class="popup-panel" :class="{ 'popup-show': showPopup }">
			<view class="panel-header">
				<text class="panel-title">{{currentRoute.route_name}}</text>
				<uni-icons type="closeempty" size="24" color="#333" @click="closePopup"></uni-icons>
			</view>
			<scroll-view scroll-y class="panel-content">
				<view class="route-description">
					<text>{{currentRoute.route_description}}</text>
				</view>
				<view class="attraction-list">
					<view class="attraction-item" v-for="(attraction, index) in currentRoute.custom_lists" :key="index">
						<view class="attraction-index">{{index + 1}}</view>
						<image class="attraction-image" :src="attraction.attraction.image" mode="aspectFill"></image>
						<view class="attraction-info">
							<text class="attraction-name">{{attraction.attraction.attraction_name}}</text>
							<view class="attraction-address" @click="openMapNav(attraction)">
								<uni-icons type="location-filled" size="16" color="#3bcb98"></uni-icons>
								<text class="address-text">{{attraction.attraction.address || '暂无地址信息'}}</text>
							</view>
						</view>
						<view class="nav-button" @click="openMapNav(attraction)">
							<uni-icons type="paperplane-filled" size="16" color="#ffffff"></uni-icons>
						</view>
					</view>
				</view>
			</scroll-view>
		</view>
	</view>
</template>

<script>
	export default {
		name: "recommend-route",
		data() {
			return {
				global_scenic_id: getApp().globalData.global_scenic_id,
				routes: [],
				currentIndex: 0,
				showPopup: false,
				currentRoute: {}
			};
		},
		created() {
			this.fetchRoutes();
		},
		methods: {
			fetchRoutes() {
				uni.request({
					url: `http://localhost:8000/route/?scenic=${this.global_scenic_id}`,
					method: 'GET',
					success: (res) => {
						if (res.data) {
							this.routes = res.data;
							this.fetchRouteDetails();
						}
					},
					fail: (err) => {
						console.error('Failed to fetch routes:', err);
					}
				});
			},
			fetchRouteDetails() {
				this.routes.forEach((route, index) => {
					uni.request({
						url: `http://localhost:8000/route/${route.id}`,
						method: 'GET',
						success: (res) => {
							if (res.data) {
								this.$set(this.routes, index, {
									...route,
									custom_lists: res.data.custom_lists
								});
							}
						},
						fail: (err) => {
							console.error('Failed to fetch attractions for route:', err);
						}
					});
				});
			},
			handleSwiperChange(e) {
				this.currentIndex = e.detail.current;
			},
			showRouteDetail(route) {
				this.currentRoute = route;
				this.showPopup = true;
			},
			closePopup() {
				this.showPopup = false;
			},
			openMapNav(attraction) {
				uni.openLocation({
					latitude: attraction.attraction.attraction_lat,
					longitude: attraction.attraction.attraction_lng,
					name: attraction.attraction.attraction_name,
					address: attraction.attraction.address,
					success: (res) => {
						console.log(res)
					},
					fail: (res) => {
						console.log(res)
					}
				})
			}
		}
	}
</script>

<style>
	.route-container {
		position: relative;
		height: 650rpx;
	}
	
	.route-cards-swiper {
		height: 650rpx;
		margin-top: 20rpx;
	}
	
	.route-card-item {
		padding: 10rpx 0;
	}
	
	.route-card {
		position: relative;
		height: 600rpx;
		border-radius: 30rpx;
		overflow: hidden;
		transform: scale(0.9);
		transition: all 0.3s;
		box-shadow: 0 10rpx 20rpx rgba(0, 0, 0, 0.1);
	}
	
	.card-active {
		transform: scale(1);
	}
	
	.route-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}
	
	.route-card-content {
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		padding: 40rpx;
		background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
		color: #fff;
	}
	
	.route-tag {
		font-size: 24rpx;
		opacity: 0.8;
		margin-bottom: 10rpx;
		color: #3bcb98;
	}
	
	.route-name {
		font-size: 40rpx;
		font-weight: bold;
		margin-bottom: 20rpx;
	}
	
	.route-info-row {
		display: flex;
		align-items: center;
		margin-bottom: 20rpx;
	}
	
	.route-info {
		display: flex;
		align-items: center;
		margin-right: 20rpx;
	}
	
	.route-info text {
		margin-left: 10rpx;
		font-size: 24rpx;
	}
	
	.route-duration {
		font-size: 24rpx;
		opacity: 0.8;
	}
	
	.route-description-text {
		font-size: 26rpx;
		opacity: 0.9;
		margin-bottom: 30rpx;
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 2;
		overflow: hidden;
	}
	
	.see-more-btn {
		display: inline-flex;
		align-items: center;
		background-color: rgba(59,203,152,0.3);
		padding: 15rpx 30rpx;
		border-radius: 30rpx;
		backdrop-filter: blur(10px);
	}
	
	.see-more-btn text {
		margin-right: 10rpx;
		font-size: 26rpx;
	}
	
	/* 底部弹出面板样式 */
	.popup-mask {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.5);
		z-index: 998;
	}
	
	.popup-panel {
		position: fixed;
		left: 0;
		right: 0;
		bottom: 0;
		height: 80vh;
		background-color: #fff;
		border-radius: 30rpx 30rpx 0 0;
		transform: translateY(100%);
		transition: transform 0.3s;
		z-index: 999;
	}
	
	.popup-show {
		transform: translateY(0);
	}
	
	.panel-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1px solid #f5f5f5;
	}
	
	.panel-title {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
	}
	
	.panel-content {
		height: calc(80vh - 100rpx);
		padding: 30rpx;
	}
	
	.route-description {
		font-size: 28rpx;
		color: #666;
		line-height: 1.6;
		margin-bottom: 30rpx;
	}
	
	.attraction-list {
		padding-bottom: 30rpx;
	}
	
	.attraction-item {
		display: flex;
		align-items: center;
		padding: 20rpx;
		margin-bottom: 20rpx;
		background-color: #f8f8f8;
		border-radius: 15rpx;
		width: 93%;
	}
	
	.attraction-index {
		width: 40rpx;
		height: 40rpx;
		border-radius: 50%;
		background: linear-gradient(to right, #5ac7d1, #60e1c1);
		color: white;
		font-size: 24rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-right: 20rpx;
	}
	
	.attraction-image {
		width: 120rpx;
		height: 120rpx;
		border-radius: 10rpx;
		margin-right: 20rpx;
	}
	
	.attraction-info {
		flex: 1;
	}
	
	.attraction-name {
		font-size: 28rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 10rpx;
	}
	
	.attraction-address {
		display: flex;
		align-items: center;
	}
	
	.address-text {
		font-size: 24rpx;
		color: #999;
		margin-left: 10rpx;
	}
	
	.nav-button {
		width: 60rpx;
		height: 60rpx;
		border-radius: 50%;
		background: linear-gradient(to right, #5ac7d1, #60e1c1);
		display: flex;
		align-items: center;
		justify-content: center;
		margin-left: 20rpx;
	}
</style>

