<template>
	<view>
		<NavBar>
			<template slot="title">
				<view>景点购票</view>
			</template>
		</NavBar>
		<uni-search-bar placeholder="搜索景点" bgColor="#EEEEEE" @confirm="search" />
		<!-- <view class="card" v-for="item in attractions">
			<van-card num="2" :tag="item.category_text" :price="item.fee" :desc="item.address"
				:title="item.attraction_name" :thumb="imageURL+item.image" thumb-mode="aspectFill">
			</van-card>
		</view> -->
		<uni-card v-for="item in attractions" @click="goToBuyPage(item)">
			<view class="attraction">
				<view class="info">
					<view class="image-info">
						<image :src="imageURL+item.image" mode="aspectFill" />
					</view>
					<view class="main-info">
						<view class="name-info">
							<text style="color: black;">{{ item.attraction_name }}</text>
							<uni-tag class="category-info" :inverted="true" :circle="true" :text="item.category_text"
								type="success" size="mini" />
						</view>
						<view class="add-info">
							<uni-icons type="paperplane-filled" size="13" color="#a9dbd0"></uni-icons>
							<text style="margin-left: 3px;">{{ item.address }}</text>
						</view>
						<view class="sell-info">
							<text style="font-size: 14px; margin-left: 3px;">10万+人已购买</text>
							<view class="fee-info">
								<image class="rmb" src="/static/rmb.png" mode="aspectFill" />
								<text class="fee" style="font-size: 30px;">{{ item.fee}}</text>
							</view>
						</view>
					</view>
				</view>
			</view>
		</uni-card>
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
				// global_scenic_id: getApp().globalData.global_scenic_id,
				global_scenic_id: 1,
				imageURL: 'http://localhost:8000/media/',
				attractions: [],
				category_choices: { // 定义category的映射关系
					1: "自然风光",
					2: "历史遗迹",
					3: "文化遗产",
					4: "娱乐体验"
				},
			}
		},
		mounted() {
			this.getAttractions();
		},
		methods: {
			// 从后端获取景点数据
			getAttractions() {
				uni.request({
					url: `http://localhost:8000/api/get_ticket_attractions?scenic=${this.global_scenic_id}`, // 添加查询参数  
					method: 'GET',
					success: (res) => {
						if (res.statusCode === 200) {
							// 假设后端返回的数据结构没有变化  
							this.attractions = res.data.attractions.map(item => ({
								...item,
								category_text: this.category_choices[item.category]
							}));
						} else {
							console.error('Failed to fetch attractions data');
						}
					},
					fail: (err) => {
						console.error('Failed to fetch attractions data:', err);
					},
				});
			},
			goToBuyPage(item) {
				// 跳转到购票页面，并传递景点信息  
				uni.navigateTo({
					url: '/pages/buy/buy?id=' + item.attraction_id // 假设每个景点有一个唯一的id作为标识  
				});
			}
		}
	}
</script>

<style>
	.attraction {
		height: 95%;
	}

	.info {
		display: flex;
		margin-top: 5px;
	}

	.main-info {
		display: flex;
		flex-direction: column;
	}

	.image-info {
		margin-right: 10px;
	}

	.image-info image {
		width: 100px;
		height: 100px;
		border-radius: 5px;
	}

	.category-info {
		margin-left: 10px;
	}

	.add-info {
		margin-top: 10px;
		font-size: 12px;
	}

	.sell-info {
		margin-top: auto;
		color: #959595;
		font-size: 12px;
		display: flex;
		justify-content: space-between;
		width: 250px;
	}

	.fee-info {
		display: flex;
		align-items: flex-end;
		color: #06dcad;
	}

	.rmb {
		width: 18px;
		height: 18px;
	}
</style>
