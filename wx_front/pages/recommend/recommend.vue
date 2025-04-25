<template>
	<view class="recommend-page">
		<NavBar>
			<template slot="title">
				<view>Recommendations</view>
			</template>
		</NavBar>
		
		<!-- 搜索和分类区域 -->
		<view class="top-section">
			<view class="search-bar">
				<uni-icons type="search" size="20" color="#999"></uni-icons>
				<input type="text" placeholder="Search Attractions" />
			</view>
			<scroll-view scroll-x="true" class="category-scroll" show-scrollbar="false">
				<!-- <view class="category-list">
					<view class="category-item" :class="{ active: activeCategory === '全部' }" @click="setCategory('全部')">
						全部
					</view>
					<view class="category-item" :class="{ active: activeCategory === '热门' }" @click="setCategory('热门')">
						热门
					</view>
					<view class="category-item" :class="{ active: activeCategory === '文化' }" @click="setCategory('文化')">
						文化
					</view>
					<view class="category-item" :class="{ active: activeCategory === '自然' }" @click="setCategory('自然')">
						自然
					</view>
				</view> -->
			</scroll-view>
		</view>
		
		<!-- 景点推荐标题 -->
		<view class="section-title">
			<text class="title-text">Attraction Recommendations</text>
			<text class="subtitle-text">Discover Exciting Attractions</text>
		</view>
		
		<!-- 推荐卡片区域 -->
		<RecommendCard></RecommendCard>
		
		<!-- 路线推荐标题 -->
		<view class="section-title">
			<text class="title-text">Route Recommendations</text>
			<text class="subtitle-text">Well-planned routes</text>
		</view>
		
		<!-- 路线推荐组件 -->
		<RecommendRoute></RecommendRoute>
	</view>
</template>

<script>
	import NavBar from "../../components/NavBar.vue";
	import RecommendCard from "../../components/RecommendCard.vue";
	import RecommendRoute from "../../components/RecommendRoute.vue";
	export default {
		components: {
			NavBar,
			RecommendCard,
			RecommendRoute,
		},
		data() {
			return {
				recommend_datas: [], // 存放推荐景点数据
				strategy: 1,
				global_scenic_id: getApp().globalData.global_scenic_id,
				activeCategory: 'All',
				currentIndex: 0
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
			setCategory(category) {
				this.activeCategory = category;
				// 这里可以添加分类筛选逻辑
			},
			handleSwiperChange(e) {
				this.currentIndex = e.detail.current;
			},
			toggleFavorite(index) {
				this.recommend_datas[index].isFavorite = !this.recommend_datas[index].isFavorite;
			},
			navto_detail(item) {
				console.log('Navigating to detail with item:', item);
				if (item && item.attraction_id) {
					uni.navigateTo({
						url: '/pages/detail/detail?attraction_id=' + item.attraction_id,
						fail: (err) => {
							console.error('Navigation failed:', err);
							uni.showToast({
								title: 'Page navigation failed',
								icon: 'none'
							});
						}
					});
				} else {
					console.error('Invalid item or missing attraction_id:', item);
					uni.showToast({
						title: 'Incomplete attraction information',
						icon: 'none'
					});
				}
			}
		},
		mounted() {
			this.fetchRecommendations();
		}
	}
</script>

<style>
	.recommend-page {
		background-color: #ffffff;
		min-height: 100vh;
		padding-bottom: 40rpx;
	}
	
	.subtitle {
		font-size: 28rpx;
		color: #666;
	}
	
	.search-bar {
		display: flex;
		align-items: center;
		background-color: #f5f5f5;
		padding: 20rpx 30rpx;
		border-radius: 50rpx;
		margin-top: 20rpx;
	}
	
	.search-bar input {
		margin-left: 20rpx;
		font-size: 28rpx;
		width: 100%;
	}
	
	.section-title {
		padding: 10rpx 35rpx;
		display: flex;
		flex-direction: column;
	}
	
	.title-text {
		font-size: 36rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 10rpx;
	}
	
	.subtitle-text {
		font-size: 24rpx;
		color: #999;
	}
	
	.category-scroll {
		margin: 15rpx 0;
	}
	
	.category-list {
		display: flex;
		padding: 0 30rpx;
		white-space: nowrap;
	}
	
	.category-item {
		padding: 15rpx 40rpx;
		margin-right: 20rpx;
		background-color: #f5f5f5;
		border-radius: 30rpx;
		font-size: 28rpx;
		color: #666;
		transition: all 0.3s;
	}
	
	.category-item.active {
		background-color: #333;
		color: #fff;
	}
	
	.cards-swiper {
		height: 900rpx;
		margin-top: 20rpx;
	}
	
	.card-item {
		padding: 10rpx 0;
	}
	
	.attraction-card {
		position: relative;
		height: 800rpx;
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
