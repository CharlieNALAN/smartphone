<template>
	<view>
		<NavBar>
			<template slot="title">
				<view>我的预约</view>
			</template>
		</NavBar>
		<view class="tabs-container">
			<view class="tabs">
				<text class="tab" :class="{ active: currentTab === 'all' }" @click="switchTab('all')">全部</text>
				<text class="tab" :class="{ active: currentTab === 'pending' }" @click="switchTab('pending')">待支付</text>
				<text class="tab" :class="{ active: currentTab === 'paid' }" @click="switchTab('paid')">已支付</text>
			</view>
			<view class="tab-content">
				<view v-if="currentTab === 'all'">
				</view>
				<view v-if="currentTab === 'pending'">
					<!-- 显示待支付门票信息 -->
					<text>待支付门票内容...</text>
				</view>
				<view v-if="currentTab === 'paid'">
					<!-- 显示已支付门票信息 -->
					<text>已支付门票内容...</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import NavBar from "../../components/NavBar.vue";

	export default {
		components: {
			NavBar,
		},
		data() {
			return {
				currentTab: 'all', // 默认选中的选项卡  
				// 你可以在这里添加你的门票数据  
				books: {
					all: [],
					booked: [],
					finished: [],
					expire: [],
				},
			};
		},
		methods: {
			switchTab(tab) {
				this.currentTab = tab;
			},
		},
	};
</script>

<style>
	.tabs-container {
		display: flex;
		flex-direction: column;
	}

	.tabs {
		display: flex;
		justify-content: space-between;
		/* 使tabs均匀分布 */
		align-items: center;
		background-color: #fff;
		/* 可以设置背景色 */
		padding: 10px 0;
		/* 上下内边距 */
	}

	.tab {
		flex: 1;
		/* 使每个tab占据等量的空间 */
		text-align: center;
		/* 文字居中 */
		padding: 10px 0;
		/* 上下内边距 */
		cursor: pointer;
		font-size: 16px;
		/* 字体大小 */
	}

	.tab.active {
		color: #007aff;
		/* 选中时的文字颜色 */
		border-bottom: 2px solid #007aff;
		/* 选中时的底部边框 */
	}

	.tab-content {
		margin-top: 20px;
		padding: 10px;
	}
</style>
