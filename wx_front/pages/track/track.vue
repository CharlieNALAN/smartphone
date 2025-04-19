<template>
	<view class="track-page">
		<NavBar>
			<template slot="title">
				<view>历史足迹</view>
			</template>
		</NavBar>
		
		<!-- 景区选择栏 -->
		<scroll-view :scroll-x="true">
			<view class="scenic-tabs">
				<view v-for="item in scenics" :key="item.scenic_id" @click="setActiveScenicId(item.scenic_id)"
					:class="{ 'scenic-tab': true, 'scenic-tab-active': item.scenic_id == activeScenicId }">
					<view class="scenic-image-container">
						<image :src="item.image" mode="aspectFill" class="scenic-image"></image>
					</view>
					<view class="scenic-name">{{item.scenic_name}}</view>
				</view>
			</view>
		</scroll-view>
		
		<!-- 行程统计卡片 -->
		<view class="stats-card">
			<view class="stats-header">
				<uni-icons type="calendar" size="22" color="#3bcb98"></uni-icons>
				<text class="stats-title">行程概览</text>
			</view>
			<view class="stats-content">
				<view class="stats-item">
					<text class="stats-value">{{rec_num}}</text>
					<text class="stats-label">次到访</text>
				</view>
				<view class="stats-divider"></view>
				<view class="stats-item">
					<text class="stats-value">{{formatDate(rec_date)}}</text>
					<text class="stats-label">最近到访</text>
				</view>
				<view class="stats-divider"></view>
				<view class="stats-item">
					<text class="stats-value">{{rec_attraction}}</text>
					<text class="stats-label">最新景点</text>
				</view>
			</view>
		</view>
		
		<!-- 地图区域 -->
		<view class="map-container">
			<map class="track-map" :latitude="selectedScenic.scenic_lat" :longitude="selectedScenic.scenic_lng"
				:scale="selectedScenic.scale" :markers="markers" :polyline="polylineStyle" show-location="true"
				@markertap="handleMarkerTap">
			</map>
			
			<!-- 分享按钮 -->
			<view class="share-button" @click="shareRoute" v-if="markers.length > 0">
				<uni-icons type="share" size="20" color="#ffffff"></uni-icons>
			</view>
			
			<!-- 起止时间卡片 -->
			<view class="time-card" v-if="markers.length > 0">
				<view class="time-section">
					<view class="time-icon">
						<uni-icons type="clock-filled" size="18" color="#3bcb98"></uni-icons>
					</view>
					<view class="time-details">
						<text class="time-label">第一次</text>
						<text class="time-value">{{getStartTime()}}</text>
						<text class="time-date">{{getStartDate()}}</text>
					</view>
				</view>
				<view class="time-divider"></view>
				<view class="time-section">
					<view class="time-icon">
						<uni-icons type="clock-filled" size="18" color="#3bcb98"></uni-icons>
					</view>
					<view class="time-details">
						<text class="time-label">最近一次</text>
						<text class="time-value">{{getEndTime()}}</text>
						<text class="time-date">{{getEndDate()}}</text>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 景点信息卡片 -->
		<view v-if="showInfo" class="attraction-info-card">
			<view class="attraction-header">
				<image class="attraction-cover" :src="selectedAttraction.image" mode="aspectFill"></image>
				<view class="attraction-profile">
					<view class="attraction-name-row">
						<text class="attraction-name">{{ selectedAttraction.attraction_name }}</text>
						<uni-icons type="closeempty" size="20" color="#999" @click="showInfo=false"></uni-icons>
					</view>
					<view class="rating">
						<uni-icons type="star-filled" size="14" color="#ffc107"></uni-icons>
						<text class="rating-value">{{ selectedAttraction.rating || 4.5 }}</text>
					</view>
				</view>
			</view>
			<view class="attraction-details">
				<view class="detail-item">
					<uni-icons type="calendar-filled" size="16" color="#3bcb98"></uni-icons>
					<text class="detail-text">游玩时间: {{ selectedMarker.check_in_time }}</text>
				</view>
				<view class="detail-item">
					<uni-icons type="location-filled" size="16" color="#3bcb98"></uni-icons>
					<text class="detail-text">{{ selectedAttraction.address }}</text>
				</view>
				<view class="detail-item" v-if="selectedAttraction.description">
					<uni-icons type="info-filled" size="16" color="#3bcb98"></uni-icons>
					<text class="detail-text description">{{ selectedAttraction.description }}</text>
				</view>
			</view>
			<view class="action-buttons">
				<view class="action-button details" @click="navto_detail(selectedAttraction.attraction_id)">
					<text>查看详情</text>
				</view>
				<view class="action-button navigate" @click="navigateToNavigationPage(selectedAttraction)">
					<uni-icons type="paperplane-filled" size="16" color="#ffffff"></uni-icons>
					<text>导航前往</text>
				</view>
			</view>
		</view>
		
		<!-- 分享预览画布（隐藏） -->
		<canvas canvas-id="shareCanvas" class="share-canvas"></canvas>
	</view>
