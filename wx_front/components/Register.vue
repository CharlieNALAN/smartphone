<template>
	<view>
		<view class="container" :style="'height:'+ show_screen_height + 'px;'">
			<image class="screen" :src="backimg_src"
				:style="'height:'+ show_screen_height + 'px;' +'width: 100%;z-index: -1;'" mode="scaleToFill"></image>
			<view class="login" v-if="isLogin">
				<u-line margin="10px 0 0 0" color="white" />
				<uni-title type="h2" title="Welcome! Please login～" align="center"></uni-title>
				<view class="lr-form">
					<uni-forms ref="baseForm" :modelValue="loginData">
						<uni-forms-item label="Phone">
							<uni-easyinput v-model="loginData.phone" placeholder="Please enter your phone number" />
						</uni-forms-item>
						<uni-forms-item label="Password">
							<uni-easyinput type="password" v-model="loginData.password" placeholder="Please enter your password" />
						</uni-forms-item>
					</uni-forms>
					<view class="button-group">
						<button class="login-btn" size="mini" @click="login">Login</button>
						<button class="register-btn" size="mini" @click="isRegister=true">Register</button>
					</view>
				</view>
			</view>
			<view class="register" v-if="isRegister">
				<uni-title type="h2" title="No account yet? Please register～" align="center"></uni-title>
				<view class="lr-form">
					<uni-forms ref="baseForm" :modelValue="registerData">
						<uni-forms-item label="Username">
							<uni-easyinput v-model="registerData.username" placeholder="Please enter your username" />
						</uni-forms-item>
						<uni-forms-item label="Phone">
							<view class="form-item">
								<uni-easyinput v-model="registerData.phone" placeholder="Please authorize your phone number" :disabled="isGettingPhone" />
								<button style="margin-left: 10px;" size="mini" open-type="getPhoneNumber"
									@getphonenumber="getUserPhone" :loading="isGettingPhone">Authorize</button>
								<!-- <button style="margin-left: 5px;" size="mini" type="default" @click="showPhoneInputDialog">手动输入</button> -->
							</view>
							<view v-if="isDemoMode" class="demo-tag">
								<text>Demo Mode</text>
							</view>
						</uni-forms-item>
						<uni-forms-item label="Password">
							<uni-easyinput type="password" v-model="registerData.password" placeholder="Please enter your password" />
						</uni-forms-item>
					</uni-forms>
					<view class="button-group">
						<button class="login-btn" size="mini" @click="register">Register</button>
						<button class="register-btn" size="mini" @click="isRegister=false">Back</button>
					</view>
				</view>
			</view>

		</view>
	</view>
</template>

