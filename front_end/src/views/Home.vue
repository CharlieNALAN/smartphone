<template>
    <div>
      <el-container>
        <el-aside width="55%">
            <heat-map style="width: 100%;height: 800px;float: left"></heat-map>
        </el-aside>
        <el-main id="data">
          <PresentData></PresentData>
        </el-main>
      </el-container>
    </div>
</template>

<script>
// import CommonAside from '@/components/CommonAside.vue'
// import MapContainer from '../components/MapContainer.vue'
import HeatMap from './components/HeatMap.vue'
import PresentData from './components/PresentData.vue'

// import * as echarts from 'echarts'
// // echarts的配置数据
// import { areaChartConfig } from '../echartsConfig'
export default {
    data() {
        return{
            radio: '1',
        }
    },
    components:{
        // CommonAside,
        // MapContainer,
        HeatMap,
        PresentData
    },
    mounted() {
        // console.log('Component mounted');
        // areaChartConfig.renderAreaChart(this.$refs.areaChart);
        // this.renderRingChart();
        // this.renderBarChart();
    },
    
}
</script>

<style>
.el-header{
    padding:0;
}
.el-main{
    float: left;
}
.el-group-radio{
    clear: left;
}

</style>