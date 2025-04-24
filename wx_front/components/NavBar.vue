<template>
	    <uni-nav-bar left-icon="left" shadow fixed status-bar 
		border="false" background-color="#a9dbd0" color="#000" 
		leftWidth="180rpx" right-width="180rpx" @clickLeft="back">
			<!-- <block slot="left" class="nav_leftview" >
				<view class="scenic_pick">
					<picker @change="bindPickerChange" :value="scenic_index" :range="scenic_array">
						<view class="scenic_text">{{scenic_array[scenic_index]}}</view>
					</picker>
					<uni-icons type="arrowdown" color="#666" size="18" />
				</view>
				<uni-icons size="16" type="bottom"></uni-icons>
			</block> -->
			<template #default>
				<view class="navTitle flex-row-centerAll">
					<slot name="title"></slot>
				</view>
			</template>
	    </uni-nav-bar>
</template>

<script>
	export default {
		methods: {
			back() {
				uni.navigateBack({
					delta: 1  // Number of pages to return, 1 means return to the previous page
				})
			}
		}
	}
</script>


<style>
.navTitle{
	width: 100%;
	height: 100%;
	font-size: 32rpx;
	text-align: center;
	margin-top: 15rpx;
}
</style>
