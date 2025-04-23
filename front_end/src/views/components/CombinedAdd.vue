<template>
    <div>
        <el-form :model="form" label-width="100px">
            <el-form-item label="策略名称">
                <el-input v-model="form.strategy_name"></el-input>
            </el-form-item>
            <el-form-item label="所属景区">
                <el-select v-model="form.scenic" placeholder="请选择">
                    <el-option v-for="scenic in scenicOptions" :key="scenic.scenic_id" :label="scenic.scenic_name"
                        :value="scenic.scenic_id"></el-option>
                </el-select>
            </el-form-item>
            <div class="hh">
                <el-checkbox v-model="use.checked1" border>
                    <br>
                    <span class="Rtitle">按景点热度推荐</span><br>
                    <span>历史人流量高的景区得到优先推荐，热度高到低排序</span>
                </el-checkbox>
                <span class="param">
                    <span class="ll1">
                        冷启动签到次数<br>达到
                        <el-input size="mini" class="ininin" v-model="combineStg[1].stgParam"></el-input>
                        次
                    </span>
                    <br>
                    <img class="img" src="../../assets/arrow.gif"/>
                    <span class="ll2">
                        <br>启用下一步骤
                    </span>
                </span>
                <el-checkbox v-model="use.checked2" border>
                    <br>
                    <span class="Rtitle">个性化推荐</span><br>
                    <span>根据用户短时时序数据推算用户下一步推荐景点，热度高到低排序</span>
                </el-checkbox>
                <span class="param">
                    <span class="ll1">
                        景区拥挤景点比例<br>达到
                        <el-input size="mini" class="ininin" v-model="combineStg[2].stgParam"></el-input>
                        %
                    </span>
                    <br>
                    <img class="img" src="../../assets/arrow.gif"/>
                    <span class="ll2">
                        <br>启用下一步骤
                    </span>
                </span>
                <el-checkbox v-model="use.checked3" border>
                    <br>
                    <span class="Rtitle">按实时人数推荐</span><br>
                    <span>分析后台数据，将人流少的景点推荐给用户，实现动态调控平衡</span>
                </el-checkbox>
            </div>
        </el-form>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            form: {
                strategy_name: '',
                scenic: '',
            },
            use: {
                checked1: '',
                checked2: '',
                checked3: '',
            },
            oneStg: {//单一策略配置表单数据
                stgSelect: '',
                stgName: ''
            },
            combineStg: [//组合策略配置表单数据
                {//1st:根据景点热度进行推荐
                    stgSelect: '',
                    stgName: '',
                    stgParam: null
                },
                {//2nd:根据景点热度进行推荐
                    stgSelect: '',
                    stgName: '',
                    stgParam: null
                },
                {//3rd:根据景区实时人数进行调度
                    stgSelect: '',
                    stgName: '',
                    stgParam: null
                },

            ],
            // 初始化筛选标签数组  
            categoryFilters: [
                { text: '自然风光', value: '1' },
                { text: '历史遗迹', value: '2' },
                { text: '文化遗产', value: '3' },
                { text: '娱乐体验', value: '4' }
            ],
            allAttractions: [],
            dialogFormVisible: false,
            selectedAttractions: [], // 已选择的景点
            filteredAttractions: [], // 根据筛选条件过滤后的景点列表
            selectedScenic: null, // 当前选中的景区
            sortableInstance: null
        }
    },
    computed: {
        scenicOptions() {
            return this.$store.state.scenicOptions;
        },
    },
    created() {
        this.$store.dispatch('fetchScenicOptions');
    },
    methods: {
        handleSave() {
            this.c_dialogVisible = false;
        }
    }
}
</script>

<style scoped>
.Rtitle {
    margin-bottom: 10px;
    display: inline-block;
}

.param {
    width: 129px;
    height: 200px;
    background-color: #EBEEF5;
    margin-right: 10px;
    display: inline-block;
    float: left;
}

.stg {
    margin-top: 15px;
    height: 500px;
}

.el-checkbox {
    width: 270px;
    margin-right: 8px;
    height: 200px;
    float: left;
    white-space: normal;
}

.hh {
    height: 200px;
}

.img {
    width: 120px;
    margin-top: -35px;
    margin-bottom: -40px;
}

.ll1 {
    display: inline-block;
    margin-left: 10px;
    margin-top: 35px;
}

.ll2 {
    display: inline-block;
    margin-top: -30px;
    margin-left: 15px;
}

.ininin {
    width: 60px;
}

.btnnn {
    margin-left: 80px;
    /*margin-top: 10px;*/
}
</style>