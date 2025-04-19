<template>
	<view class="tabbar-container">
		<block>
			<view class="tabbar-item" v-for="(item,index) in tabbarList"
				:class="[item.centerItem ? ' center-item' : '']" @click="changeItem(item)">
				<view class="item-top">
					<image :src="currentItem==item.id?item.selectIcon:item.icon"></image>
				</view>
				<view class="item-bottom" :class="[currentItem==item.id ? 'item-active' : '']">
					<text>{{item.text}}</text>
				</view>
			</view>
		</block>

	</view>
</template>

<script>
	export default {
		props: {
			currentPage: {
				type: Number,
				default: 0
			}
		},
		data() {
			return {
				currentItem: 0,
				tabbarList: [{
					id: 0,
					path: "pages/home/home",
					icon: "../static/tabbar_icon/location.png",
					selectIcon: "../static/tabbar_icon/location-active.png",
					text: "首页",
					centerItem: false
				}, {
					id: 1,
					path: "pages/recommend/recommend",
					icon: "../static/tabbar_icon/fire.png",
					selectedIcon: "../static/tabbar_icon/fire-active.png",
					text: "推荐",
					centerItem: false
				}, {
					id: 2,
					path: "pages/map/map",
					icon: "../static/tabbar_icon/flag.png",
					selectIcon: "../static/tabbar_icon/flag-active.png",
					text: "地图",
					centerItem: true
				}, {
					id: 3,
					path: "pages/track/track",
					icon: "../static/tabbar_icon/flag.png",
					selectIcon: "../static/tabbar_icon/flag-active.png",
					text: "足迹",
					centerItem: false
				}, {
					id: 4,
					path: "pages/user/user",
					icon: "../static/tabbar_icon/user.png",
					selectIcon: "../static/tabbar_icon/user-active.png",
					text: "我的",
					centerItem: false
				}]

			};
		},
		mounted() {
			this.currentItem = this.currentPage;
			uni.hideTabBar();
		},
		methods: {
			changeItem(item) {
				let _this = this;
				//_this.currentItem = item.id;  
				uni.switchTab({
					url: item.path
				});
				console.log(item.path)
			}
		}
	}
</script>
<style>
	view {
		padding: 0;
		margin: 0;
		box-sizing: border-box;
	}

	.tabbar-container {
		position: fixed;
		bottom: 0;
		left: 0;
		width: 100%;
		height: 110rpx;
		/* box-shadow: 0 0 5px #999;  */
		box-shadow: 0px 3px 20px rgba(0, 0, 0, 0.16);
		border-top: 1px;
		display: flex;
		align-items: center;
		padding: 5rpx 0;
		color: #999999;
		z-index: 200;
		background-color: #fff;
	}

	.tabbar-container .tabbar-item {
		width: 20%;
		height: 100rpx;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		text-align: center;
	}

	.tabbar-container .item-active {
		color: #1AD080;
	}

	.tabbar-container .center-item {
		display: block;
		position: relative;
	}

	.tabbar-container .tabbar-item .item-top {
		width: 54rpx;
		height: 54rpx;
		padding: 0rpx;
	}

	.tabbar-container .center-item .item-top {
		flex-shrink: 0;
		width: 100rpx;
		height: 100rpx;
		position: absolute;
		top: -50rpx;
		left: calc(50% - 50rpx);
		border-radius: 50%;
		box-shadow: 0px 3px 20px rgba(0, 0, 0, 0.16);
		/* box-shadow: 0 0 5px #999;  */
		background-color: #ffffff;
		padding: 10rpx;
	}

	.tabbar-container .tabbar-item .item-top image {
		width: 100%;
		height: 100%;
	}

	tabbar-container .tabbar-item:nth-child(3) .item-top image {
		background: #ff0000;
	}

	.tabbar-container .tabbar-item .item-bottom {
		font-size: 28rpx;
		width: 100%;
	}

	.tabbar-container .center-item .item-bottom {
		position: absolute;
		bottom: 5rpx;
	}
</style>
