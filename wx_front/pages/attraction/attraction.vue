<template>
	<view class="attraction-page">
		<NavBar>
			<template slot="title">
				<view>Attraction List</view>
			</template>
		</NavBar>
		
		<!-- 搜索栏 -->
		<view class="search-container">
			<uni-search-bar placeholder="Search attractions" bgColor="#f5f5f5" radius="50" cancelButton="none" 
				@confirm="search" borderColor="#eeeeee" />
		</view>
		
		<!-- 景点列表 -->
		<view class="attraction-list">
			<view class="attraction-card" v-for="item in attractions">
				<view class="attraction-content">
					<view class="attraction-image">
						<image :src="item.image" mode="aspectFill" />
					</view>
					<view class="attraction-info">
						<view class="attraction-name-row">
							<text class="attraction-name">{{ item.attraction_name }}</text>
							<uni-tag class="category-tag" :text="item.category_text" 
								:inverted="true" type="success" size="small" />
						</view>
						<view class="attraction-description">
							<text>{{item.description || "No description"}}</text>
						</view>
						<view class="attraction-meta">
							<view class="distance-info">
								<uni-icons type="location-filled" size="14" color="#3bcb98"></uni-icons>
								<text>{{getDistanceText(item)}}</text>
							</view>
							<view class="action-button" @click="navto_detail(item.attraction_id)">
								<text>Details</text>
								<uni-icons type="right" size="14" color="#ffffff"></uni-icons>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 无数据提示 -->
		<view class="empty-state" v-if="attractions.length === 0">
			<uni-icons type="info-filled" size="50" color="#cccccc"></uni-icons>
			<text>No attraction data</text>
		</view>
	</view>
</template>

<script>
	import NavBar from "../../components/NavBar.vue";
	import { mapState, mapActions } from 'vuex';

	export default {
		components: {
			NavBar
		},
		data() {
			return {
				global_scenic_id: getApp().globalData.global_scenic_id,
				attractions: [], // 存储从后端获取的景点数据
				distanceCache: {} // 缓存计算的距离
			}
		},
		computed: {
			...mapState({
				userLocation: state => state.userLocation
			})
		},
		onShow() {
			// 每次显示页面时获取最新位置
			this.getUserLocation();
		},
		mounted() {
			// 页面加载时获取位置和景点数据
			this.getUserLocation();
			this.getAttractions();
			// 开始监听位置变化
			this.$store.dispatch('startLocationWatch');
		},
		onHide() {
			// 页面隐藏时停止监听位置
			this.$store.dispatch('stopLocationWatch');
		},
		onUnload() {
			// 页面卸载时停止监听位置
			this.$store.dispatch('stopLocationWatch');
		},
		methods: {
			...mapActions(['getUserLocation']),
			
			// 计算并返回到景点的距离文本
			getDistanceText(attraction) {
				// 如果没有用户位置或景点位置，返回默认文本
				if (!this.userLocation || !attraction.attraction_lat || !attraction.attraction_lng) {
					return 'Distance unknown';
				}
				
				// 使用缓存避免重复计算
				const attractionId = attraction.attraction_id;
				if (this.distanceCache[attractionId]) {
					return this.distanceCache[attractionId];
				}
				
				// 计算距离
				const { value, unit } = this.calculateDistance(
					this.userLocation.latitude, 
					this.userLocation.longitude,
					attraction.attraction_lat,
					attraction.attraction_lng
				);
				
				// 保存到缓存
				const distanceText = `${value.toFixed(0)}${unit} from you`;
				this.distanceCache[attractionId] = distanceText;
				
				return distanceText;
			},
			
			// 计算两点之间的距离
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

				// 返回包含距离值和单位的对象
				return {
					value: distanceValue,
					unit: distanceUnit
				};
			},
			
			deg2rad(deg) {
				return deg * (Math.PI / 180);
			},
			
			// 位置变化时清除距离缓存
			clearDistanceCache() {
				this.distanceCache = {};
			},
			
			// 从后端获取景点数据
			getAttractions() {        
			  	uni.request({  
			        url: `http://localhost:8000/attraction?scenic=${this.global_scenic_id}`, // 添加查询参数  
			        method: 'GET',  
			        success: (res) => {  
			            if (res.statusCode === 200) {  
			                // 直接使用后端返回的数据，包括category_text  
			                this.attractions = res.data.results;
							console.log(this.attractions);
							// 清除距离缓存，以便重新计算
							this.clearDistanceCache();
			            } else {  
			                console.error('Failed to fetch attractions data');  
			            }  
			        },  
			        fail: (err) => {  
			            console.error('Failed to fetch attractions data:', err);  
			        },  
			    });  
			},
			navto_detail(attraction_id) {
				console.log('Navigate to navigation page' + attraction_id);
				uni.navigateTo({
					url: '/pages/detail/detail?attraction_id=' + attraction_id,
				})
			},
			search(e) {
				console.log("搜索关键词:", e.value);
				// 实现搜索功能
			}
		},
		watch: {
			// 监听位置变化，清除距离缓存
			userLocation: {
				handler() {
					this.clearDistanceCache();
				},
				deep: true
			}
		}
	}
</script>

<style>
	.attraction-page {
		background-color: #f5f5f5;
		min-height: 100vh;
		padding-bottom: 30rpx;
	}
	
	/* 搜索栏样式 */
	.search-container {
		padding: 20rpx 30rpx;
		background-color: #ffffff;
		border-bottom: 1px solid #f0f0f0;
	}
	
	/* 景点列表样式 */
	.attraction-list {
		padding: 20rpx;
	}
	
	.attraction-card {
		background-color: #ffffff;
		border-radius: 15rpx;
		margin-bottom: 20rpx;
		box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.05);
		overflow: hidden;
	}
	
	.attraction-content {
		display: flex;
		position: relative;
	}
	
	.attraction-image {
		width: 220rpx;
		min-width: 220rpx;
		height: 220rpx;
	}
	
	.attraction-image image {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}
	
	.attraction-info {
		flex: 1;
		padding: 20rpx;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}
	
	.attraction-name-row {
		display: flex;
		align-items: center;
		margin-bottom: 10rpx;
	}
	
	.attraction-name {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-right: 10rpx;
	}
	
	.category-tag {
		transform: scale(0.9);
		transform-origin: left center;
	}
	
	.attraction-description {
		margin-bottom: 12rpx;
	}
	
	.attraction-description text {
		font-size: 26rpx;
		color: #666;
		line-height: 1.4;
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 1;
		overflow: hidden;
		text-overflow: ellipsis;
	}
	
	.attraction-meta {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.distance-info {
		display: flex;
		align-items: center;
	}
	
	.distance-info text {
		font-size: 24rpx;
		color: #999;
		margin-left: 5rpx;
	}
	
	.action-button {
		display: flex;
		align-items: center;
		background: linear-gradient(to right, #5ac7d1, #60e1c1);
		padding: 8rpx 20rpx;
		border-radius: 30rpx;
	}
	
	.action-button text {
		color: #ffffff;
		font-size: 24rpx;
		margin-right: 5rpx;
	}
	
	/* 无数据状态 */
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 100rpx 0;
	}
	
	.empty-state text {
		margin-top: 20rpx;
		font-size: 28rpx;
		color: #999;
	}
</style>
