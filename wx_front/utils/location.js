// 定义获取用户位置信息的方法
function getUserLocation() {
	wx.getLocation({
		type: 'gcj02',
		success(res) {
			const latitude = res.latitude
			const longitude = res.longitude
			sendLocationToBackend(latitude, longitude)
		},
		fail(err) {
			console.error(err)
		}
	})
}

// 定义发送位置信息给后端的方法
function sendLocationToBackend(latitude, longitude) {
	uni.request({
		url: 'https://127.0.0.1:8000/api/record_stay',
		method: 'POST',
		data: {
			latitude: latitude,
			longitude: longitude
		},
		success(res) {
			console.log(res.data)
		},
		fail(err) {
			console.error(err)
		}
	})
}

// 定义定时器，每隔一分钟执行一次获取用户位置信息的方法
function startLocationTimer() {
	setInterval(() => {
		getUserLocation()
	}, 60000) // 每隔一分钟（60秒）执行一次
}

// 导出 startLocationTimer 方法
export {
	startLocationTimer
}
