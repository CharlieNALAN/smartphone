<template>
	<view>
		<NavBar>
			<template slot="title">
				<view>Attraction Details</view>
			</template>
		</NavBar>
		<!-- <uni-nav-bar shadow fixed="true" statusBar="true" @clickLeft="back">
			<block slot="left">
				<uni-icons type="back" size="24"></uni-icons>
			</block>
			<view class="nav_title">
				景点详情
			</view>
		</uni-nav-bar> -->
		<view class="container" style="height: 250px;">
			<image style="width: 100%;" class="detail_img" :src="attraction_data.image" mode="aspectFill"></image>
		</view>
		<uni-list>
			<uni-list-item :title="attraction_data.attraction_name" />
			<uni-list-item :title="'Opening: '+ attraction_data.open_time + '-' + attraction_data.close_time" />
			<uni-list-item>
				<template v-slot:body>
					<view class="address_view">
						{{attraction_data.address}}
					</view>
				</template>
				<template v-slot:footer>
					<view class="nav_view" @click="navigateToNavigationPage(attraction_data)">
						<image class="slot_img" src="/static/tabbar_icon/location-active.png" mode="widthFix"></image>
						<text>Map·Nav</text>
					</view>
				</template>
			</uni-list-item>
			<!-- <uni-list-item showArrow="" title="点击购票" /> -->
		</uni-list>
		<view class="tour_detail_card">
			<view class="tour_detail_content">
				<view class="tour_index_title">
					<text>Playability Index</text>
				</view>
				<view class="tour_index_grade">
					<view class="tour_index_grade_content">
						<text>Recommended: 9</text>
						<text> Viewing: 10</text>
					</view>
					<view class="tour_index_grade_content">
						<text>Popularity: 10</text>
						<text>Comfort: 8</text>
					</view>
				</view>
			</view>
		</view>
		<view class="tour_detail_card">
			<view class="tour_detail_content">
				<view class="tour_index_title">
					<text>Attraction Introduction</text>
				</view>
				<view class="tour_intro">
					{{attraction_data.description}}
				</view>
			</view>
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
				attraction_data: {},
			}
		},
		methods: {
			back() {
				uni.navigateBack()
			},
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
		onLoad(options) {
			const attractionId = options.attraction_id;
			if (attractionId) {
				uni.request({
					url: 'http://localhost:8000/api/attraction/' + attractionId + '/',
					method: 'GET',
					success: (res) => {
						this.attraction_data = res.data;
					},
					fail: (err) => {
						console.error('Failed to fetch attractions data:', err);
					},

				})
			}
		}
	}
</script>

<style>
	.container {
		width: 100vw;
		display: flex;
		justify-content: center;
	}

	.address_view {
		display: flex;
		flex: 1;
		align-items: center;
	}

	.nav_view {
		display: flex;
		justify-content: flex-end;
		align-items: center;
		flex-direction: column;
	}

	.slot_img {
		width: 20px;
		height: 20px;
	}

	.tour_detail_content {
		padding: 40rpx 30rpx 40rpx 30rpx;
		width: 100%;
	}

	.tour_index_title {
		font-weight: bold;
	}

	.tour_index_grade {
		margin-top: 20rpx;
		background: linear-gradient(to right, #faf0e5, #fbe4c8);

		padding: 40rpx 30rpx 40rpx 30rpx;
		border-radius: 20rpx;
	}

	.tour_index_grade_content {
		display: flex;
		justify-content: space-between;
		margin-right: 200rpx;
		color: #815c3f;
	}

	.tour_intro {
		margin-top: 20rpx;
	}
</style>
