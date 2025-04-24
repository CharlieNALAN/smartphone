<template>
    <el-container>
        <el-header style="background-color: rgb(130, 173, 252)">SmartTravel</el-header>
        <el-container>
            <el-main>
                <el-radio-group v-model="radio">
                    <el-radio :label="1">Today</el-radio>
                    <el-radio :label="2">Yesterday</el-radio>
                    <el-radio :label="3">This Week</el-radio>
                    <el-radio :label="4">This Month</el-radio>
                </el-radio-group>
                <!-- <div class="echarts1" ref="areaChart" style="width:500px; height: 300px;"></div> -->
                <!-- <router-view></router-view> -->
             </el-main>
        </el-container>
    </el-container>
</template>

<script>
// // echarts的配置数据
// import { areaChartConfig } from '../echartsConfig'
export default {
    data() {
        return{
            radio: '1',
        }
    },
    components:{
        
    },
    mounted() {
        // console.log('Component mounted');
        areaChartConfig.renderAreaChart(this.$refs.areaChart);
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
.echarts1{
    margin-top: 20px;
    /* margin-left: 100px; */
}
</style>