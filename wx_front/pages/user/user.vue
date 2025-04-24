<template>
	<view>
		<NavBar>
			<template slot="title">
				<view>Profile</view>
			</template>
		</NavBar>
		<view class="container_head">
			<view class="head_pers_info" bindtap="head_pers_info">
				<view class="head_pic">
					<image class="head_pic_content" mode="aspectFit" src="http://localhost:8000/media/user.jpg"></image>
				</view>
				<view class="inf_content">
					<view class="user-row">
						<view class="user-info-container">
							<text class="user_info">{{ userInfo.username || 'Guest' }}</text>
							<view v-if="isLoggedIn" class="user-badge">
								<uni-icons type="checkmarkempty" size="12" color="#fff"></uni-icons>
								<text>Verified</text>
							</view>
							<view v-else class="guest-badge">
								<uni-icons type="info" size="12" color="#fff"></uni-icons>
								<text>Not Logged In</text>
							</view>
						</view>
						<button v-if="!isLoggedIn" class="login-btn" size="mini" @click="showLoginPopup">
							<text>Login</text>
							<uni-icons type="arrowright" size="14" color="#333"></uni-icons>
						</button>
					</view>
					<view class="user-detail" v-if="isLoggedIn">
						<view class="phone-info">
							<uni-icons type="phone" size="14" color="#fff"></uni-icons>
							<text class="phone-text">{{ userInfo.phone }}</text>
						</view>
						<view class="user-id">
							<text>ID: {{ userInfo.id || userInfo.user_id }}</text>
						</view>
					</view>
					<view v-else class="guest-info">
						<view class="guest-tip">
							<uni-icons type="info" size="14" color="rgba(255,255,255,0.8)"></uni-icons>
							<text>Login to access more features</text>
						</view>
					</view>
				</view>
			</view>
		</view>
		<view class="category">
			<navigator class="category-item" hover-class="none" :url="item.url" v-for="item in menuList" :key="item.id"
				:open-type="item.opentype">
				<image class="icon" :src="menu_url + item.src"></image>
				<text class="text">{{item.text}}</text>
			</navigator>
		</view>
		<view class="list">
			<uni-list>
				<uni-list-item showArrow>
					<template v-slot:body>
						<view class="list_item_contain">
							<uni-icons type="person-filled" size="28"></uni-icons>
							<text>Personal Information</text>
						</view>
					</template>
				</uni-list-item>
				<uni-list-item showArrow clickable="true" @click="guidesign_dialog()">
					<template v-slot:body>
						<view class="list_item_contain">
							<uni-icons type="compose" size="28"></uni-icons>
							<text>Guide Application</text>
						</view>
					</template>
				</uni-list-item>
				<uni-list-item showArrow>
					<template v-slot:body>
						<view class="list_item_contain">
							<uni-icons type="more" size="28"></uni-icons>
							<text>About App</text>
						</view>
					</template>
				</uni-list-item>
				<uni-list-item showArrow>
					<template v-slot:body>
						<view class="list_item_contain">
							<uni-icons type="help" size="28"></uni-icons>
							<text>Get Help</text>
						</view>
					</template>
				</uni-list-item>
				<uni-list-item showArrow clickable="true" @click="logout()" v-if="isLoggedIn">
					<template v-slot:body>
						<view class="list_item_contain">
							<uni-icons type="closeempty" size="28" color="#dd524d"></uni-icons>
							<text class="logout-text">Logout</text>
						</view>
					</template>
				</uni-list-item>
			</uni-list>
		</view>
		<view>
			<uni-popup ref="inputDialog" type="dialog">
				<uni-popup-dialog ref="inputClose" mode="input" title="Enter Invitation Code" placeholder="Please enter content"
					@confirm="dialogInputConfirm">
				</uni-popup-dialog>
			</uni-popup>
		</view>
		<view class="last_view"></view>
		
		<!-- Login Popup -->
		<uni-popup ref="loginPopup" type="center">
			<view class="login-popup">
				<view class="login-title">Account Login</view>
				<view class="login-form">
					<view class="input-item">
						<text class="input-label">Phone</text>
						<input type="number" v-model="loginForm.phone" placeholder="Enter phone number" maxlength="11" />
					</view>
					<view class="input-item">
						<text class="input-label">Password</text>
						<input type="password" v-model="loginForm.password" placeholder="Enter password" />
					</view>
					<view class="login-btns">
						<button class="submit-btn" :loading="isLogging" @click="handleLogin">Login</button>
						<button class="cancel-btn" @click="closeLoginPopup">Cancel</button>
					</view>
				</view>
			</view>
		</uni-popup>
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
				menu_url: 'http://localhost:8000/media/usercenter/',
				userInfo: {
					username: '',
					phone: ''
				},
				isLoggedIn: false,
				isLogging: false,
				loginForm: {
					phone: '',
					password: ''
				},
				menuList: [{
					id: 1,
					url: '/pages/bought/bought',
					text: 'My Tickets',
					src: 'menpiao.png',
					opentype: 'navigate',
				}, {
					id: 2,
					url: '/pages/booked/booked',
					text: 'My Bookings',
					src: 'yuyue.png',
					opentype: 'navigate',
				}, {
					id: 3,
					url: '/pages/map/map',
					text: 'Order History',
					src: 'suoyou.png',
					opentype: 'navigate',
				}, {
					id: 4,
					url: '/pages/track/track',
					text: 'Message Center',
					src: 'xiaoxi.png',
					opentype: 'navigate',
				}]
			}
		},
		onShow() {
			// Get latest user info each time page is shown
			this.getUserInfo();
		},
		methods: {
			// Show login popup
			showLoginPopup() {
				// Clear form
				this.loginForm = {
					phone: '',
					password: ''
				};
				this.$refs.loginPopup.open();
			},
			
			// Close login popup
			closeLoginPopup() {
				this.$refs.loginPopup.close();
			},
			
			// Handle login
			handleLogin() {
				// Form validation
				if (!this.loginForm.phone) {
					uni.showToast({
						title: 'Please enter phone number',
						icon: 'none'
					});
					return;
				}
				if (!this.loginForm.password) {
					uni.showToast({
						title: 'Please enter password',
						icon: 'none'
					});
					return;
				}
				
				this.isLogging = true;
				
				// Send login request
				uni.request({
					url: getApp().globalData.resourceURL + 'login/',
					method: 'POST',
					data: {
						phone: this.loginForm.phone,
						password: this.loginForm.password
					},
					success: (res) => {
						if (res.statusCode === 200 && res.data.code === 0) {
							// Login successful
							this.userInfo = res.data.data;
							this.isLoggedIn = true;
							
							// Save user info to local storage
							try {
								uni.setStorageSync('userInfo', JSON.stringify(this.userInfo));
								
								// Assign to global variable
								getApp().globalData.userInfo = this.userInfo;
								
								uni.showToast({
									title: 'Login successful',
									icon: 'success'
								});
								
								// Close popup
								this.closeLoginPopup();
								
							} catch (e) {
								console.error('Failed to save user info', e);
							}
						} else {
							// Login failed
							uni.showToast({
								title: res.data.msg || 'Login failed, please try again',
								icon: 'none'
							});
						}
					},
					fail: (err) => {
						console.error('Login request failed', err);
						uni.showToast({
							title: 'Network error, please try again',
							icon: 'none'
						});
					},
					complete: () => {
						this.isLogging = false;
					}
				});
			},
			
			// Get user info
			getUserInfo() {
				try {
					const userInfoStr = uni.getStorageSync('userInfo');
					if (userInfoStr) {
						this.userInfo = JSON.parse(userInfoStr);
						this.isLoggedIn = true;
						console.log('Loaded user info from storage:', this.userInfo);
					} else {
						this.userInfo = {
							username: '',
							phone: ''
						};
						this.isLoggedIn = false;
					}
				} catch (e) {
					console.error('Failed to get user info', e);
					this.userInfo = {
						username: '',
						phone: ''
					};
					this.isLoggedIn = false;
				}
			},
			
			// Logout
			logout() {
				uni.showModal({
					title: 'Confirm',
					content: 'Are you sure you want to logout?',
					success: (res) => {
						if (res.confirm) {
							// Clear user info
							uni.removeStorageSync('userInfo');
							
							// Clear global variable
							getApp().globalData.userInfo = null;
							
							// Reset page state
							this.userInfo = {
								username: '',
								phone: ''
							};
							this.isLoggedIn = false;
							
							uni.showToast({
								title: 'Logged out successfully',
								icon: 'success'
							});
						}
					}
				});
			},
			
			// Show guide application dialog
			guidesign_dialog() {
				if (!this.isLoggedIn) {
					uni.showToast({
						title: 'Please login first',
						icon: 'none'
					});
					return;
				}
				
				this.$refs.inputDialog.open();
			},
			
			// Handle invitation code confirmation
			dialogInputConfirm(val) {
				if (!val) {
					uni.showToast({
						title: 'Please enter invitation code',
						icon: 'none'
					});
					return;
				}
				
				// Verify invitation code
				uni.request({
					url: getApp().globalData.resourceURL + 'validate_invitation_code/',
					method: 'POST',
					data: {
						user_id: this.userInfo.id || this.userInfo.user_id,
						code: val
					},
					success: (res) => {
						if (res.statusCode === 200 && res.data.valid) {
							uni.showToast({
								title: 'Application submitted successfully',
								icon: 'success'
							});
						} else {
							uni.showToast({
								title: 'Invalid invitation code',
								icon: 'none'
							});
						}
					},
					fail: (err) => {
						console.error('Verification request failed', err);
						uni.showToast({
							title: 'Network error, please try again',
							icon: 'none'
						});
					}
				});
			}
		}
	}