</template>

<script>
	import NavBar from "../../components/NavBar.vue";
	export default {
		components: {
			NavBar
		},
		data() {
			return {
				scenics: [],
				activeScenicId: getApp().globalData.global_scenic_id,
				// 当前选中的景区  
				selectedScenic: null,
				// 标记点数据，可以基于选中的景区动态生成  
				markers: [],
				// 折线数据，如果需要的话也可以动态生成  
				polyline: [],
				showInfo: false, // 是否显示景点信息卡片
				selectedAttraction: {}, // 当前选中的景点信息
				selectedMarker: {},
				rec_num: 0,
				rec_date: null,
				rec_attraction: "",
				pattern: {
					color: '#7A7E83',
					backgroundColor: '#fff',
					selectedColor: '#007AFF',
					buttonColor: '#007AFF',
					iconColor: '#fff'
				},
				canvasWidth: 600, // 分享图宽度
				canvasHeight: 900, // 分享图高度
				userInfo: null, // 用户信息
				isLoggedIn: false, // 是否已登录
				noFootprintMessage: '' // 无足迹信息提示
			}
		},
		computed: {
			polylineStyle() {
				if (!this.polyline || this.polyline.length === 0) return [];
				
				return [{
					...this.polyline[0],
					color: '#333333',
					width: 3,
					dottedLine: true,
					borderWidth: 1,
					borderColor: '#000000'
				}];
			},
			markersWithCallout() {
				// 对 markers 进行处理，为每个 marker 添加自定义的 callout
				return this.markers.map(marker => ({
					...marker,
					customCallout: {
						display: 'BYCLICK', // 气泡是否常显，'BYCLICK'表示点击时显示
						textAlign: 'center',
						borderWidth: 1,
						borderColor: '#007AFF'
					},
					showCallout: false
				}));
			}
		},
		mounted() {
			this.getScenics();
			this.checkLoginStatus();
		},
		onShow() {
			// 每次页面显示时重新检查登录状态
			// 这确保了从其他页面退出登录后回到此页面时能正确更新
			console.log('历史足迹页面显示，重新检查登录状态');
			this.checkLoginStatus();
			
			// 如果有选中的景区，重新获取足迹数据
			if (this.selectedScenic) {
				this.updateMarkersAndPolylines();
			}
		},
		methods: {
			// 检查登录状态
			checkLoginStatus() {
				// 先清除之前的数据
				this.clearFootprintData();
				
				// 尝试从全局变量获取用户信息
				const app = getApp();
				console.log('全局对象结构:', JSON.stringify(app.globalData));
				
				if (app.globalData && app.globalData.userInfo) {
					this.userInfo = app.globalData.userInfo;
					this.isLoggedIn = true;
					console.log('从全局变量获取到用户信息:', JSON.stringify(this.userInfo));
					return;
				}
				
				// 如果全局变量中没有，尝试从本地存储获取
				try {
					const userInfoStr = uni.getStorageSync('userInfo');
					console.log('本地存储用户信息:', userInfoStr || '无');
					
					if (userInfoStr) {
						this.userInfo = JSON.parse(userInfoStr);
						this.isLoggedIn = true;
						console.log('从本地存储获取到用户信息:', JSON.stringify(this.userInfo));
						
						// 同时更新全局变量
						if (app.globalData) {
							app.globalData.userInfo = this.userInfo;
							console.log('已更新全局变量中的用户信息');
						} else {
							console.error('globalData未定义，无法更新全局用户信息');
						}
					} else {
						this.isLoggedIn = false;
						this.userInfo = null;
						this.showToastMessage('请先登录以查看您的足迹');
						console.log('未找到已登录的用户信息');
						this.clearFootprintData();
					}
				} catch (e) {
					console.error('获取用户信息失败', e);
					this.isLoggedIn = false;
					this.userInfo = null;
					this.showToastMessage('获取用户信息失败');
					this.clearFootprintData();
				}
			},
			// 显示提示信息
			showToastMessage(message) {
				uni.showToast({
					title: message,
					icon: 'none',
					duration: 2000
				});
			},
			// 清除足迹数据的方法
			clearFootprintData() {
				this.markers = [];
				this.polyline = [];
				this.rec_num = 0;
				this.rec_date = null;
				this.rec_attraction = "暂无记录";
				this.showInfo = false;
				this.selectedAttraction = {};
				this.selectedMarker = {};
			},
			// 从后端获取景区数据
			getScenics() {
				uni.request({
					url: 'http://localhost:8000/scenic',
					method: 'GET',
					success: (res) => {
						if (res.statusCode === 200) {
							// 将从后端获取的数据存储到attractions中
							this.scenics = res.data;
							if (this.scenics.length > 0) {
								this.selectedScenic = this.scenics[this.activeScenicId-1];
								this.updateMarkersAndPolylines(); // 更新地图的标记点和折线
							}
						} else {
							console.error('Failed to fetch scenics data');
						}
					},
					fail: (err) => {
						console.error('Failed to fetch scenics data:', err);
					},
				});
			},
			setActiveScenicId(id) {
				this.activeScenicId = id;
				this.selectScenic(id);
			},
			// 选择景区的方法  
			selectScenic(scenicId) {
				this.selectedScenic = this.scenics.find(scenic => scenic.scenic_id === scenicId);
				// 根据选中的景区更新标记点和折线数据  
				this.updateMarkersAndPolylines();
			},
			updateMarkersAndPolylines() {
				// 清空已有数据
				this.clearFootprintData();
				
				// 如果未登录，显示提示信息并返回
				if (!this.isLoggedIn || !this.userInfo) {
					this.showToastMessage('请先登录以查看您的足迹');
					console.log('用户未登录，无法获取足迹');
					return;
				}
				
				// 如果景区信息不存在，显示提示并返回
				if (!this.selectedScenic || !this.selectedScenic.scenic_id) {
					console.error('景区信息不存在');
					this.showToastMessage('无法获取景区信息');
					return;
				}
				
				const scenic = this.selectedScenic.scenic_id;
				
				// 优先查找可能的用户ID字段
				let userId = null;
				if (this.userInfo.id) {
					userId = this.userInfo.id;
				} else if (this.userInfo.user_id) {
					userId = this.userInfo.user_id;
				} else if (this.userInfo.userId) {
					userId = this.userInfo.userId;
				} else if (this.userInfo.userid) {
					userId = this.userInfo.userid;
				}
				
				console.log('用户信息:', JSON.stringify(this.userInfo));
				console.log('获取到的用户ID:', userId);
				
				// 如果无法获取用户ID，显示提示并尝试使用全局用户信息的id
				if (!userId && app.globalData && app.globalData.userInfo) {
					userId = app.globalData.userInfo.id;
					console.log('尝试从全局变量直接获取ID:', userId);
				}
				
				// 如果还是无法获取ID，则显示错误信息
				if (!userId) {
					console.error('无法获取用户ID，请确保用户已正确登录');
					this.showToastMessage('无法获取用户信息，请重新登录');
					return;
				}
				
				// 显示加载提示
				uni.showLoading({
					title: '加载足迹中...'
				});
				
				// 使用新的API接口获取指定用户和景区的足迹
				uni.request({
					url: `http://localhost:8000/api/footprint/user/${userId}/scenic/${scenic}/`,
					method: 'GET',
					success: (res) => {
						// 隐藏加载提示
						uni.hideLoading();
						this.handleFootprintResponse(res);
					},
					fail: this.handleRequestFail
				});
			},
			updateRecNum(footprints) {
				const uniqueDates = new Set(footprints.map(footprint => new Date(footprint.check_in_time)
					.toLocaleDateString()));
				this.rec_num = uniqueDates.size;
			},
			updateRecDateAndAttraction(sortedFootprints) {
				if (sortedFootprints.length === 0) {
					this.rec_date = null;
					this.rec_attraction = "暂无记录";
					return;
				}
				
				let latest = sortedFootprints.length - 1;
				const latestFootprint = sortedFootprints[latest];
				this.rec_date = new Date(latestFootprint.check_in_time).toLocaleDateString();
				this.rec_attraction = latestFootprint.attraction__attraction_name;
			},
			formatDate(date) {
				if (!date) return '暂无记录';
				return new Date(date).toLocaleDateString();
			},
			getStartTime() {
				if (!this.markers || this.markers.length === 0) return '08:00';
				const firstMarker = this.markers[0];
				const date = new Date(firstMarker.check_in_time);
				return '08:00';
			},
			getStartDate() {
				if (!this.markers || this.markers.length === 0) return '';
				const firstMarker = this.markers[0];
				const date = new Date(firstMarker.check_in_time);
				return date.toLocaleDateString();
			},
			getEndTime() {
				if (!this.markers || this.markers.length === 0) return '16:00';
				const lastMarker = this.markers[this.markers.length - 1];
				const date = new Date(lastMarker.check_in_time);
				return '16:00';
			},
			getEndDate() {
				if (!this.markers || this.markers.length === 0) return '';
				const lastMarker = this.markers[this.markers.length - 1];
				const date = new Date(lastMarker.check_in_time);
				return date.toLocaleDateString();
			},
			handleMarkerTap(e) {
				const markerId = e.markerId;
				this.selectedMarker = this.markers.find(marker => marker.id === markerId);
				const attractionId = this.selectedMarker.attraction_id;
				this.showInfo = true;
				uni.request({
					url: `http://localhost:8000/attraction/${attractionId}`,
					method: 'GET',
					success: (res) => {
						if (res.statusCode === 200) {
							// 将从后端获取的数据存储到attractions中
							this.selectedAttraction = res.data;
						} else {
							console.error('Failed to fetch attraction data');
						}
					},
					fail: (err) => {
						console.error('Failed to fetch attraction data:', err);
					},
				});
			},
			navto_detail(attractionId) {
				console.log('Navigate to navigation page' + attractionId);
				uni.navigateTo({
					url: `/pages/detail/detail?attraction_id=${attractionId}`
				});
			},
			navigateToNavigationPage(attraction) {
				// 实现导航到导航页面的逻辑
				console.log('Navigate to navigation page', attraction);
				// 这里可以根据实际情况实现导航逻辑
			},
			
			// 分享路线功能
			shareRoute() {
				uni.showLoading({
					title: '生成分享图片中...'
				});
				setTimeout(() => {
					this.createShareImage();
				}, 300);
			},
			
			// 创建分享图片
			createShareImage() {
				const ctx = uni.createCanvasContext('shareCanvas', this);
				const width = this.canvasWidth;
				const height = this.canvasHeight;
				
				// 绘制背景
				ctx.fillStyle = '#ffffff';
				ctx.fillRect(0, 0, width, height);
				
				// 绘制标题
				ctx.fillStyle = '#333333';
				ctx.font = 'normal bold 24px sans-serif';
				ctx.textAlign = 'center';
				ctx.fillText(`${this.selectedScenic.scenic_name}游览路线`, width / 2, 50);
				
				// 绘制日期
				ctx.fillStyle = '#666666';
				ctx.font = 'normal 16px sans-serif';
				ctx.fillText(`行程日期: ${this.getStartDate()} - ${this.getEndDate()}`, width / 2, 80);
				
				// 创建地图静态图片URL（使用腾讯地图静态图API）
				const center = `${this.selectedScenic.scenic_lat},${this.selectedScenic.scenic_lng}`;
				const zoom = this.selectedScenic.scale;
				const size = '500x500';
				const markers = this.markers.map(m => `markers=color:red|size:mid|${m.latitude},${m.longitude}`).join('&');
				const path = `path=color:0x3bcb98|weight:4|${this.polyline[0].points.map(p => `${p.latitude},${p.longitude}`).join('|')}`;
				
				console.log("center: " + center);
				console.log("zoom: " + zoom);
				console.log("size: " + size);
				console.log("markers: " + markers);
				console.log("path: " + path);

				// 这里使用腾讯地图静态图API（需要替换为真实的key）
				// 注意：实际使用时需要申请腾讯地图API Key
				const apiKey = 'LQ2BZ-J6V6A-GGPKJ-COKYU-FNMM3-MVFPN';
				const mapImageUrl = `https://apis.map.qq.com/ws/staticmap/v2/?center=${center}&zoom=${zoom}&size=${size}&${markers}&${path}&key=${apiKey}`;
				
				console.log("mapImageUrl: " + mapImageUrl);

				// 获取地图图片
				uni.showLoading({
					title: '获取地图中...'
				});
				
				uni.getImageInfo({
					src: mapImageUrl,
					success: (res) => {
						// 绘制地图
						ctx.drawImage(res.path, 50, 100, 500, 500);
						
						// 绘制行程统计
						this.drawStatsBox(ctx, 50, 620, 500, 120);
						
						// 绘制底部版权信息
						ctx.fillStyle = '#999999';
						ctx.font = 'normal 14px sans-serif';
						ctx.textAlign = 'center';
						ctx.fillText('我的旅行足迹 - 分享自景区导览App', width / 2, height - 30);
						
						// 绘制到画布
						ctx.draw(false, () => {
							setTimeout(() => {
								this.saveCanvasToImage();
							}, 300);
						});
					},
					fail: (err) => {
						console.error('获取地图图片失败', err);
						uni.hideLoading();
						
						// 获取失败时尝试使用备用地图
						uni.showToast({
							title: '使用备用地图',
							icon: 'none',
							duration: 1500
						});
						
						// 使用备用地图图片
						const backupMapPath = '/static/map_placeholder.png';
						uni.getImageInfo({
							src: backupMapPath,
							success: (res) => {
								// 绘制备用地图
								ctx.drawImage(res.path, 50, 100, 500, 500);
								
								// 绘制行程统计
								this.drawStatsBox(ctx, 50, 620, 500, 120);
								
								// 绘制底部版权信息
								ctx.fillStyle = '#999999';
								ctx.font = 'normal 14px sans-serif';
								ctx.textAlign = 'center';
								ctx.fillText('我的旅行足迹 - 分享自景区导览App', width / 2, height - 30);
								
								// 绘制到画布
								ctx.draw(false, () => {
									setTimeout(() => {
										this.saveCanvasToImage();
									}, 300);
								});
							},
							fail: (err2) => {
								console.error('获取备用地图图片失败', err2);
								uni.hideLoading();
								uni.showToast({
									title: '生成分享图片失败',
									icon: 'none'
								});
							}
						});
					}
				});
			},
			
			// 绘制统计信息框
			drawStatsBox(ctx, x, y, width, height) {
				// 绘制统计信息背景
				ctx.fillStyle = '#f9f9f9';
				ctx.strokeStyle = '#eeeeee';
				this.roundRect(ctx, x, y, width, height, 10);
				ctx.fill();
				ctx.stroke();
				
				// 绘制标题
				ctx.fillStyle = '#333333';
				ctx.font = 'normal bold 18px sans-serif';
				ctx.textAlign = 'left';
				ctx.fillText('行程概览', x + 20, y + 30);
				
				// 绘制统计数据
				const itemWidth = width / 3;
				
				// 到访次数
				ctx.fillStyle = '#333333';
				ctx.font = 'normal bold 22px sans-serif';
				ctx.textAlign = 'center';
				ctx.fillText(this.rec_num, x + itemWidth / 2, y + 70);
				
				ctx.fillStyle = '#999999';
				ctx.font = 'normal 14px sans-serif';
				ctx.fillText('次到访', x + itemWidth / 2, y + 95);
				
				// 分隔线1
				ctx.beginPath();
				ctx.moveTo(x + itemWidth, y + 50);
				ctx.lineTo(x + itemWidth, y + height - 30);
				ctx.strokeStyle = '#eeeeee';
				ctx.stroke();
				
				// 最近到访
				ctx.fillStyle = '#333333';
				ctx.font = 'normal bold 18px sans-serif';
				ctx.textAlign = 'center';
				ctx.fillText(this.formatDate(this.rec_date), x + itemWidth * 1.5, y + 70);
				
				ctx.fillStyle = '#999999';
				ctx.font = 'normal 14px sans-serif';
				ctx.fillText('最近到访', x + itemWidth * 1.5, y + 95);
				
				// 分隔线2
				ctx.beginPath();
				ctx.moveTo(x + itemWidth * 2, y + 50);
				ctx.lineTo(x + itemWidth * 2, y + height - 30);
				ctx.strokeStyle = '#eeeeee';
				ctx.stroke();
				
				// 最新景点
				ctx.fillStyle = '#333333';
				ctx.font = 'normal bold 16px sans-serif';
				ctx.textAlign = 'center';
				// 如果文字太长，截取显示
				const attractionName = this.rec_attraction.length > 8 ? 
					this.rec_attraction.substring(0, 7) + '...' : this.rec_attraction;
				ctx.fillText(attractionName, x + itemWidth * 2.5, y + 70);
				
				ctx.fillStyle = '#999999';
				ctx.font = 'normal 14px sans-serif';
				ctx.fillText('最新景点', x + itemWidth * 2.5, y + 95);
			},
			
			// 绘制圆角矩形
			roundRect(ctx, x, y, width, height, radius) {
				ctx.beginPath();
				ctx.moveTo(x + radius, y);
				ctx.lineTo(x + width - radius, y);
				ctx.arcTo(x + width, y, x + width, y + radius, radius);
				ctx.lineTo(x + width, y + height - radius);
				ctx.arcTo(x + width, y + height, x + width - radius, y + height, radius);
				ctx.lineTo(x + radius, y + height);
				ctx.arcTo(x, y + height, x, y + height - radius, radius);
				ctx.lineTo(x, y + radius);
				ctx.arcTo(x, y, x + radius, y, radius);
				ctx.closePath();
			},
			
			// 保存画布为图片并分享
			saveCanvasToImage() {
				uni.canvasToTempFilePath({
					canvasId: 'shareCanvas',
					success: (res) => {
						uni.hideLoading();
						// 保存图片到相册
						uni.saveImageToPhotosAlbum({
							filePath: res.tempFilePath,
							success: () => {
								this.openShareMenu(res.tempFilePath);
							},
							fail: (err) => {
								console.error('保存图片失败', err);
								uni.showToast({
									title: '保存图片失败',
									icon: 'none'
								});
							}
						});
					},
					fail: (err) => {
						uni.hideLoading();
						console.error('生成图片失败', err);
						uni.showToast({
							title: '生成图片失败',
							icon: 'none'
						});
					}
				}, this);
			},
			
			// 打开分享菜单
			openShareMenu(imagePath) {
				// #ifdef MP-WEIXIN
				uni.showShareImageMenu({
					path: imagePath,
					success: () => {
						uni.showToast({
							title: '分享成功',
							icon: 'success'
						});
					},
					fail: (err) => {
						console.error('打开分享菜单失败', err);
						uni.showToast({
							title: '请长按图片分享',
							icon: 'none'
						});
					}
				});
				// #endif
				
				// #ifndef MP-WEIXIN
				uni.showModal({
					title: '分享成功',
					content: '图片已保存到相册，请到相册中查看并分享',
					showCancel: false
				});
				// #endif
			},
			
			// 处理足迹数据响应
			handleFootprintResponse(res) {
				if (res.statusCode === 200) {
					const footprints = res.data;
					console.log('获取到足迹数据:', footprints ? footprints.length : 0, '条');
					
					if (footprints && footprints.length > 0) {
						// 更新标记点数据
						this.markers = footprints.map(footprint => ({
							id: footprint.id,
							longitude: footprint.attraction__attraction_lng,
							latitude: footprint.attraction__attraction_lat,
							name: footprint.attraction__attraction_name,
							attraction_id: footprint.attraction__attraction_id,
							check_in_time: footprint.check_in_time.split('T')[0],
							width: 25, // 设置标记宽度
							height: 35, // 设置标记高度
							iconPath: '/static/marker.png', // 自定义图标路径
						}));
						
						// 绘制路线轨迹
						const sortedFootprints = [...footprints].sort(
							(a, b) => new Date(a.check_in_time) - new Date(b.check_in_time)
						);
						const points = sortedFootprints.map(footprint => ({
							longitude: footprint.attraction__attraction_lng,
							latitude: footprint.attraction__attraction_lat
						}));
						
						this.polyline = [{
							points: points,
							color: "#333333",
							arrowLine: true,
							width: 3,
							dottedLine: true
						}];
						
						// 更新 rec_num, rec_date 和 rec_attraction
						this.updateRecNum(footprints);
						this.updateRecDateAndAttraction(sortedFootprints);
						
						// 清空无足迹提示
						this.noFootprintMessage = '';
					} else {
						// 没有足迹数据
						this.showToastMessage(`您在${this.selectedScenic.scenic_name}暂无历史足迹`);
					}
				} else {
					// 请求失败
					console.error('获取足迹数据失败:', res);
					this.showToastMessage('获取足迹数据失败');
				}
			},
			
			// 处理请求失败
			handleRequestFail(err) {
				// 隐藏加载提示
				uni.hideLoading();
				
				console.error('请求足迹数据失败:', err);
				this.showToastMessage('网络请求失败，请检查网络');
			}
		}
	};
