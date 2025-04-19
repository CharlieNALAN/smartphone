<template>
	<view>
		<NavBar>
			<template slot="title">
				<view>购票详情</view>
			</template>
		</NavBar>
		<view class="container">
			<uni-card class="name-date" :is-shadow="false">
				<u-line margin="5px 0 0 0" color="white" />
				<view class="title">{{attraction_data.attraction_name}}</view>
				<u-line margin="15px 0px" color="lightgrey" />
				<view class="title">游玩日期</view>
				<u-line margin="6px 0" color="white" />
				<uni-datetime-picker type="date" :clear-icon="false" v-model="ticket_date" @maskClick="maskClick" />
			</uni-card>
			<uni-card :is-shadow="false">
				<u-line margin="5px 0 0 0" color="white" />
				<u-row>
					<u-col span="10">
						<view class="title" style="font-size: 20px;">单日票</view>
					</u-col>
					<u-col span="2">
						<image class="rmb" src="/static/rmb.png" mode="aspectFill" />
						<text class="fee" style="font-size: 30px;">{{attraction_data.fee}}</text>
					</u-col>
				</u-row>
				<u-line margin="5px 0px" color="white" />
				<u-row>
					<u-col span="9">
						<view>开放时间：{{attraction_data.open_time}} - {{attraction_data.close_time}}</view>
					</u-col>
					<u-col span="3">
						<u-number-box v-model="ticketCount" @change="handleNumberChange"></u-number-box>
					</u-col>
				</u-row>
				<u-line margin="15px 0px" color="lightgrey" />
				<view class="title">填写游玩人</view>
				<u-line margin="5px 0px" color="white" />
				<view v-if="isVisible" v-for="(visitor, index) in visitors" :key="index">
					<u-row>
						<u-col span="1">
							<u-icon name="minus-circle" color="#2979ff" size="18" @click="removeVisitor(index)">
							</u-icon>
						</u-col>
						<u-col span="10">
							<view>姓名 {{visitor.name}}</view>
							<view>身份证号 {{visitor.idcard}}</view>
							<view>手机号码 {{visitor.phone}}</view>
						</u-col>
						<u-col span="1">
							<u-icon name="arrow-right" color="#2979ff" size="18"></u-icon>
						</u-col>
					</u-row>
				</view>
				<u-button :disabled="ticketCount <= visitors.length" text="新增游玩人" @click="addTravellers"
					color="radial-gradient(circle, #9890e3, #b1f4cf)">
				</u-button>
			</uni-card>
		</view>
		<view class="pay">
			<u-row>
				<u-col span="9">
					<text>合计：</text>
					<image class="rmb" src="/static/rmb.png" mode="aspectFill" />
					<text class="fee" style="font-size: 22px;">{{totalFee}}</text>
				</u-col>
				<u-col span="3">
					<u-button text="立即支付" @click="gotoPay" color="linear-gradient(to right, #f9b423, #ff4e50)">
					</u-button>
				</u-col>
			</u-row>
		</view>
		<view>
			<uni-popup ref="add" type="bottom" backgroundColor="#f4f5f7">
					<uni-title type="h2" title="新增游玩人" align="center"></uni-title>
					<view class="col-horizontal-center" style="height: 500px; ">
						<view class="form">
							<u-form @submit.native.prevent="submitForm">
								<u-form-item>
									<u-input type="text" v-model="newVisitor.name" placeholder="与证件姓名一致" border="none">
										<u--text text="中文姓名" slot="prefix" margin="0 15px 0 0"></u--text>
									</u-input>
								</u-form-item>
								<u-form-item>
									<u-input type="idcard" v-model="newVisitor.idcard" placeholder="与证件号码一致"
										border="none">
										<u--text text="身份证号" slot="prefix" margin="0 15px 0 0"></u--text>
									</u-input>
								</u-form-item>
								<u-form-item>
									<u-input type="number" v-model="newVisitor.phone" placeholder="用于接受出行短信"
										border="none">
										<u--text text="手机号码" slot="prefix" margin="0 15px 0 0"></u--text>
									</u-input>
								</u-form-item>
							</u-form>
						</view>
						<view class="hor-ver-center" style="width: 380px; height: 400px;">
							<u-button type="primary" shape="circle" text="保存并使用" @click="submitForm"></u-button>
						</view>
					</view>
				</uni-popup>
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
				attraction_data: {},
				show: false,
				isVisible: false,
				ticketCount: 1,
				ticket_date: '',
				visitors: [], // 存放游玩人信息的数组  
				newVisitor: { // 临时存储新游玩人信息的对象  
					name: '',
					idcard: '',
					phone: ''
				},
				price: 0,
			}
		},
		onLoad(options) {
			const attractionId = options.id; // 获取传递过来的景点id
			
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
		},
		computed: {
			totalFee() {
				const quantity = Number(this.ticketCount) || 1;
				this.price = this.attraction_data.fee * quantity;
				return this.attraction_data.fee * quantity;
			}
		},
		methods: {
			addTravellers() {
				this.$refs.add.open('button')
			},
			handleNumberChange(ticketCount) {
				console.log('当前值为: ' + ticketCount);
				this.ticketCount = ticketCount;
			},
			maskClick(e) {
				console.log('maskClick事件:', e);
			},
			submitForm() {
				if (this.validateForm()) { // 验证表单  
					this.visitors.push({
						...this.newVisitor
					}); // 将新游玩人添加到数组末尾  
					this.newVisitor = {
						name: '',
						idcard: '',
						phone: ''
					}; // 清空输入框  
					this.$refs.add.close(); // 关闭弹窗
					this.isVisible = true;
				} else {
					// 提示用户输入有误  
					uni.showToast({
						title: '输入有误，请检查表单信息',
						icon: 'none'
					});
				}
			},
			// 验证表单  
			validateForm() {
				let isValid = true;
				if (!this.newVisitor.name) {
					uni.showToast({
						title: '姓名不能为空',
						icon: 'none'
					});
					isValid = false;
				}
				if (!this.newVisitor.idcard) {
					uni.showToast({
						title: '身份证号不能为空',
						icon: 'none'
					});
					isValid = false;
				}
				if (!this.newVisitor.phone) {
					uni.showToast({
						title: '手机号不能为空',
						icon: 'none'
					});
					isValid = false;
				}
				// 可以添加更多的验证逻辑，比如身份证号格式验证、手机号格式验证等  
				return isValid;
			},
			// 处理表单提交事件  
			addVisitor(e) {
				e.preventDefault(); // 阻止表单默认提交行为  
				this.submitForm(); // 调用提交表单的方法  
			},
			removeVisitor(index) {
				// 使用 splice 方法从数组中移除指定索引的元素  
				this.visitors.splice(index, 1);
			},
			async gotoPay() {
				const ticketData = {
					user: 1,
					attraction: this.attraction_data.attraction_id,
					ticket_date: this.ticket_date,
					ticket_count: this.visitors.length,
					price: this.price,
					visitors: this.visitors
				};
				console.log(ticketData);
				try {
					const res = await uni.request({
						url: 'http://localhost:8000/ticket/',
						method: 'POST',
						data: ticketData,
						header: {
							'content-type': 'application/json', // 默认值  
							// 如果后端需要身份验证，可以在这里添加token等  
							// 'Authorization': 'Bearer ' + token  
						},
						success: (response) => {
							console.log('创建订单成功:', response.data);
						},
						fail: (error) => {
							// 请求失败处理  
							console.error('请求失败:', error);
							// 显示错误信息给用户  
						}
					});
				} catch (error) {
					// 捕获async/await中的错误  
					console.error('请求发生错误:', error);
					// 显示错误信息给用户  
				}
			}
		}
	}
</script>

<style>
	.title {
		color: black;
		font-size: 18px;
	}

	.container {
		width: 100%;
	}

	uni-card .uni-card {
		border-radius: 15px;
	}

	.name-date text {
		font-size: 18px;
		color: black;
	}

	.row-two .view {
		margin-top: 20px;
	}

	.rmb {
		width: 18px;
		height: 18px;
	}

	.form {
		width: 380px;
		margin: 20px;
		padding: 20px;
		background: white;
		border-radius: 10px;
	}

	.pay {
		height: 100px;
		padding: 10px 15px;
		position: fixed;
		bottom: 0;
		width: 100%;
		left: 0;
		z-index: -999;
		box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
	}

	.fee {
		color: #06dcad;
		font-weight: bold;
	}
</style>
