<template>
	<view>
		<NavBar>
			<template slot="title">
				<view>My</view>
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
							<text>Log in to view more...</text>
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
							<text>Profile</text>
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
							<text>About</text>
						</view>
					</template>
				</uni-list-item>
				<uni-list-item showArrow>
					<template v-slot:body>
						<view class="list_item_contain">
							<uni-icons type="help" size="28"></uni-icons>
							<text>Help</text>
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
				<uni-popup-dialog ref="inputClose" mode="input" title="Enter Invitation Code" placeholder="Please enter code"
					@confirm="dialogInputConfirm">
				</uni-popup-dialog>
			</uni-popup>
		</view>
		<view class="last_view"></view>
		
		<!-- Login popup -->
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
					text: 'Tickets',
					src: 'menpiao.png',
					opentype: 'navigate',
				}, {
					id: 2,
					url: '/pages/booked/booked',
					text: 'Bookings',
					src: 'yuyue.png',
					opentype: 'navigate',
				}, {
					id: 3,
					url: '/pages/map/map',
					text: 'Orders',
					src: 'suoyou.png',
					opentype: 'navigate',
				}, {
					id: 4,
					url: '/pages/track/track',
					text: 'Messages',
					src: 'xiaoxi.png',
					opentype: 'navigate',
				}]
			}
		},
		onShow() {
			// Get latest user info every time page is shown
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
				if (!this.loginForm.phone || !this.loginForm.password) {
					uni.showToast({
						title: 'Please fill in all fields',
						icon: 'none'
					});
					return;
				}
				
				this.isLogging = true;
				
				// Send login request
				uni.request({
					url: 'http://localhost:8000/api/user/login',
					method: 'POST',
					data: {
						phone: this.loginForm.phone,
						password: this.loginForm.password
					},
					success: res => {
						console.log('Login response:', res.data);
						
						if (res.data.status === 'success') {
							// Login successful, save user info
							if (res.data.user) {
								// Store user info to global data and local storage
								const app = getApp();
								if (app.globalData) {
									app.globalData.userInfo = res.data.user;
									console.log('User info saved to global variable:', app.globalData.userInfo);
								} else {
									console.error('globalData not defined');
								}
								
								uni.setStorageSync('userInfo', JSON.stringify(res.data.user));
								console.log('User info saved to local storage');
								
								// Update current page user info
								this.userInfo = res.data.user;
								this.isLoggedIn = true;
								
								// Close login popup
								this.closeLoginPopup();
								
								// Show success message
								uni.showToast({
									title: 'Login successful',
									icon: 'success'
								});
							}
						} else {
							// Login failed, show error message
							let errorMsg = 'Login failed';
							if (res.data.message) {
								errorMsg = res.data.message;
							}
							uni.showToast({
								title: errorMsg,
								icon: 'none'
							});
						}
					},
					fail: err => {
						console.error('Login request failed', err);
						uni.showToast({
							title: 'Network connection failed',
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
				// Try to get user info from global variable
				const app = getApp();
				console.log('Getting user info - current global variable:', app.globalData);
				
				if (app.globalData && app.globalData.userInfo) {
					this.userInfo = app.globalData.userInfo;
					this.isLoggedIn = true;
					console.log('Got user info from global variable:', this.userInfo);
					return;
				}
				
				// If not in global variable, try to get from local storage
				try {
					const userInfoStr = uni.getStorageSync('userInfo');
					console.log('User info in local storage:', userInfoStr || 'none');
					
					if (userInfoStr) {
						this.userInfo = JSON.parse(userInfoStr);
						this.isLoggedIn = true;
						console.log('Got user info from local storage:', this.userInfo);
						
						// Also update global variable
						if (app.globalData) {
							app.globalData.userInfo = this.userInfo;
							console.log('Updated user info in global variable');
						} else {
							console.error('globalData not defined');
						}
					} else {
						this.isLoggedIn = false;
						this.userInfo = {
							username: 'Guest',
							phone: 'Not logged in'
						};
						console.log('No logged in user info found');
					}
				} catch (e) {
					console.error('Failed to get user info', e);
					this.isLoggedIn = false;
					this.userInfo = {
						username: 'Guest',
						phone: 'Not logged in'
					};
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
							console.log('Cleared user info from local storage');
							
							const app = getApp();
							if (app.globalData) {
								app.globalData.userInfo = null;
								console.log('Cleared user info from global variable');
							} else {
								console.error('globalData not defined');
							}
							
							this.isLoggedIn = false;
							this.userInfo = {
								username: 'Guest',
								phone: 'Not logged in'
							};
							
							uni.showToast({
								title: 'Logged out',
								icon: 'success'
							});
						}
					}
				});
			},
			guidesign_dialog() {
				this.$refs.inputDialog.open()
			},
			dialogInputConfirm(val) {
				this.$refs.inputDialog.close()
				console.log(val)
				uni.showToast({
					icon: 'success',
					title: 'Guide application submitted!'
				})
			},
		}
	}
</script>

