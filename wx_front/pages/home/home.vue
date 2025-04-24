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
			<uni-notice-bar show-icon scrollable text="Hong Kong Park Tulip Flower Show has opened reservation channel! Note that opening hours are 8:00-17:00, please plan your visit time accordingly!">
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
						<text>View All</text>
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
			<uni-section class="futitle" title="Featured Routes" titleFontSize="30rpx">
				<template v-slot:right>
					<navigation class="title-more" url="/pages/recommend/recommend">
						<text>View All</text>
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
		
		<!-- Add AI chat floating button -->
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
				scenic_array: ['Victoria Harbour', 'Victoria Peak', 'Disneyland', 'Ocean Park', 'Lamma Island'],
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
					text: 'Map Guide',
					src: '/static/home_menu/map.png',
					opentype: 'switchTab',
				}, {
					id: 2,
					url: '/pages/attraction/attraction',
					text: 'Attraction Info',
					src: '/static/home_menu/info.png',
					opentype: 'navigate',
				}, {
					id: 3,
					url: '/pages/ticket/ticket',
					text: 'Book Tickets',
					src: '/static/home_menu/ticket.png',
					opentype: 'navigate',
				}, {
					id: 4,
					url: '/pages/track/track',
					text: 'History Trail',
					src: '/static/home_menu/track.png',
					opentype: 'switchTab',
				}]

			};
		},
		methods: {
			bindPickerChange: function(e) {
				console.log('picker sends selection change, carrying value', e.detail.value);
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
		width: 120px;
	}

	picker {
		width: 100px;
		font-size: 18px;
	}

	swiper {
		/* margin-top: 30px; */
		height: 500rpx;
	}

	.scenic_text {
		width: 100px;
	}
	
	.slide-image {
		width: 100%;
		height: 500rpx;
	}

	.notice {
		margin-top: 200px;
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
	}

	.icon {
		width: 100rpx;
		height: 100rpx;
	}

	.text {
		font-size: 24rpx;
		margin-top: 10rpx;
	}

	.container {
		margin: 0 36rpx;
	}

	.container-color {
		color: #888;
	}

	.title-more {
		display: flex;
		align-items: center;
		font-size: 26rpx;
		color: #666;
	}

	.title {
		font-weight: bold;
		margin-top: 40rpx;
		margin-bottom: 14rpx;
	}

	.futitle {
		margin-top: 30rpx;
		margin-bottom: 20rpx;
	}

	.hot-image {
		width: 190rpx;
		height: 230rpx;
		margin-right: 28rpx;
		display: inline-block;
	}

	.hot-image image {
		width: 100%;
		height: 100%;
		border-radius: 5px;
	}
</style>
