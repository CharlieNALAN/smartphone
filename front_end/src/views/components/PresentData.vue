<template>
    <div>
        <NoticeBar></NoticeBar>
        <br>
        <!--    <el-alert-->
        <!--      title="景区实时情况刷新间隔：60s"-->
        <!--      type="info"-->
        <!--      >-->
        <!--    </el-alert>-->
        <i class="el-icon-warning">流量预警</i>
        <span class="interval">(刷新间隔:60s)</span>
        <span @click="refresh">
            <i class="el-icon-refresh-left"></i>
        </span>
        <el-table :data="warningData" :cell-style="setCellColor" style="width: 100%;margin-left: 20px;">
            <el-table-column prop="poiName" label="景点名称" width="120">
            </el-table-column>
            <el-table-column prop="percentage" label="流量" width="210">
                <template slot-scope="scope">
                    <!--          {{scope.row.name}}-->
                    <el-progress :percentage="scope.row.percentage" :stroke-width="10" :width="50"
                        :color="colors"></el-progress>
                </template>
            </el-table-column>
            <el-table-column prop="delta" align="right" label="较上个时段人数变化" width="160">
            </el-table-column>
        </el-table>

        <i class="el-icon-time">实时流量</i>
        <span class="interval">(刷新间隔:60s)</span>
        <span @click="refresh">
            <i class="el-icon-refresh-left"></i>
        </span>
        <el-table :cell-style="setCellColor" :data="allData" style="width: 700px;margin-left: 20px;">
            <el-table-column prop="poiName" label="景点名称" width="120">
            </el-table-column>
            <!--      <el-table-column-->
            <!--        prop="num"-->
            <!--        label="流量"-->
            <!--        sortable-->
            <!--        width="160">-->
            <!--      </el-table-column>-->
            <el-table-column prop="percentage" label="流量" sortable width="210">
                <template slot-scope="scope">
                    <!--          {{scope.row.name}}-->
                    <el-progress :percentage="scope.row.percentage" :stroke-width="10" :width="50"
                        :color="colors"></el-progress>
                </template>
            </el-table-column>
            <el-table-column prop="delta" align="right" sotable label="较上个时段人数变化" width="160">
            </el-table-column>
        </el-table>

        <!--    <el-card>-->
        <!--      今日未正常开放景点-->
        <!--      <br><br>-->
        <!--      龙井八景景区-->
        <!--    </el-card>-->
    </div>
</template>
  
<script>
import NoticeBar from '../components/NoticeBar'

export default {

    name: "PresentData",
    components: {
        NoticeBar
    },
    data() {
        return {
            percentage: 10,
            colors: [
                { color: '#ffa500', percentage: 20 },
                { color: '#0dbf8c', percentage: 40 },
                { color: '#E6A23C', percentage: 60 },
                { color: '#ffa500', percentage: 80 },
                { color: '#F56C6C', percentage: 100 }
            ],
            warningData: [
                {
                    poiName: '灵隐寺',
                    num: 38190,
                    percentage: 92,
                    delta: '+200'
                },
                {
                    poiName: '三潭印月',
                    num: 30290,
                    percentage: 72,
                    delta: '+172'
                },
                {
                    poiName: '太子湾公园',
                    num: 20190,
                    percentage: 88,
                    delta: '+192'
                },
            ],
            allData: [
                {
                    poiName: '杭州植物园',
                    num: 282,
                    percentage: 67,
                    delta: '+12'
                },
                {
                    poiName: '曲苑风荷',
                    num: 190,
                    percentage: 46,
                    delta: '+19'
                },
                {
                    poiName: '灵隐寺',
                    num: 38190,
                    percentage: 92,
                    delta: '+200'
                },
                {
                    poiName: '苏东坡纪念馆',
                    num: 30290,
                    percentage: 72,
                    delta: '+172'
                },
                {
                    poiName: '太子湾公园',
                    num: 20190,
                    percentage: 88,
                    delta: '+192'
                },
                {
                    poiName: '三潭印月',
                    num: 200,
                    percentage: 22,
                    delta: '-15'
                },
                {
                    poiName: '苏堤春晓',
                    num: 182,
                    percentage: 55,
                    delta: '-72'
                },
                {
                    poiName: '杭州动物园',
                    num: 282,
                    percentage: 63,
                    delta: '-22'
                }
            ]
        }
    },
    methods: {
        refresh() {
            // location.reload()

            setTimeout(null, 500)
            this.warningData = [
                {
                    poiName: '一线天',
                    num: 30290,
                    percentage: 70,
                    delta: '-142'
                },
                {
                    poiName: '太子湾公园',
                    num: 20190,
                    percentage: 82,
                    delta: '+142'
                },
            ]
            this.allData = [
                {
                    poiName: '三潭印月',
                    num: 200,
                    percentage: 22,
                    delta: '-15'
                },
                {
                    poiName: '楼外楼',
                    num: 182,
                    percentage: 55,
                    delta: '-72'
                },
                {
                    poiName: '知味观',
                    num: 282,
                    percentage: 63,
                    delta: '-22'
                },
                {
                    poiName: '杭州植物园',
                    num: 282,
                    percentage: 67,
                    delta: '+12'
                },
                {
                    poiName: '曲苑风荷',
                    num: 190,
                    percentage: 46,
                    delta: '+19'
                },
                {
                    poiName: '灵隐寺',
                    num: 38190,
                    percentage: 92,
                    delta: '+200'
                },
                {
                    poiName: '一线天',
                    num: 30290,
                    percentage: 72,
                    delta: '+172'
                },
                {
                    poiName: '太子湾公园',
                    num: 20190,
                    percentage: 88,
                    delta: '+192'
                },

            ]
        },
        setCellColor({ row, column, rowIndex, columnIndex }) {
            if (columnIndex === 2) {
                if (row.delta > 0) {
                    // console.log(row.status)
                    return 'color: #F56C6C'
                } else {
                    return 'color: #67C23A'
                }
            }
        },
    }
}
</script>
  
<style scoped>
.el-icon-time {
    margin-top: 25px;
    margin-bottom: 10px;
    font-size: 20px;
    color: #67C23A;
    margin-left: 15px;
}

.el-icon-warning {
    margin-left: 15px;
    margin-top: 10px;
    margin-bottom: 10px;
    font-size: 20px;
    color: #F56C6C;
}

.interval {
    color: grey;
    font-size: 15px;
    margin-left: 10px;
}
</style>
  