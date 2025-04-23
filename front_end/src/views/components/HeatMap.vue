<template>
    <div class="map-container">
        <div class="change-zone">
            <el-select v-model="selectedScenic" @change="changeScenic" placeholder="请选择景区">
                <el-option v-for="scenic in scenicList" :key="scenic.scenic_id" :label="scenic.scenic_name" :value="scenic.scenic_name"></el-option>
            </el-select>
        </div>
        <div id="map" class="map"></div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            // selectedScenic: '千岛湖',
            selectedScenic: '请选择景区', // 初始化状态下
            scenicList: [],
            map: null,
            heatmap: null,
            heatmapData: {
                西湖: [
                    { lng: 120.149120, lat: 30.229461, count: 10000 },
                    { lng: 120.101378, lat: 30.240852, count: 20000 },
                    { lng: 120.101379, lat: 30.240853, count: 25000 },
                    { lng: 120.101379, lat: 30.240852, count: 20000 },
                    { lng: 120.147041, lat: 30.260794, count: 30000 },
                    { lng: 120.146187, lat: 30.252092, count: 24000 },
                    { lng: 120.146188, lat: 30.252093, count: 28000 },
                    { lng: 120.1388, lat: 30.241747, count: 22000 },
                    { lng: 120.142587, lat: 30.251685, count: 16000 },
                    { lng: 120.142587, lat: 30.251685, count: 30000 },
                    { lng: 120.142587, lat: 30.251684, count: 16000 },
                    { lng: 120.142588, lat: 30.251685, count: 30000 },
                    { lng: 120.142587, lat: 30.251686, count: 20000 },
                    { lng: 120.142586, lat: 30.251685, count: 25000 },
                    { lng: 120.130316, lat: 30.21935, count: 30000 },
                    { lng: 120.130316, lat: 30.21934, count: 20000 },
                    { lng: 120.156092, lat: 30.239814, count: 30000 },
                    { lng: 120.156091, lat: 30.239813, count: 20000 },
                    { lng: 120.133404, lat: 30.231413, count: 30000 },
                    { lng: 120.133454, lat: 30.231413, count: 30000 },
                    { lng: 120.133504, lat: 30.231413, count: 30000 },
                    { lng: 120.133504, lat: 30.231423, count: 30000 },
                ],
                西溪湿地: [
                    { lng: 120.064911, lat: 30.266962, count: 25000 },
                    { lng: 120.081575, lat: 30.27318, count: 25000 },
                    { lng: 120.081574, lat: 30.273179, count: 30000 },
                ],
                千岛湖: [
                    { lng: 119.025671, lat: 29.587624, count: 20000 },
                    { lng: 119.025670, lat: 29.587624, count: 20000 },
                    { lng: 119.025671, lat: 29.587625, count: 20000 },
                    // 其他数据...
                ],
                良渚古城: [
                    { lng: 120.006745, lat: 30.37169, count: 30000 },
                    { lng: 120.028044, lat: 30.377433, count: 30000 },
                    { lng: 120.028045, lat: 30.377434, count: 30000 },
                    // 其他数据...
                ],
                大明山: [
                    { lng: 118.997844, lat: 30.028484, count: 22000 },
                    // 其他数据...
                ],
            }
        };
    },
    name: "HeatMap",
    mounted() {
        this.initMap();
        this.fetchScenicData();  // 用于获取景区数据
    },
    methods: {
        initMap() {
            this.map = new AMap.Map("map", {
                center: [120.1388, 30.241747],
                zoom: 14,
            });
            // 初始化热力图层
            this.heatmap = new AMap.Heatmap(this.map, {
                radius: 50,
                opacity: [0, 0.8],
                gradient: {
                    0.5: "blue",
                    0.65: "rgb(117,211,248)",
                    0.7: "rgb(0, 255, 0)",
                    0.9: "#ffea00",
                    1.0: "red",
                },
            });
            // 设置热力图数据
            this.setHeatmapData();
            // // 初始化地图中心
            // this.setMapCenter();
        },
        changeScenic() {
            // 在这里根据选中的景区设置地图中心
            switch (this.selectedScenic) {
                case '西湖':
                    this.map.setCenter([120.146465, 30.244667]);
                    this.setHeatmapData();
                    break;
                case '千岛湖':
                    this.map.setCenter([119.072218, 29.558612]);
                    this.setHeatmapData();
                    break;
                case '西溪湿地':
                    this.map.setCenter([120.064911, 30.266962]);
                    this.setHeatmapData();
                    break;
                case '良渚古城':
                    this.map.setCenter([120.006745, 30.37169]);
                    this.setHeatmapData();
                    break;
                case '大明山':
                    this.map.setCenter([118.994429, 30.041756]);
                    this.setHeatmapData();
                    break;
                default:
                    break;
            }
        },
        setHeatmapData() {
            // 设置热力图数据
            const data = this.heatmapData[this.selectedScenic] || [];
            this.heatmap.setDataSet({
                data,
                max: 30000,
            });
        },
        fetchScenicData() {
            axios.get('http://localhost:8000/api/scenic/')
            .then(response => {
                this.scenicList = response.data;
            })
            .catch(error => {
                console.error('Error fetching scenic spots:', error);
            });
        },
    },
};
</script>

<style>
.map-container {
    position: relative;
    width: 650px;
    height: 100%;
}
.change-zone .el-select {
    margin-left: 10px;
    margin-top: 10px;
    width: 150px;
    z-index: 2;
}
.map {
    height: 100%;
    margin-top: -50px;
    z-index: 1;
}
</style>