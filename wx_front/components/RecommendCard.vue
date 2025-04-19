<template>
	<swiper class="cards-swiper" :circular="true" :previous-margin="'50rpx'" :next-margin="'50rpx'" @change="handleSwiperChange">
		<swiper-item v-for="(item, index) in recommend_datas" :key="index" class="card-item">
			<view class="attraction-card" :class="{ 'card-active': currentIndex === index }">
				<image :src="'http://localhost:8000/' + item.image" mode="aspectFill" class="card-image"></image>
				<view class="card-content">
					<view class="location-tag">{{item.scenic_name || ''}}</view>
					<view class="attraction-name">{{item.attraction_name}}</view>
					<view class="rating-row">
						<view class="rating">
							<uni-icons type="star-filled" size="14" color="#ffc107"></uni-icons>
							<text>{{item.rating || '4.8'}}</text>
						</view>
						<text class="reviews">{{item.reviews || '100'}} reviews</text>
					</view>
					<view class="see-more-btn" @click="to_detail(item)">
						<text>See more</text>
						<uni-icons type="right" size="14" color="#ffffff"></uni-icons>
					</view>
				</view>
				<view class="card-favorite" @click="toggleFavorite(index)">
					<uni-icons :type="item.isFavorite ? 'heart-filled' : 'heart'" size="24" color="#ffffff"></uni-icons>
				</view>
			</view>
		</swiper-item>
	</swiper>
</template>

<script>
	import {
		mapState
	} from 'vuex';
	import {
		calculateDistance,
		deg2rad
	} from '../utils/distance.js';
	export default {
		name: 'RecommendCard',
		options: {
			virtualHost: true
		},
		props: {
			// 接收父组件传递的景点数据
			initialData: {
				type: Array,
				default: () => []
			}
		},
		data() {
			return {
				recommend_datas: [], // 存放推荐景点数据
				currentIndex: 0,
				strategy: 1,
				global_scenic_id: getApp().globalData.global_scenic_id,
			};
		},
		computed: {
			...mapState({
				userLocation: state => state.userLocation
			})
		},
		watch: {
			initialData: {
				handler(newVal) {
					if (newVal && newVal.length > 0) {
						this.recommend_datas = newVal.map(item => ({
							...item,
							isFavorite: false
						}));
					}
				},
				immediate: true
			}
		},
		methods: {
			// 发送请求获取推荐景点信息
			fetchRecommendations() {
				if (this.global_scenic_id == 1) {
					this.strategy = 1;
				} else if (this.global_scenic_id == 2) {
					this.strategy = 2;
				} else if (this.global_scenic_id == 3) {
					this.strategy = 5;
				}
				uni.request({
					url: 'http://localhost:8000/api/recommend-list/' + this.strategy + '/',
					method: 'GET',
					success: (res) => {
						if (res.data.recommendations) {
							this.recommend_datas = res.data.recommendations.map(item => ({
								...item,
								isFavorite: false
							}));
						}
					},
					fail: (err) => {
						console.error('Failed to fetch recommendations:', err);
					}
				});
			},
			handleSwiperChange(e) {
				this.currentIndex = e.detail.current;
				// 触发事件通知父组件当前索引变化
				this.$emit('index-change', this.currentIndex);
			},
			toggleFavorite(index) {
				this.recommend_datas[index].isFavorite = !this.recommend_datas[index].isFavorite;
				// 触发事件通知父组件收藏状态变化
				this.$emit('favorite-change', {
					index: index,
					isFavorite: this.recommend_datas[index].isFavorite
				});
			},
			navto_detail(item) {
				console.log('item: ' + item);
				uni.navigateTo({
					url: '/pages/detail/detail?attraction_id=' + item.attraction_id,
				})
			},
		},
		mounted() {
			if (!this.initialData || this.initialData.length === 0) {
				this.fetchRecommendations();
			}
		}
	}
</script>

<style>
	.cards-swiper {
		height: 650rpx;
		margin-top: 20rpx;
	}
	
	.card-item {
		padding: 10rpx 0;
	}
	
	.attraction-card {
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
	
	.card-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}
	
	.card-content {
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		padding: 40rpx;
		background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
		color: #fff;
	}
	
	.location-tag {
		font-size: 24rpx;
		opacity: 0.8;
		margin-bottom: 10rpx;
	}
	
	.attraction-name {
		font-size: 40rpx;
		font-weight: bold;
		margin-bottom: 20rpx;
	}
	
	.rating-row {
		display: flex;
		align-items: center;
		margin-bottom: 30rpx;
	}
	
	.rating {
		display: flex;
		align-items: center;
		margin-right: 20rpx;
	}
	
	.rating text {
		margin-left: 10rpx;
	}
	
	.reviews {
		font-size: 24rpx;
		opacity: 0.8;
	}
	
	.see-more-btn {
		display: inline-flex;
		align-items: center;
		background-color: rgba(255,255,255,0.2);
		padding: 15rpx 30rpx;
		border-radius: 30rpx;
		backdrop-filter: blur(10px);
	}
	
	.see-more-btn text {
		margin-right: 10rpx;
		font-size: 26rpx;
	}
	
	.card-favorite {
		position: absolute;
		top: 30rpx;
		right: 30rpx;
		width: 80rpx;
		height: 80rpx;
		border-radius: 50%;
		background-color: rgba(0,0,0,0.3);
		backdrop-filter: blur(10px);
		display: flex;
		align-items: center;
		justify-content: center;
	}
</style>
