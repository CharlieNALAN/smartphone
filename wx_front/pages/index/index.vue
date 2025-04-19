<template>
	<view>
		<view class="uni-margin-wrap">
			<swiper :style="'height:'+ show_screen_height + 'px;'" indicator-dots="true" :current="currentIndex"
				@change="swiperChange">
				<swiper-item>
					<image class="swiper-item" :src="backimg_src" mode="scaleToFill" />
					<view class="login_button">
						<button @click="goToLogin">进入小程序</button>
					</view>
				</swiper-item>
				<swiper-item>
					<Register @loginSuccess="handleLoginSuccess"></Register>
				</swiper-item>
				<swiper-item>
					<WelOne></WelOne>
				</swiper-item>
			</swiper>
		</view>
	</view>
</template>

<script>
	import WelOne from '../../components/WelOne.vue';
	import Register from '../../components/Register.vue';
	export default {
		components: {
			WelOne,
			Register
		},
		data() {
			return {
				backimg_src: getApp().globalData.resourceURL + '/media/back_img.png',
				show_screen_height: getApp().globalData.windowHeight,
				AppId: 'wxb877596d5caae332',
				AppSecret: 'c20278f741625a3088c729e0a187ca28',
				login_code: '',
				currentIndex: 0, // 当前swiper-item索引
			}
		},
		methods: {
			swiperChange(e) {
				this.currentIndex = e.detail.current;
			},
			goToLogin() {
				// 切换到下一个swiper-item
				this.currentIndex = 1; // Register组件在第二个swiper-item中
			},
			handleLoginSuccess() {
				uni.showToast({
					title: '登录成功',
					icon: 'success'
				});
				this.currentIndex = 2;
			},
			async wxLogin() {
				try {
					const {
						code
					} = await uni.login();
					const {
						userInfo,
						encryptedData,
						iv
					} = await uni.getUserInfo();
					const {
						phoneNumber
					} = await uni.request({
						url: 'http://localhost:8000/api/get-phone-number', // 替换成后端接口地址
						method: 'POST',
						data: {
							code,
							encryptedData,
							iv
						}
					});
					// 将获取的用户名和手机号发送到后端进行注册或登录
					await uni.request({
						url: 'http://localhost:8000/api/register-or-login', // 替换成后端接口地址
						method: 'POST',
						data: {
							username: userInfo.nickName, // 使用微信昵称作为用户名
							phone: phoneNumber // 使用获取的手机号
						}
					});
					// 注册或登录成功后的操作
					uni.showToast({
						title: '登录成功',
						icon: 'success'
					});
				} catch (error) {
					console.error('微信登录失败:', error);
					uni.showToast({
						title: '登录失败',
						icon: 'none'
					});
				}
			},
		},
	}
</script>

<style>
	.content {
		width: 100%;
		overflow: hidden;
	}

	.login_button {
		position: absolute;
		left: 50%;
		bottom: 20%;
		transform: translate(-50%, -50%);
	}

	.uni-margin-wrap {
		width: 100%;
	}

	.swiper-item {
		display: block;
		line-height: 300rpx;
		text-align: center;
		height: 100%;
		width: 100%;
		z-index: -1;
	}

	.login_button {
		position: absolute;
		left: 50%;
		bottom: 20%;
		transform: translate(-50%, -50%);
	}
</style>
