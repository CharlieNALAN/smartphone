<template>
	<view>
		<view class="swiper">
			<swiper :indicator-dots="true" :autoplay="true" :interval="3000" :duration="1000">
				<swiper-item v-for="item in swiperList">
					<image :src="item" class="slide-image"></image>
				</swiper-item>
			</swiper>
		</view>
		<uni-nav-bar left-width="120px" border="false" fixed="true" statusBar="true" background-color="#00FF0000">
			<block slot="left" class="nav_leftview">
				<view class="scenic_pick">
					<picker @change="bindPickerChange" :value="scenic_index" :range="scenic_array">
						<view class="scenic_text">{{scenic_array[scenic_index]}}</view>
					</picker>
					<uni-icons type="arrowdown" color="#666" size="18" />
				</view>
			</block>
		</uni-nav-bar>
		<view class="notice">
			<uni-notice-bar show-icon scrollable text="The Hong Kong Park Tulip Exhibition has opened the reservation channel! Note that the opening hours are 8:00-17:00, please arrange your visit time!">
			</uni-notice-bar>
		</view>
		<view class="category">
			<navigator class="category-item" hover-class="none" :url="item.url" v-for="item in menuList" :key="item.id"
				:open-type="item.opentype">
				<image class="icon" :src="item.src"></image>
				<text class="text">{{item.text}}</text>
			</navigator>
		</view>
		<view class="container">
			<uni-section class="futitle" title="Popular Attractions" titleFontSize="30rpx">
				<template v-slot:right>
					<navigation class="title-more" url="/pages/recommend/recommend">
						<text>See all</text>
						<uni-icons type="right" size="18"></uni-icons>
					</navigation>
				</template>
			</uni-section>
			<scroll-view :scroll-x="true" style="white-space: nowrap;">
				<view v-for="item in scenicList" class="hot-image">
					<image :src="item"></image>
				</view>
			</scroll-view>
		</view>
		<view class="container container-color">
			<uni-section class="futitle" title="Popular Routes" titleFontSize="30rpx">
				<template v-slot:right>
					<navigation class="title-more" url="/pages/recommend/recommend">
						<text>See all</text>
						<uni-icons type="right" size="18"></uni-icons>
					</navigation>
				</template>
			</uni-section>
			<scroll-view :scroll-x="true" style="white-space: nowrap;">
				<view v-for="item in routeList" class="hot-image">
					<image :src="item"></image>
				</view>
			</scroll-view>
		</view>
		
		<!-- 添加AI聊天悬浮按钮 -->
		<chat-button :position-bottom="200"></chat-button>
	</view>

</template>

<script>
	import ChatButton from '@/components/ChatButton.vue'
	
	export default {
		components: {
			ChatButton
		},
		data() {
			return {
				scenic_index: getApp().globalData.global_scenic_id - 1,
				scenic_array: ['Victoria Harbour', 'Peak', 'Disneyland', 'Ocean Park', 'Lamma Island'],
				swiperList: [
					'/static/swiper/seven.png',
					'/static/swiper/eight.png',
					'/static/swiper/nine.png',
					'/static/swiper/ten.png',
					'/static/swiper/eleven.png',
				],
				scenicList: [
					'/static/swiper/victoriaharbour2.jpg',
					'/static/swiper/victoriapeak2.jpg',
					'/static/swiper/disneyland1.jpg',
					'/static/swiper/oceanpark2.jpg',
					'/static/swiper/lammaisland1.jpg',
				],
				routeList: [
					'/static/swiper/route1.png',
					'/static/swiper/route2.png',
					'/static/swiper/route3.png',
					'/static/swiper/route4.png',
					'/static/swiper/route5.png',
				],
				menuList: [{
					id: 1,
					url: '/pages/map/map',
					text: 'Map',
					src: '/static/home_menu/map.png',
					opentype: 'switchTab',
				}, {
					id: 2,
					url: '/pages/attraction/attraction',
					text: 'Attractions',
					src: '/static/home_menu/info.png',
					opentype: 'navigate',
				}, {
					id: 3,
					url: '/pages/ticket/ticket',
					text: 'Ticket',
					src: '/static/home_menu/ticket.png',
					opentype: 'navigate',
				}, {
					id: 4,
					url: '/pages/track/track',
					text: 'Footprint',
					src: '/static/home_menu/track.png',
					opentype: 'switchTab',
				}]

			};
		},
		methods: {
			bindPickerChange: function(e) {
				console.log('picker发送选择改变，携带值为', e.detail.value);
				this.scenic_index = e.detail.value;
				getApp().globalData.global_scenic_id = parseInt(this.scenic_index) + 1;
			},
			change(e) {
				console.log("e:", e);
			},
			handleTap(item) {
				console.log('Tap event triggered:', item);
			}
		},
	};
</script>

<style>
	.uni-navbar {
		margin-top: -500rpx;
	}

	.uni-navbar__content {
		border: 0 none !important;
	}

	.nav_leftview {
		display: flex;
		align-items: center;
	}

	.scenic_pick {
		width: 150px;
	}

	picker {
		width: 110px;
		height: 40px;
		font-size: 13px;
		background-color: white;
		border-radius: 20px;
		padding-left: 10px;
		/* 垂直居中 */
		display: flex;
		align-items: center;
	}

	swiper {
		/* margin-top: 30px; */
		height: 500rpx;
	}

	.scenic_text {
		width: 118px;
		font-weight: bolder;
		font-family: ui-monospace;
		align-items: center;
	}
	
	.slide-image {
		width: 100%;
		height: 490rpx;
	}

	.notice {
		margin-top: 180px;
	}

	.category {
		margin: 20rpx 0 20rpx;
		padding: 10rpx 0;
		display: flex;
		flex-direction: row;
		justify-content: center;
		flex-wrap: wrap;
		min-height: 128rpx;
	}

	.category-item {
		width: 160rpx;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		box-sizing: border-box;
		margin: 5rpx 8rpx 0;

	}

	.icon {
		width: 90rpx;
		height: 90rpx;
		margin-bottom: 15rpx;
	}

	.text {
		font-size: 26rpx;
		color: #666;
	}

	.futitle {
		background-color: aquamarine;
	}

	.title-more {
		display: flex;
		flex-direction: row;
		justify-content: center;
	}

	.container {
		width: 100%;
		/* 根据需求调整容器宽度 */
		overflow: hidden;
	}

	.hot-image {
		display: inline-block;
		padding: 5px;
		margin-right: 10px;
	}

	.hot-image image {
		height: 390rpx;
	}
</style>