</script>

<style>
	.track-page {
		background-color: #f5f5f5;
		min-height: 100vh;
	}
	
	/* 景区选择栏样式 */
	.scenic-tabs {
		display: flex;
		padding: 20rpx 20rpx 10rpx;
		background-color: #ffffff;
	}
	
	.scenic-tab {
		display: flex;
		flex-direction: column;
		align-items: center;
		margin-right: 30rpx;
		padding: 10rpx 15rpx;
		border-radius: 12rpx;
		transition: all 0.3s;
	}
	
	.scenic-tab-active {
		background: rgba(59, 203, 152, 0.1);
	}
	
	.scenic-image-container {
		width: 100rpx;
		height: 100rpx;
		border-radius: 50%;
		overflow: hidden;
		border: 3rpx solid transparent;
		margin-bottom: 10rpx;
	}
	
	.scenic-tab-active .scenic-image-container {
		border-color: #3bcb98;
	}
	
	.scenic-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}
	
	.scenic-name {
		font-size: 24rpx;
		color: #666;
		text-align: center;
	}
	
	.scenic-tab-active .scenic-name {
		color: #3bcb98;
		font-weight: bold;
	}
	
	/* 行程统计卡片 */
	.stats-card {
		margin: 20rpx;
		background-color: #ffffff;
		border-radius: 20rpx;
		box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.05);
		padding: 30rpx;
		overflow: hidden;
	}
	
	.stats-header {
		display: flex;
		align-items: center;
		margin-bottom: 20rpx;
	}
	
	.stats-title {
		font-size: 30rpx;
		font-weight: bold;
		margin-left: 10rpx;
	}
	
	.stats-content {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 10rpx 0;
	}
	
	.stats-item {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 10rpx;
	}
	
	.stats-value {
		font-size: 32rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 5rpx;
		text-align: center;
	}
	
	.stats-label {
		font-size: 24rpx;
		color: #999;
	}
	
	.stats-divider {
		width: 2rpx;
		height: 60rpx;
		background-color: #f0f0f0;
	}
	
	/* 地图区域 */
	.map-container {
		margin: 20rpx;
		border-radius: 20rpx;
		overflow: hidden;
		position: relative;
		box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.05);
	}
	
	.track-map {
		width: 100%;
		height: 650rpx;
	}
	
	/* 分享按钮 */
	.share-button {
		position: absolute;
		top: 20rpx;
		right: 20rpx;
		width: 80rpx;
		height: 80rpx;
		border-radius: 50%;
		background: linear-gradient(to right, #5ac7d1, #60e1c1);
		display: flex;
		justify-content: center;
		align-items: center;
		box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.1);
		z-index: 10;
	}
	
	/* 起止时间卡片 */
	.time-card {
		position: absolute;
		bottom: 20rpx;
		left: 20rpx;
		right: 20rpx;
		background-color: rgba(255, 255, 255, 0.9);
		border-radius: 20rpx;
		padding: 30rpx;
		display: flex;
		justify-content: space-between;
		box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.1);
	}
	
	.time-section {
		display: flex;
		align-items: center;
		flex: 1;
	}
	
	.time-icon {
		margin-right: 20rpx;
	}
	
	.time-details {
		display: flex;
		flex-direction: column;
	}
	
	.time-label {
		font-size: 24rpx;
		color: #999;
		margin-bottom: 5rpx;
	}
	
	.time-value {
		font-size: 30rpx;
		font-weight: bold;
	}
	
	.time-date {
		font-size: 24rpx;
		color: #999;
	}
	
	.time-divider {
		width: 2rpx;
		height: 80rpx;
		background-color: #f0f0f0;
		margin: 0 40rpx;
	}
	
	/* 景点信息卡片 */
	.attraction-info-card {
		margin: 20rpx;
		background-color: #ffffff;
		border-radius: 20rpx;
		box-shadow: 0 4rpx 10rpx rgba(0, 0, 0, 0.05);
		overflow: hidden;
	}
	
	.attraction-header {
		display: flex;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1px solid #f5f5f5;
	}
	
	.attraction-cover {
		width: 130rpx;
		height: 130rpx;
		border-radius: 15rpx;
		object-fit: cover;
	}
	
	.attraction-profile {
		flex: 1;
		margin-left: 20rpx;
	}
	
	.attraction-name-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}
	
	.attraction-name {
		font-size: 34rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 10rpx;
	}
	
	.rating {
		display: flex;
		align-items: center;
		margin-top: 10rpx;
	}
	
	.rating-value {
		font-size: 28rpx;
		color: #333;
		margin-left: 10rpx;
	}
	
	.attraction-details {
		padding: 20rpx 30rpx;
	}
	
	.detail-item {
		display: flex;
		margin-bottom: 15rpx;
		align-items: flex-start;
	}
	
	.detail-text {
		font-size: 28rpx;
		color: #666;
		margin-left: 15rpx;
		flex: 1;
		line-height: 1.5;
	}
	
	.description {
		display: -webkit-box;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 2;
		overflow: hidden;
	}
	
	.action-buttons {
		display: flex;
		padding: 20rpx 30rpx 30rpx;
		border-top: 1px solid #f5f5f5;
	}
	
	.action-button {
		display: flex;
		align-items: center;
		justify-content: center;
		height: 80rpx;
		border-radius: 40rpx;
		font-size: 28rpx;
	}
	
	.action-button.details {
		flex: 1;
		background-color: rgba(59, 203, 152, 0.1);
		color: #3bcb98;
		margin-right: 20rpx;
	}
	
	.action-button.navigate {
		flex: 1;
		background: linear-gradient(to right, #5ac7d1, #60e1c1);
		color: white;
	}
	
	.action-button.navigate text {
		margin-left: 10rpx;
	}
	
	/* 分享画布 */
	.share-canvas {
		position: fixed;
		top: -9999px;
		left: -9999px;
		width: 600px; /* 分享图宽度 */
		height: 900px; /* 分享图高度 */
	}
</style>
