<template>
	<uni-popup ref="add" type="bottom" backgroundColor="#fff">
		<uni-title type="h2" title="新增游玩人" align="center"></uni-title>
		<view class="add-card col-horizontal-center" style="height: 500px; ">
			<uni-card :is-shadow="false">
				<u-form @submit.native.prevent="submitForm">
					<u-form-item>
						<u-input type="text" v-model="newVisitor.name" placeholder="与证件姓名一致" border="none">
							<u--text text="中文姓名" slot="prefix" margin="0 15px 0 0"></u--text>
						</u-input>
					</u-form-item>
					<u-form-item>
						<u-input type="idcard" v-model="newVisitor.idcard" placeholder="与证件号码一致" border="none">
							<u--text text="身份证号" slot="prefix" margin="0 15px 0 0"></u--text>
						</u-input>
					</u-form-item>
					<u-form-item>
						<u-input type="number" v-model="newVisitor.phone" placeholder="用于接受出行短信" border="none">
							<u--text text="手机号码" slot="prefix" margin="0 15px 0 0"></u--text>
						</u-input>
					</u-form-item>
				</u-form>
			</uni-card>
			<view class="hor-ver-center" style="width: 380px; height: 400px;">
				<u-button type="primary" shape="circle" text="保存并使用" @click="submitForm"></u-button>
			</view>
		</view>
	</uni-popup>
</template>

<script>
	export default {
		props: {
			newVisitor: Object, // 新游玩人信息
		},
		watch: {
			// 监听 newVisitor 对象的变化
			newVisitor: {
				immediate: true, // 立即执行
				handler() {
					// 如果 newVisitor 对象的值发生变化，则重置为初始值
					this.resetForm();
				}
			}
		},
		methods: {
			resetForm() {
				this.newVisitor = {
					name: '',
					idcard: '',
					phone: ''
				};
			},
			submitForm() {
				if (this.validateForm()) {
					this.$emit('addVisitor', {
						...this.newVisitor
					}); // 将新游玩人信息提交给父组件
					this.$refs.add.close(); // 关闭弹窗
				} else {
					// 提示用户输入有误
					uni.showToast({
						title: '输入有误，请检查表单信息',
						icon: 'none'
					});
				}
			},
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
				return isValid;
			},
		}
	}
</script>