</script>

<style>
	.container_head {
		height: 200rpx;
		margin-top: 100rpx;
		background-color: #3bcb98;
		padding: 30rpx;
		border-radius: 10px;
		margin-left: 30rpx;
		margin-right: 30rpx;
		color: white;
	}

	.head_pers_info {
		display: flex;
		flex-direction: row;
		align-items: center;
	}

	.head_pic {
		width: 100rpx;
		height: 100rpx;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.head_pic_content {
		width: 90rpx;
		height: 90rpx;
		border-radius: 50%;
	}

	.inf_content {
		width: 550rpx;
		margin-left: 20rpx;
	}

	.user-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 10rpx;
	}

	.user-info-container {
		display: flex;
		align-items: center;
	}

	.user_info {
		font-size: 18px;
		font-weight: bold;
		margin-right: 10rpx;
	}

	.user-badge, .guest-badge {
		display: flex;
		align-items: center;
		padding: 2rpx 10rpx;
		border-radius: 15rpx;
		font-size: 10px;
	}

	.user-badge {
		background-color: rgba(255, 255, 255, 0.3);
	}

	.guest-badge {
		background-color: rgba(0, 0, 0, 0.2);
	}

	.login-btn {
		display: flex;
		align-items: center;
		padding: 0 15rpx;
		height: 50rpx;
		line-height: 50rpx;
		background-color: #ffffff;
		border-radius: 25rpx;
		font-size: 12px;
	}

	.user-detail, .guest-info {
		font-size: 12px;
		color: rgba(255, 255, 255, 0.8);
	}

	.phone-info {
		display: flex;
		align-items: center;
		margin-bottom: 5rpx;
	}

	.phone-text {
		margin-left: 5rpx;
	}

	.guest-tip {
		display: flex;
		align-items: center;
	}

	.category {
		margin: 40rpx 0;
		padding: 10rpx 0;
		display: flex;
		flex-direction: row;
		justify-content: center;
		flex-wrap: wrap;
	}

	.category-item {
		width: 25%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		margin-bottom: 20rpx;
	}

	.icon {
		width: 90rpx;
		height: 90rpx;
		margin-bottom: 10rpx;
	}

	.text {
		font-size: 24rpx;
		color: #666;
	}

	.list {
		margin: 0 30rpx;
	}

	.list_item_contain {
		display: flex;
		align-items: center;
	}

	.list_item_contain text {
		margin-left: 20rpx;
		font-size: 14px;
	}

	.logout-text {
		color: #dd524d;
	}

	.last_view {
		height: 80rpx;
	}

	.login-popup {
		width: 600rpx;
		padding: 30rpx;
		background-color: #fff;
		border-radius: 10px;
	}

	.login-title {
		font-size: 18px;
		font-weight: bold;
		text-align: center;
		margin-bottom: 30rpx;
	}

	.login-form {
		margin-top: 20rpx;
	}

	.input-item {
		margin-bottom: 20rpx;
	}

	.input-label {
		font-size: 14px;
		color: #666;
		margin-bottom: 10rpx;
		display: block;
	}

	input {
		height: 80rpx;
		border: 1px solid #eee;
		border-radius: 5px;
		padding: 0 20rpx;
		font-size: 14px;
	}

	.login-btns {
		display: flex;
		margin-top: 30rpx;
	}

	.submit-btn, .cancel-btn {
		flex: 1;
		height: 80rpx;
		line-height: 80rpx;
		text-align: center;
		border-radius: 5px;
		font-size: 14px;
	}

	.submit-btn {
		background-color: #3bcb98;
		color: #fff;
		margin-right: 10rpx;
	}

	.cancel-btn {
		background-color: #f8f8f8;
		color: #666;
		margin-left: 10rpx;
	}
</style>
