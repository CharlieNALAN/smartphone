<template>
	<view>
		<NavBar>
			<template slot="title">
				<view>预约详情</view>
			</template>
		</NavBar>
		<view class="col-horizontal-center container">
			<view class="col-ver-center info-container attraction-info">
				<view class="attraction-name">
					<uni-icons type="star-filled" color="orange" size="16"></uni-icons>
					{{ attraction_data.attraction_name }}
				</view>
				<view class="attraction-time">
					景区开放时间：{{ attraction_data.open_time }} - {{ attraction_data.close_time }}
				</view>
			</view>
			<view class="info-container book-info">
				<u-row>
					<u-col span="6">
						<view class="title">预约日期</view>
					</u-col>
					<u-col span="6">
						<uni-datetime-picker type="date" :clear-icon="false" v-model="book_date"
							@maskClick="maskClick" />
					</u-col>
				</u-row>
				<u-line margin="8px 0px" color="white" />
				<u-row>
					<u-col span="6">
						<view class="title">游玩时间</view>
					</u-col>
					<u-col span="6">
						<view class="book-time">
							<picker @change="bindPickerChange" :value="index" :range="array">
								<view :class="{ 'gray-text': index === 0 }">{{array[index]}}</view>
							</picker>
						</view>
					</u-col>
				</u-row>
			</view>
			<view class="info-container visitor-info">
				<u-row>
					<u-col span="8">
						<view class="title">请选择游客</view>
					</u-col>
					<u-col span="4">
						<view class="gray-text" style="font-size: 12px;">最多可添加四位游客</view>
					</u-col>
				</u-row>
				<view v-if="isVisible" v-for="(visitor, index) in visitors" :key="index">
					<u-line margin="10px 0px" color="white" />
					<u-row>
						<u-col span="1">
							<u-icon name="minus-circle" color="#2979ff" size="18" @click="removeVisitor(index)">
							</u-icon>
						</u-col>
						<u-col span="10">
							<view>姓名： {{visitor.name}}</view>
							<view>身份证号： {{visitor.idcard}}</view>
							<view>手机号码： {{visitor.phone}}</view>
						</u-col>
						<u-col span="1">
							<u-icon name="arrow-right" color="#2979ff" size="18"></u-icon>
						</u-col>
					</u-row>
				</view>
				<u-line margin="10px 0px" color="white" />
				<u-button :disabled="visitors.length == 4" text="新增" @click="addTravellers"
					color="radial-gradient(circle, #9890e3, #b1f4cf)">
				</u-button>
			</view>
			<view class="save">
				<u-button :disabled="visitors.length < 1" text="立即预约" @click="saveBook"
					color="linear-gradient(to right, #00c9ff 0%, #92fe9d 100%)">
				</u-button>
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
				book_date: '',
				index: 0,
				array: ['请选择游玩时间', '8:00-10:00', '10:00-12:00', '12:00-14:00', '14:00-16:00', '16:00-18:00'],
				isVisible: false,
				visitors: [], // 存放游玩人信息的数组  
				newVisitor: { // 临时存储新游玩人信息的对象  
					name: '',
					idcard: '',
					phone: ''
				},
			}
		},
		onLoad(options) {
			// const attractionId = options.id; // 获取传递过来的景点id
			const attractionId = 6;
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
		methods: {
			bindPickerChange: function(e) {
				console.log('picker发送选择改变，携带值为', e.detail.value)
				this.index = e.detail.value
			},
			addTravellers() {
				this.$refs.add.open('button')
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
		}
	}
</script>

<style>
	.container {
		width: 100%;
		height: 100vh;
		background: #f4f5f7;
	}

	.info-container {
		width: 93%;
		margin: 10px 0;
		padding: 15px;
		border-radius: 12px;
		background: white;
	}

	.attraction-info {
		height: 100px;
		background: linear-gradient(to right, #00c9ff 0%, #92fe9d 100%);
		color: white;
	}

	.attraction-time {
		margin-top: 10px;
		font-size: 12px;
	}

	.visitor-info,
	.book-info {
		font-size: 14px;
	}
	
	.visitor-info {
		margin-bottom: 100px;
	}

	.book-info {
		height: 110px;
	}

	.gray-text {
		color: gray;
	}

	.form {
		width: 380px;
		margin: 20px;
		padding: 20px;
		background: white;
		border-radius: 10px;
	}
	
	.save {
		width: 93%;
	}
</style>
