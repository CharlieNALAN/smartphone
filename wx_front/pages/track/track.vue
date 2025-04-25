<template>
	<view class="track-page">
		<NavBar>
			<template slot="title">
				<view>Footprints</view>
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
				<text class="stats-title">Trip Overview</text>
			</view>
			<view class="stats-content">
				<view class="stats-item">
					<text class="stats-value">{{rec_num}}</text>
					<text class="stats-label">Visits</text>
				</view>
				<view class="stats-divider"></view>
				<view class="stats-item">
					<text class="stats-value">{{formatDate(rec_date)}}</text>
					<text class="stats-label">Last Visit</text>
				</view>
				<view class="stats-divider"></view>
				<view class="stats-item">
					<text class="stats-value">{{rec_attraction}}</text>
					<text class="stats-label">Latest Spot</text>
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
						<text class="time-label">First Time</text>
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
						<text class="time-label">Last Time</text>
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
					<text class="detail-text">Play Time: {{ selectedMarker.check_in_time }}</text>
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
					<text>View Details</text>
				</view>
				<view class="action-button navigate" @click="navigateToNavigationPage(selectedAttraction)">
					<uni-icons type="paperplane-filled" size="16" color="#ffffff"></uni-icons>
					<text>Navigate</text>
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
				// Current selected scenic  
				selectedScenic: null,
				// Marker data for the map  
				markers: [],
				// Polyline data  
				polyline: [],
				showInfo: false, 
				selectedAttraction: {}, 
				selectedMarker: {},
				rec_num: 0,
				rec_date: null,
				rec_attraction: "No Records",
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
				// First clear previous data
				this.clearFootprintData();
				
				// Try to get user info from global variable
				const app = getApp();
				console.log('Global object structure:', JSON.stringify(app.globalData));
				
				if (app.globalData && app.globalData.userInfo) {
					this.userInfo = app.globalData.userInfo;
					this.isLoggedIn = true;
					console.log('Got user info from global variable:', JSON.stringify(this.userInfo));
					return;
				}
				
				// If not in global variable, try to get from local storage
				try {
					const userInfoStr = uni.getStorageSync('userInfo');
					console.log('Local storage user info:', userInfoStr || 'none');
					
					if (userInfoStr) {
						this.userInfo = JSON.parse(userInfoStr);
						this.isLoggedIn = true;
						console.log('Got user info from local storage:', JSON.stringify(this.userInfo));
						
						// Also update global variable
						if (app.globalData) {
							app.globalData.userInfo = this.userInfo;
							console.log('Updated user info in global variable');
						} else {
							console.error('globalData not defined, cannot update global user info');
						}
					} else {
						this.isLoggedIn = false;
						this.userInfo = null;
						this.showToastMessage('Please login to view your footprints');
						console.log('No logged in user info found');
						this.clearFootprintData();
					}
				} catch (e) {
					console.error('Failed to get user info', e);
					this.isLoggedIn = false;
					this.userInfo = null;
					this.showToastMessage('Failed to get user info');
					this.clearFootprintData();
				}
			},
			// Show toast message
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
				this.rec_attraction = "No Records";
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
				// Clear existing data
				this.clearFootprintData();
				
				// If not logged in, show prompt and return
				if (!this.isLoggedIn || !this.userInfo) {
					this.showToastMessage('Please login to view your footprints');
					console.log('User not logged in, cannot get footprints');
					return;
				}
				
				// If scenic info doesn't exist, show prompt and return
				if (!this.selectedScenic || !this.selectedScenic.scenic_id) {
					console.error('Scenic info does not exist');
					this.showToastMessage('Unable to get scenic information');
					return;
				}
				
				const scenic = this.selectedScenic.scenic_id;
				
				// Find possible user ID field
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
				
				console.log('User info:', JSON.stringify(this.userInfo));
				console.log('User ID found:', userId);
				
				// If unable to get user ID, show prompt and try to use ID from global user info
				if (!userId && app.globalData && app.globalData.userInfo) {
					userId = app.globalData.userInfo.id;
					console.log('Trying to get ID directly from global variable:', userId);
				}
				
				// If still unable to get ID, show error message
				if (!userId) {
					console.error('Unable to get user ID, please ensure user is properly logged in');
					this.showToastMessage('Unable to get user info, please login again');
					return;
				}
				
				// Show loading indicator
				uni.showLoading({
					title: 'Loading footprints...'
				});
				
				// Use new API endpoint to get footprints for specific user and scenic
				uni.request({
					url: `http://localhost:8000/api/footprint/user/${userId}/scenic/${scenic}/`,
					method: 'GET',
					success: (res) => {
						// Hide loading indicator
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
					this.rec_attraction = "No Records";
					return;
				}
				
				let latest = sortedFootprints.length - 1;
				const latestFootprint = sortedFootprints[latest];
				this.rec_date = new Date(latestFootprint.check_in_time).toLocaleDateString();
				this.rec_attraction = latestFootprint.attraction__attraction_name;
			},
			formatDate(date) {
				if (!date) return 'No Records';
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
			
			// Share route functionality
			shareRoute() {
				uni.showLoading({
					title: 'Generating share image...'
				});
				setTimeout(() => {
					this.createShareImage();
				}, 300);
			},
			
			// Handle footprint data response
			handleFootprintResponse(res) {
				if (res.statusCode === 200) {
					const footprints = res.data;
					console.log('Footprint data received:', footprints ? footprints.length : 0, 'records');
					
					if (footprints && footprints.length > 0) {
						// Update marker data
						this.markers = footprints.map(footprint => ({
							id: footprint.id,
							longitude: footprint.attraction__attraction_lng,
							latitude: footprint.attraction__attraction_lat,
							name: footprint.attraction__attraction_name,
							attraction_id: footprint.attraction__attraction_id,
							check_in_time: footprint.check_in_time.split('T')[0],
							width: 25, // Set marker width
							height: 35, // Set marker height
							iconPath: '/static/marker.png', // Custom icon path
						}));
						
						// Draw route trajectory
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
						
						// Update rec_num, rec_date and rec_attraction
						this.updateRecNum(footprints);
						this.updateRecDateAndAttraction(sortedFootprints);
						
						// Clear no footprint message
						this.noFootprintMessage = '';
					} else {
						// No footprint data
						this.showToastMessage(`No footprint history in ${this.selectedScenic.scenic_name}`);
					}
				} else {
					// Request failed
					console.error('Failed to get footprint data:', res);
					this.showToastMessage('Failed to get footprint data');
				}
			},
			
			// Handle request failure
			handleRequestFail(err) {
				// Hide loading indicator
				uni.hideLoading();
				
				console.error('Footprint data request failed:', err);
				this.showToastMessage('Network request failed, please check your connection');
			},
			
			// Create share image
			createShareImage() {
				const ctx = uni.createCanvasContext('shareCanvas', this);
				const width = this.canvasWidth;
				const height = this.canvasHeight;
				
				// Draw background
				ctx.fillStyle = '#ffffff';
				ctx.fillRect(0, 0, width, height);
				
				// Draw title
				ctx.fillStyle = '#333333';
				ctx.font = 'normal bold 24px sans-serif';
				ctx.textAlign = 'center';
				ctx.fillText(`${this.selectedScenic.scenic_name} Tour Route`, width / 2, 50);
				
				// Draw date
				ctx.fillStyle = '#666666';
				ctx.font = 'normal 16px sans-serif';
				ctx.fillText(`Tour Date: ${this.getStartDate()} - ${this.getEndDate()}`, width / 2, 80);
				
				// Create static map image URL (using Tencent Map API)
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

				// Using Tencent Map static image API (need to replace with real key)
				// Note: You need to apply for Tencent Map API Key in production
				const apiKey = 'LQ2BZ-J6V6A-GGPKJ-COKYU-FNMM3-MVFPN';
				const mapImageUrl = `https://apis.map.qq.com/ws/staticmap/v2/?center=${center}&zoom=${zoom}&size=${size}&${markers}&${path}&key=${apiKey}`;
				
				console.log("mapImageUrl: " + mapImageUrl);

				// Get map image
				uni.showLoading({
					title: 'Getting map...'
				});
				
				uni.getImageInfo({
					src: mapImageUrl,
					success: (res) => {
						// Draw map
						ctx.drawImage(res.path, 50, 100, 500, 500);
						
						// Draw trip statistics
						this.drawStatsBox(ctx, 50, 620, 500, 120);
						
						// Draw copyright info
						ctx.fillStyle = '#999999';
						ctx.font = 'normal 14px sans-serif';
						ctx.textAlign = 'center';
						ctx.fillText('My Travel Footprints - Shared from Scenic Guide App', width / 2, height - 30);
						
						// Draw to canvas
						ctx.draw(false, () => {
							setTimeout(() => {
								this.saveCanvasToImage();
							}, 300);
						});
					},
					fail: (err) => {
						console.error('Failed to get map image', err);
						uni.hideLoading();
						
						// Try using backup map if failed
						uni.showToast({
							title: 'Using backup map',
							icon: 'none',
							duration: 1500
						});
						
						// Use backup map image
						const backupMapPath = '/static/map_placeholder.png';
						uni.getImageInfo({
							src: backupMapPath,
							success: (res) => {
								// Draw backup map
								ctx.drawImage(res.path, 50, 100, 500, 500);
								
								// Draw trip statistics
								this.drawStatsBox(ctx, 50, 620, 500, 120);
								
								// Draw copyright info
								ctx.fillStyle = '#999999';
								ctx.font = 'normal 14px sans-serif';
								ctx.textAlign = 'center';
								ctx.fillText('My Travel Footprints - Shared from Scenic Guide App', width / 2, height - 30);
								
								// Draw to canvas
								ctx.draw(false, () => {
									setTimeout(() => {
										this.saveCanvasToImage();
									}, 300);
								});
							},
							fail: (err2) => {
								console.error('Failed to get backup map image', err2);
								uni.hideLoading();
								uni.showToast({
									title: 'Failed to generate share image',
									icon: 'none'
								});
							}
						});
					}
				});
			},
			
			// Draw stats box
			drawStatsBox(ctx, x, y, width, height) {
				// Draw stats background
				ctx.fillStyle = '#f9f9f9';
				ctx.strokeStyle = '#eeeeee';
				this.roundRect(ctx, x, y, width, height, 10);
				ctx.fill();
				ctx.stroke();
				
				// Draw title
				ctx.fillStyle = '#333333';
				ctx.font = 'normal bold 18px sans-serif';
				ctx.textAlign = 'left';
				ctx.fillText('Trip Overview', x + 20, y + 30);
				
				// Draw stats data
				const itemWidth = width / 3;
				
				// Visit count
				ctx.fillStyle = '#333333';
				ctx.font = 'normal bold 22px sans-serif';
				ctx.textAlign = 'center';
				ctx.fillText(this.rec_num, x + itemWidth / 2, y + 70);
				
				ctx.fillStyle = '#999999';
				ctx.font = 'normal 14px sans-serif';
				ctx.fillText('Visits', x + itemWidth / 2, y + 95);
				
				// Divider 1
				ctx.beginPath();
				ctx.moveTo(x + itemWidth, y + 50);
				ctx.lineTo(x + itemWidth, y + height - 30);
				ctx.strokeStyle = '#eeeeee';
				ctx.stroke();
				
				// Last visit
				ctx.fillStyle = '#333333';
				ctx.font = 'normal bold 18px sans-serif';
				ctx.textAlign = 'center';
				ctx.fillText(this.formatDate(this.rec_date), x + itemWidth * 1.5, y + 70);
				
				ctx.fillStyle = '#999999';
				ctx.font = 'normal 14px sans-serif';
				ctx.fillText('Last Visit', x + itemWidth * 1.5, y + 95);
				
				// Divider 2
				ctx.beginPath();
				ctx.moveTo(x + itemWidth * 2, y + 50);
				ctx.lineTo(x + itemWidth * 2, y + height - 30);
				ctx.strokeStyle = '#eeeeee';
				ctx.stroke();
				
				// Latest attraction
				ctx.fillStyle = '#333333';
				ctx.font = 'normal bold 16px sans-serif';
				ctx.textAlign = 'center';
				// Truncate text if too long
				const attractionName = this.rec_attraction.length > 8 ? 
					this.rec_attraction.substring(0, 7) + '...' : this.rec_attraction;
				ctx.fillText(attractionName, x + itemWidth * 2.5, y + 70);
				
				ctx.fillStyle = '#999999';
				ctx.font = 'normal 14px sans-serif';
				ctx.fillText('Latest Spot', x + itemWidth * 2.5, y + 95);
			},
			
			// Draw rounded rectangle
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
			
			// Save canvas as image and share
			saveCanvasToImage() {
				uni.canvasToTempFilePath({
					canvasId: 'shareCanvas',
					success: (res) => {
						uni.hideLoading();
						// Save image to album
						uni.saveImageToPhotosAlbum({
							filePath: res.tempFilePath,
							success: () => {
								this.openShareMenu(res.tempFilePath);
							},
							fail: (err) => {
								console.error('Failed to save image', err);
								uni.showToast({
									title: 'Failed to save image',
									icon: 'none'
								});
							}
						});
					},
					fail: (err) => {
						uni.hideLoading();
						console.error('Failed to generate image', err);
						uni.showToast({
							title: 'Failed to generate image',
							icon: 'none'
						});
					}
				}, this);
			},
			
			// Open share menu
			openShareMenu(imagePath) {
				// #ifdef MP-WEIXIN
				uni.showShareImageMenu({
					path: imagePath,
					success: () => {
						uni.showToast({
							title: 'Shared successfully',
							icon: 'success'
						});
					},
					fail: (err) => {
						console.error('Failed to open share menu', err);
						uni.showToast({
							title: 'Please long press image to share',
							icon: 'none'
						});
					}
				});
				// #endif
				
				// #ifndef MP-WEIXIN
				uni.showModal({
					title: 'Share Success',
					content: 'Image has been saved to album, please check and share from there',
					showCancel: false
				});
				// #endif
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
