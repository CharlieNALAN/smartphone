export function calculateDistance(lat1, lon1, lat2, lon2) {
    var R = 6371; // 地球半径，单位：千米  
    var dLat = deg2rad(lat2 - lat1); // 纬度差转换为弧度  
    var dLon = deg2rad(lon2 - lon1); // 经度差转换为弧度  
    var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var distanceKm = R * c; // 距离，单位：千米  
    var distanceUnit = 'km';
    var distanceValue = distanceKm;
    if (distanceKm < 1) {
        distanceValue = distanceKm * 1000; // 转换为米  
        distanceUnit = 'm';
    }

    // 返回包含距离值和单位的对象，或者仅返回距离值（如果需要）  
    return {
        value: distanceValue,
        unit: distanceUnit
    };
}

export function deg2rad(deg) {
    return deg * (Math.PI / 180);
}
