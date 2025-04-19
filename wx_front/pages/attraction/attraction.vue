<template>
	<view class="attraction-page">
		<NavBar>
			<template slot="title">
				<view>景点列表</view>
			</template>
		</NavBar>
		
		<!-- 搜索栏 -->
		<view class="search-container">
			<uni-search-bar placeholder="搜索景点" bgColor="#f5f5f5" radius="50" cancelButton="none" 
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
						<view class="attraction-header">
							<text class="attraction-name">{{ item.attraction_name }}</text>
							<uni-tag class="category-tag" :text="item.category_text" 
								:inverted="true" type="success" size="small" />
						</view>
						<view class="attraction-description">
							<text>{{item.description}}</text>
						</view>
						<view class="attraction-meta">
							<view class="distance-info">
								<uni-icons type="location-filled" size="14" color="#3bcb98"></uni-icons>
								<text>距离您300m</text>
							</view>
							<view class="action-button" @click="navto_detail(item.attraction_id)">
								<text>查看详情</text>
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
			<text>暂无景点数据</text>
		</view>
	</view>
</template>

<script>
	import NavBar from "../../components/NavBar.vue";

	export default {
		components: {
			NavBar
		},
		data() {
			return {
				global_scenic_id: getApp().globalData.global_scenic_id,
				attractions: [], // 存储从后端获取的景点数据
				category_choices: { // 定义category的映射关系  
					1: "自然风光",
					2: "历史遗迹",
					3: "文化遗产",
					4: "娱乐体验"
				}
			}
		},
		mounted() {
			this.getAttractions();
		},
		methods: {
			// 从后端获取景点数据
			getAttractions() {        
			  	uni.request({  
			        url: `http://localhost:8000/attraction?scenic=${this.global_scenic_id}`, // 添加查询参数  
			        method: 'GET',  
			        success: (res) => {  
			            if (res.statusCode === 200) {  
			                // 假设后端返回的数据结构没有变化  
			                this.attractions = res.data.results.map(item => ({  
			                    ...item,  
			                    category_text: this.category_choices[item.category]  
			                }));
							console.log(this.attractions);
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
	
	.attraction-header {
		display: flex;
		align-items: center;
		margin-bottom: 10rpx;
	}
	
	.attraction-name {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-right: 15rpx;
	}
	
	.category-tag {
		transform: scale(0.9);
		transform-origin: left center;
	}
	
	.attraction-description {
		flex: 1;
		margin-bottom: 10rpx;
	}
	
	.attraction-description text {
		font-size: 26rpx;
		color: #666;
		line-height: 1.4;
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 2;
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
		padding: 10rpx 20rpx;
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
