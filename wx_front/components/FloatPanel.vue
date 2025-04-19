<template>
	<view class="floating-panel" v-show="show">
		<view class="panel-content">
			<view v-for="attraction in attractions" :key="attraction.id" class="attraction">
				<view class="attraction-info">
					<view>{{ attraction.name }}</view>
					<img :src="attraction.image" alt="attraction image" />
					<view>距离：{{ attraction.distance }}千米</view>
				</view>
				<button @click="navigateToNavigationPage(attraction)">去这里</button>
			</view>
		</view>
		<button class="close-button" @click="togglePanel">关闭</button>
	</view>
</template>

<script>
	export default {
		props: {
			show: Boolean,
			attractions: Array
		},
		methods: {
			togglePanel() {
				this.$emit('update:show', false);
			},
			navigateToNavigationPage(attraction) {
				// 跳转至导航页面的逻辑，您需要自行实现
			}
		}
	};
</script>

<style scoped>
	.floating-panel {
		position: fixed;
		bottom: 0;
		left: 0;
		width: 100%;
		background-color: #fff;
		border-top: 1px solid #ccc;
		box-shadow: 0 -4px 4px rgba(0, 0, 0, 0.1);
		z-index: 1000;
	}

	.panel-content {
		padding: 10px;
	}

	.attraction {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 10px;
	}

	.attraction img {
		width: 80px;
		height: 80px;
	}

	.close-button {
		display: block;
		width: 100%;
		background-color: #fff;
		border: none;
		text-align: center;
		padding: 10px;
		color: #333;
		font-size: 16px;
		cursor: pointer;
	}
</style>
