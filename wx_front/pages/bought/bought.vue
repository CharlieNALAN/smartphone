<template>
	<view>
		<NavBar>
			<template slot="title">
				<view>我的门票</view>
			</template>
		</NavBar>
		<view class="tabs-container">
			<view class="tabs">
				<view class="tab" :class="{ active: currentTab === 'all' }" @click="switchTab('all')">全部</view>
				<view class="tab" :class="{ active: currentTab === 'pending' }" @click="switchTab('pending')">
					<text>待支付</text>
					<uni-badge v-if="pendingCount > 0" :text="pendingCount" absolute="rightTop" :offset="[-5, -10]"></uni-badge>
				</view>
				<view class="tab" :class="{ active: currentTab === 'paid' }" @click="switchTab('paid')">已支付</view>
			</view>
			<view class="tab-content">
				<view v-if="currentTab === 'all'">
					<uni-card v-for="item in tickets">
						<template v-slot:title>
							<view>
								<view class="info">
									<view class="image-info">
										<image :src="global_url+item.attraction.image" mode="aspectFill" />
									</view>
									<view class="main-info junyun">
										<view class="name-info junyun">
											<view class="name-container">
												<text
													style="color: black;">{{ item.attraction.attraction_name }}门票</text>
											</view>
											<view class="count-container">
												<text style="color: black;">x{{ item.ticket_count }}</text>
											</view>
										</view>
										<view class="other-info junyun">
											<text
												style="font-size: 14px; margin-left: 3px; color: grey;">使用日期：{{ item.ticket_date }}</text>
											<uni-tag class="status" :inverted="true" :circle="true"
												:text="item.status_text" :type="item.status_text === '待支付' ? 'error' :   
												item.status_text === '已支付' ? 'success' :   
												item.status_text === '已完成' ? 'primary' :   
												item.status_text === '已取消' ? 'default' :   
												'default'" size="mini" />
										</view>
										<view class="nav kaoyou">
										    <uni-tag :text="item.status === 0 ? '前往支付' : '查看详情'" type="warning" style="margin-left: 15px;" @click="item.status === 0 ? navto_pay(item.ticket_id) : navto_detail(item.ticket_id)"></uni-tag>
										</view>
									</view>
								</view>
							</view>
						</template>
						<u-line color="lightgrey" />
						<u-line margin="3px 0px" color="white" />
						<text>购买好门票后请提前安排好行程，避免门票失效喔～</text>
					</uni-card>
				</view>
				<view v-if="currentTab === 'pending'">
					<uni-card v-for="item in tickets">
						<template v-slot:title>
							<view>
								<view class="info">
									<view class="image-info">
										<image :src="global_url+item.attraction.image" mode="aspectFill" />
									</view>
									<view class="main-info junyun">
										<view class="name-info junyun">
											<view class="name-container">
												<text
													style="color: black;">{{ item.attraction.attraction_name }}门票</text>
											</view>
											<view class="count-container">
												<text style="color: black;">x{{ item.ticket_count }}</text>
											</view>
										</view>
										<view class="other-info junyun">
											<text
												style="font-size: 14px; margin-left: 3px; color: grey;">使用日期：{{ item.ticket_date }}</text>
											<uni-tag class="status" :inverted="true" :circle="true"
												:text="item.status_text" :type="item.status_text === '待支付' ? 'error' :   
												item.status_text === '已支付' ? 'success' :   
												item.status_text === '已完成' ? 'primary' :   
												item.status_text === '已取消' ? 'default' :   
												'default'" size="mini" />
										</view>
										<view class="nav kaoyou">
											<uni-tag text="前往支付" type="warning" style="margin-left: 15px;"
												@click="navto_pay(item.ticket_id)"></uni-tag>
										</view>
									</view>
								</view>
							</view>
						</template>
						<u-line color="lightgrey" />
						<u-line margin="3px 0px" color="white" />
						<text>购买好门票后请提前安排好行程，避免门票失效喔～</text>
					</uni-card>
				</view>
				<view v-if="currentTab === 'paid'">
					<uni-card v-for="item in tickets">
						<template v-slot:title>
							<view>
								<view class="info">
									<view class="image-info">
										<image :src="global_url+item.attraction.image" mode="aspectFill" />
									</view>
									<view class="main-info junyun">
										<view class="name-info junyun">
											<view class="name-container">
												<text
													style="color: black;">{{ item.attraction.attraction_name }}门票</text>
											</view>
											<view class="count-container">
												<text style="color: black;">x{{ item.ticket_count }}</text>
											</view>
										</view>
										<view class="other-info junyun">
											<text
												style="font-size: 14px; margin-left: 3px; color: grey;">使用日期：{{ item.ticket_date }}</text>
											<uni-tag class="status" :inverted="true" :circle="true"
												:text="item.status_text" :type="item.status_text === '待支付' ? 'error' :   
												item.status_text === '已支付' ? 'success' :   
												item.status_text === '已完成' ? 'primary' :   
												item.status_text === '已取消' ? 'default' :   
												'default'" size="mini" />
										</view>
										<view class="nav kaoyou">
											<uni-tag text="查看详情" type="warning" style="margin-left: 15px;"
												@click="navto_detail(item.attraction_id)"></uni-tag>
										</view>
									</view>
								</view>
							</view>
						</template>
						<u-line color="lightgrey" />
						<u-line margin="3px 0px" color="white" />
						<text>购买好门票后请提前安排好行程，避免门票失效喔～</text>
					</uni-card>
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
				global_url: getApp().globalData.resourceURL,
				tickets: [], // 存储门票数据的数组  
				currentTab: 'all', // 当前选中的标签  
				tabStatuses: { // tab 对应的数字标识  
					'all': null, // 'all' 标识对应所有门票数据，所以这里用 null  
					'pending': 0, // 'pending' 标识对应待支付门票数据  
					'paid': 1 // 'paid' 标识对应已支付门票数据  
				},
				status_choices: { // 定义status的映射关系
					0: "待支付",
					1: "已支付",
					2: "已完成",
					3: "已取消"
				},
				pendingCount: 0,
			};
		},
		mounted() {
			this.fetchTickets(this.tabStatuses[this.currentTab]);
		},
		methods: {
			switchTab(tab) {
				this.currentTab = tab; // 更新当前选中的标签  
				const status = this.tabStatuses[tab]; // 获取对应 tab 的状态标识  
				this.fetchTickets(status); // 加载对应状态的门票数据  
			},
			fetchTickets(status) {
				let url = 'http://localhost:8000/ticket';
				if (status !== null) {
					url += '?status=' + status; // 根据传入的 status 参数添加查询条件  
				}
				uni.request({
					url: url,
					method: 'GET',
					success: (res) => {
						if (res.data && res.data.length > 0) {
							this.tickets = res.data.map(item => ({
								...item,
								status_text: this.status_choices[item.status]
							}));
							this.fetchTicketDetails();
							if(status != 1) {
								this.pendingCount = this.tickets.filter(item => item.status === 0).length;
							}
						} else {
							this.tickets = [];
							uni.showToast({
								title: '暂无数据',
								icon: 'none'
							});
						}
					},
					fail: (error) => { // 注意这里使用fail代替catch，因为uni.request使用的是fail来处理错误  
						console.error(error);
						uni.showToast({
							title: '加载失败',
							icon: 'none'
						});
					}
				});
			},
			fetchTicketDetails() {
				this.tickets.forEach((ticket, index) => {
					uni.request({
						url: `http://localhost:8000/ticket/${ticket.ticket_id}`, // 替换为实际的后端 URL
						method: 'GET',
						success: (res) => {
							if (res.data) {
								this.$set(this.tickets, index, {
									...ticket,
									attraction: res.data.attraction
								}); // 将景点数据添加到对象中
							}
						},
						fail: (err) => {
							console.error('Failed to fetch details for ticket:', err);
						}
					});
				});
				console.log(this.tickets);
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
		padding: 0 10px;
	}

	.info {
		display: flex;
		align-items: center;
		margin-top: 10px;
	}

	.status-info {
		margin: 5px 0;
	}

	.image-info image {
		width: 90px;
		height: 90px;
	}

	.main-info {
		flex-direction: column;
		/* 子元素垂直排列 */
		margin: 0 10px;
		width: 320px;
	}

	.name-info {
		margin-bottom: 5px;
		align-items: center;
	}

	.name-info text {
		margin-right: 10px;
	}

	.count-container {
		/* 这里也可以添加其他样式，比如字体大小、边距等 */
		text-align: right;
		/* 虽然在微信小程序中这个属性可能不生效，但你可以保留它作为占位符 */
	}

	.nav {
		width: 100%;
		margin-top: 10px;
	}
</style>