<style>
	.category {
		margin-top: 20rpx;
		padding: 10rpx 0;
		display: flex;
		flex-direction: row;
		justify-content: center;
		flex-wrap: wrap;
		min-height: 128rpx;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.category-item {
		width: 160rpx;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		box-sizing: border-box;
		margin: 5rpx 8rpx 0;
	}

	.icon {
		width: 90rpx;
		height: 90rpx;
		margin-bottom: 15rpx;
	}

	.list {
		padding-top: 20rpx;
		width: 100%;
		display: flex;
		justify-content: center;
		align-items: center;
		background: #f0f0f0;
	}
	uni-list {
		width: 95%;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}
	uni-list-item {
		width: 100%;
	}

	.nav_title {
		display: flex;
		justify-content: center;
		align-items: center;
		flex: 1;
		font-size: 18px;
	}

	.parent_catainer {
		background: #f0f0f0;
	}

	/* 头部背景图片 */
	.container_head {
		height: 370rpx;
		width: 100%;
		display: flex;
		justify-content: flex-end;
		align-items: flex-end;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		position: relative;
		overflow: hidden;
	}

	.container_head::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
					linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
		background-size: 20px 20px;
		transform: rotate(-15deg);
		opacity: 0.5;
	}

	.head_img {
		position: absolute;
		width: 100%;
		height: 370rpx;
	}

	.head_pers_info {
		height: 200rpx;
		width: 100%;
		margin-bottom: 50rpx;
		justify-content: left;
		display: flex;
		align-items: center;
		flex-direction: row;
		position: relative;
		z-index: 1;
		backdrop-filter: blur(5px);
		padding: 20rpx 0;
	}

	.head_pic {
		margin-left: 5%;
		position: relative;
		border: 3rpx solid rgba(255, 255, 255, 0.3);
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
		border-radius: 60rpx;
		overflow: hidden;
		background: rgba(255, 255, 255, 0.1);
	}

	.head_pic_content {
		position: absolute;
		width: 110rpx;
		height: 110rpx;
		border-radius: 55rpx;
		background-color: white;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
	}

	.inf_content {
		display: flex;
		flex-direction: column;
		margin-left: 24rpx;
		align-items: flex-start;
		justify-content: center;
		color: #ffffff;
		padding-bottom: 5rpx;
		width: 75%;
	}

	.user-row {
		display: flex;
		flex-direction: row;
		align-items: center;
		width: 100%;
	}

	.user-info-container {
		display: flex;
		align-items: center;
		gap: 10rpx;
	}

	.user-badge {
		display: flex;
		align-items: center;
		background: rgba(255, 255, 255, 0.2);
		padding: 4rpx 12rpx;
		border-radius: 20rpx;
		font-size: 20rpx;
		color: #fff;
		gap: 4rpx;
	}

	.user-detail {
		display: flex;
		flex-direction: column;
		gap: 8rpx;
		margin-top: 8rpx;
	}

	.phone-info {
		display: flex;
		align-items: center;
		gap: 8rpx;
	}

	.phone-text {
		font-size: 28rpx;
		color: #fff;
	}

	.user-id {
		font-size: 24rpx;
		color: rgba(255, 255, 255, 0.8);
	}

	.user_info {
		text-align: left;
		font-size: 36rpx;
		font-weight: bold;
		margin-bottom: 0;
		margin-right: 15rpx;
		color: #fff;
		text-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
	}

	.guest-badge {
		display: flex;
		align-items: center;
		background: rgba(255, 255, 255, 0.15);
		padding: 4rpx 12rpx;
		border-radius: 20rpx;
		font-size: 20rpx;
		color: rgba(255, 255, 255, 0.9);
		gap: 4rpx;
	}

	.guest-info {
		margin-top: 12rpx;
	}

	.guest-tip {
		display: flex;
		align-items: center;
		gap: 8rpx;
		font-size: 24rpx;
		color: rgba(255, 255, 255, 0.8);
		background: rgba(255, 255, 255, 0.1);
		padding: 8rpx 16rpx;
		border-radius: 30rpx;
	}

	.login-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 4rpx;
		background: linear-gradient(to right, #96fbc4, #f9f586);
		color: #333;
		font-size: 24rpx;
		padding: 4rpx 20rpx;
		line-height: 1.5;
		height: auto;
		border-radius: 30rpx;
		font-weight: normal;
		margin-top: 0;
		margin-left: auto;
		box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.1);
		transition: all 0.3s ease;
	}

	.login-btn:active {
		transform: scale(0.95);
		box-shadow: 0 2rpx 6rpx rgba(0, 0, 0, 0.15);
	}

	.family_info_ct_phone {
		text-align: center;
		justify-content: center;
		font-size: 28rpx;
		margin-bottom: 2rpx;
		margin-top: -10px;
	}

	.list_item_contain {
		display: flex;
		justify-content: center;
		align-items: center;
		margin-left: 30rpx;
	}

	.list_item_contain text {
		margin-left: 10rpx;
	}
	
	.logout-text {
		color: #dd524d;
	}

	.last_view {
		background: #f0f0f0;
		width: 100%;
		height: 1200rpx;
	}
	
	/* Login popup styles */
	.login-popup {
		width: 650rpx;
		background-color: #fff;
		border-radius: 20rpx;
		padding: 30rpx;
	}
	
	.login-title {
		font-size: 36rpx;
		text-align: center;
		font-weight: bold;
		margin-bottom: 40rpx;
	}
	
	.login-form {
		width: 100%;
	}
	
	.input-item {
		margin-bottom: 30rpx;
	}
	
	.input-label {
		font-size: 28rpx;
		color: #333;
		margin-bottom: 10rpx;
		display: block;
	}
	
	.input-item input {
		height: 80rpx;
		border: 1px solid #ddd;
		border-radius: 8rpx;
		padding: 0 20rpx;
		font-size: 28rpx;
	}
	
	.login-btns {
		display: flex;
		justify-content: space-between;
		margin-top: 40rpx;
	}
	
	.submit-btn {
		width: 45%;
		background: linear-gradient(to right, #96fbc4, #f9f586);
		color: #333;
		border: none;
	}
	
	.cancel-btn {
		width: 45%;
		background-color: #f5f5f5;
		color: #666;
		border: none;
	}
</style>