<script>
	export default {
		name: "register",
		data() {
			return {
				backimg_src: getApp().globalData.resourceURL + '/media/welcome.png',
				show_screen_height: getApp().globalData.windowHeight,
				loginData: {
					phone: '', // 注意：这里只是模拟输入，真实环境中需要通过微信API获取  
					password: '',
				},
				registerData: {
					username: '',
					phone: '', // 将从微信API获取
					password: '',
				},
				isLogin: true,
				isRegister: false,
				isGettingPhone: false, // 控制按钮加载状态
				isDemoMode: true, // 演示模式开关，演示时设为true
				demoPhones: ['13812345678', '15987654321', '18123456789', '17012345678', '13987654321'], // 演示用的手机号
			};
		},
		methods: {
			// 获取用户手机号
			getUserPhone(e) {
				// 记录回调信息
				console.log("微信手机号授权回调:", JSON.stringify(e.detail));
				
				// 检测授权失败情况 - 针对演示模式
				if (this.isDemoMode && (!e.detail.code || e.detail.errMsg.indexOf('fail') > -1)) {
					console.log("检测到演示模式，使用模拟手机号");
					this.simulateGetPhone();
					return;
				}
				
				// 正常授权流程 - 真实环境使用
				// 检查是否获取到code
				if (!e.detail.code) {
					console.error("未获取到授权code");
					uni.showToast({
						title: 'Authorization failed, please try again',
						icon: 'none'
					});
					return;
				}
				
				this.isGettingPhone = true; // 设置加载状态
				
				// 调用后端接口获取手机号
				uni.request({
					url: 'http://localhost:8000/api/user/get_phone_number',
					method: 'POST',
					data: {
						code: e.detail.code,
						// 如果还有encryptedData和iv，也要传给后端
						// 但新版本的微信小程序API中，这些数据可能已经不再直接提供
					},
					success: (res) => {
						console.log('获取手机号响应:', JSON.stringify(res.data));
						
						if (res.statusCode === 200 && res.data.phoneNumber) {
							// 成功获取到手机号
							this.registerData.phone = res.data.phoneNumber;
							uni.showToast({
								title: '手机号获取成功',
								icon: 'success'
							});
						} else {
							// 获取手机号失败
							console.error("获取手机号失败:", res.data);
							uni.showToast({
								title: res.data.message || 'Failed to get phone number, please try again',
								icon: 'none',
								duration: 3000
							});
						}
					},
					fail: (err) => {
						console.error('获取手机号请求失败:', JSON.stringify(err));
						uni.showToast({
							title: 'Network request failed, please check the network',
							icon: 'none',
							duration: 3000
						});
					},
					complete: () => {
						this.isGettingPhone = false;
					}
				});
			},
			
			// 模拟获取手机号 - 仅用于演示
			simulateGetPhone() {
				this.isGettingPhone = true;
				
				// 显示加载提示，模拟网络请求
				uni.showLoading({
					title: 'Getting phone number...'
				});
				
				// 模拟网络延迟
				setTimeout(() => {
					// 随机选择一个演示手机号或生成一个随机手机号
					const randomIndex = Math.floor(Math.random() * this.demoPhones.length);
					this.registerData.phone = this.demoPhones[randomIndex];
					
					// 隐藏加载提示
					uni.hideLoading();
					
					// 显示成功提示
					uni.showToast({
						title: 'Simulated ok',
						icon: 'success'
					});
					
					this.isGettingPhone = false;
				}, 1500); // 模拟1.5秒的网络延迟
			},
			

			login() {
				// 表单验证
				if (!this.loginData.phone || !this.loginData.password) {
					uni.showToast({
						title: 'Please fill in all infor',
						icon: 'none'
					});
					return;
				}
				
				// 显示加载状态
				uni.showLoading({
					title: 'Logging in...'
				});
				
				// 发送网络请求到后端进行登录验证
				uni.request({
					url: 'http://localhost:8000/api/user/login',
					method: 'POST',
					data: {
						phone: this.loginData.phone,
						password: this.loginData.password
					},
					success: res => {
						// 隐藏加载提示
						uni.hideLoading();
						
						console.log('登录响应:', res.data);
						
						if (res.data.status === 'success') {
							// 登录成功，保存用户信息到全局状态
							if (res.data.user) {
								// 将用户信息存储到全局数据
								const app = getApp();
								if (app.globalData) {
									app.globalData.userInfo = res.data.user;
									console.log('已将用户信息保存到全局变量:', app.globalData.userInfo);
								} else {
									console.error('globalData未定义');
								}
								
								// 保存到本地存储，下次启动时自动登录
								uni.setStorageSync('userInfo', JSON.stringify(res.data.user));
								console.log('已将用户信息保存到本地存储');
							}
							
							// 显示成功提示
							uni.showToast({
								title: 'Login!',
								icon: 'success',
								duration: 1500
							});
							
							// 通知父组件登录成功
							setTimeout(() => {
								this.$emit('loginSuccess');
							}, 1500);
						} else {
							// 登录失败，显示具体错误信息
							let errorMsg = 'Login failed';
							
							if (res.data.message) {
								if (res.data.message.includes('phone')) {
									errorMsg = 'The phone number has not been registered';
								} else if (res.data.message.includes('password')) {
									errorMsg = 'Wrong password';
								} else {
									errorMsg = res.data.message;
								}
							}
							
							uni.showToast({
								title: errorMsg,
								icon: 'none',
								duration: 2000
							});
						}
					},
					fail: err => {
						// 隐藏加载提示
						uni.hideLoading();
						
						// 请求失败，可能是网络问题
						console.error('Login request failed', err);
						uni.showToast({
							title: 'Network connection failed, please check the network',
							icon: 'none',
							duration: 2000
						});
					}
				});
			},
			// 注册用户  
			register() {
				if (!this.registerData.username || !this.registerData.phone || !this.registerData.password) {
					uni.showToast({
						title: 'Please fill in all infor',
						icon: 'none'
					});
					return;
				}
				
				// 显示加载状态
				// uni.showLoading({
				// 	title: 'Registering...'
				// });
				
				// 发送注册请求
				uni.request({
					url: 'http://localhost:8000/api/user/register', // 假设的后端接口地址  
					method: 'POST',
					data: {
						username: this.registerData.username,
						phone: this.registerData.phone, // 真实环境中应该发送encryptedData给后端解密  
						password: this.registerData.password
					},
					success: (res) => {
						// 隐藏加载提示
						uni.hideLoading();
						
						console.log('注册响应:', res.data);
						
						if (res.data.code === 0) {
							// 注册成功
							// 如果注册接口同时返回了用户信息，可以直接保存
							if (res.data.user) {
								// 将用户信息存储到全局数据
								const app = getApp();
								if (app.globalData) {
									app.globalData.userInfo = res.data.user;
									console.log('已将用户信息保存到全局变量:', app.globalData.userInfo);
								}
								
								// 保存到本地存储
								uni.setStorageSync('userInfo', JSON.stringify(res.data.user));
								console.log('已将用户信息保存到本地存储');
							}
							
							this.isLogin = true;
							this.isRegister = false;
							
							uni.showToast({
								title: 'Registered!',
								icon: 'success'
							});
						} else {
							// 注册失败
							uni.showToast({
								title: 'Register failed: ' + (res.data.message || 'Unknown error'),
								icon: 'none',
								duration: 3000
							});
						}
					},
					fail: (err) => {
						// 隐藏加载提示
						uni.hideLoading();
						
						console.error('注册请求失败:', err);
						uni.showToast({
							title: 'Network request failed, please check the network',
							icon: 'none',
							duration: 3000
						});
					}
				});
			}
		}
	};
</script>

<style>
	.container {
		width: 100%;
	}

	.login,
	.register {
		position: absolute;
		left: 50%;
		bottom: 20%;
		transform: translate(-50%, -50%);
		background-color: white;
		width: 320px;
		height: 320px;
		border-radius: 20px;
	}

	.lr-form {
		/* width: 90%; */
		padding: 20px;
	}

	.form-item {
		display: flex;
		align-items: center;
	}

	.button-group {
		margin-top: 30px;
		display: flex;
		justify-content: space-around;
	}

	.login-btn {
		background: linear-gradient(to top, #96fbc4 0%, #f9f586 100%);
		/* color: white; */
	}

	.register-btn {
		background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
	}
	
	/* 演示模式标记样式 */
	.demo-tag {
		margin-top: 5px;
		display: inline-block;
		font-size: 12px;
		color: #ff7f50;
		background-color: rgba(255, 127, 80, 0.1);
		padding: 2px 8px;
		border-radius: 10px;
		border: 1px dashed #ff7f50;
	}
</style>
