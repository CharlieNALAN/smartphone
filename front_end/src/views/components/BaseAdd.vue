<template>
    <el-form ref="baseForm" :model="form" label-width="100px">
        <el-form-item label="策略名称">
            <el-input v-model="form.strategy_name"></el-input>
        </el-form-item>
        <el-form-item label="所属景区">
            <el-select v-model="form.scenic" placeholder="请选择">
                <el-option v-for="scenic in scenicOptions" :key="scenic.scenic_id" :label="scenic.scenic_name"
                    :value="scenic.scenic_id"></el-option>
            </el-select>
        </el-form-item>
        <el-form-item label="策略类型选择">
            <el-radio-group v-model="form.strategy_select">
                <el-radio class="radio" value="1" label="1">
                    <span class="Rtitle">按实时人数推荐</span><br>
                    <span>分析后台数据，将人流少的景点推荐给用户，实现动态调控平衡</span>
                </el-radio>
                <br>
                <el-radio class="radio" value="2" label="2">
                    <span class="Rtitle">按景点热度推荐</span><br>
                    <span>历史人流量高的景区得到优先推荐，热度高到低排序</span>
                </el-radio>
                <br>
                <el-radio class="radio" value="5" label="5">
                    <span class="Rtitle">个性化推荐</span><br>
                    <span>根据用户短时时序数据推算用户下一步推荐景点</span>
                </el-radio>
            </el-radio-group>
        </el-form-item>
        <el-button style="margin-top: 10px" @click="handleBaseSave" :disabled="isSaveDisabled">保存</el-button>
        <el-button style="margin-top: 10px" @click="handleBaseClose">取消</el-button>
    </el-form>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            form: {
                strategy_name: '',
                scenic: '',
                strategy_select: ''
            },
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
        handleBaseClose() {
            this.$emit('close-dialog');
        },
        handleBaseSave() {
            // 构造要保存的数据对象
            const formData = {
                strategy_name: this.form.strategy_name,
                scenic: this.form.scenic,
                strategy_type: this.form.strategy_select
            };
            console.log(formData);
            // 发送POST请求保存数据
            axios.post('http://localhost:8000/recommendation-strategies/', formData)
                .then(response => {
                    // 获取保存成功后返回的数据
                    const savedData = response.data;

                    // 提示保存成功
                    this.$message({
                        type: 'success',
                        message: '策略保存成功'
                    });

                    this.$emit('close-dialog');

                    // 可以根据需要进行其他操作，例如重新加载数据等
                })
                .catch(error => {
                    // 提示保存失败
                    this.$message.error('策略保存失败，请重试');

                    // 打印错误信息
                    console.error('保存失败：', error);
                });
        }

    }
}
</script>

<style scoped>
.radio {
    width: 200px;
    height: 80px;
    padding: 20px;
    background-color: whitesmoke;
    margin-bottom: 15px;
    border-radius: 12px;
    border: #909399 1px solid;
}

.radio span {
    white-space: normal;
    line-height: 20px;
}

.Rtitle {
    margin-bottom: 10px;
    display: inline-block;
}

.form {
    margin-top: 15px;
    height: 500px;
}
</style>