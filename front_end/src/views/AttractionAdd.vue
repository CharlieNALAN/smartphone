<template>
    <div>
        <h1>新增景点</h1>
        <div class="container">
            <div class="map-add">
                <el-amap :events="events" :zoom="zoom" v-model="mapCenter" @click="handleMapClick"
                    style="width: 100%; height: 100%;">
                </el-amap>
            </div>
            <el-form ref="ruleForm" :model="ruleForm" :rules="rules" label-width="120px" enctype="multipart/form-data">
                <el-form-item label="景点名称" prop="attraction_name">
                    <el-input v-model="ruleForm.attraction_name"></el-input>
                </el-form-item>
                <el-form-item label="所属景区" prop="scenic">
                    <el-select v-model="ruleForm.scenic" placeholder="请选择所属景区" @change="handleScenicChange">
                        <el-option v-for="scenic in scenicOptions" :key="scenic.scenic_id" :label="scenic.scenic_name"
                            :value="scenic.scenic_id">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="景点经度" prop="attraction_lng">
                    <el-input v-model="ruleForm.attraction_lng"></el-input>
                </el-form-item>
                <el-form-item label="景点纬度" prop="attraction_lat">
                    <el-input v-model="ruleForm.attraction_lat"></el-input>
                </el-form-item>
                <el-form-item label="景点地址" prop="address">
                    <el-input v-model="ruleForm.address"></el-input>
                </el-form-item>
                <el-form-item label="景点描述" prop="description" placeholder="请输入景点描述">
                    <el-input type="textarea" v-model="ruleForm.description"></el-input>
                </el-form-item>
                <el-form-item label="景点类别" prop="category">
                    <el-radio-group v-model="ruleForm.category">
                        <el-radio :label="1">自然风光</el-radio>
                        <el-radio :label="2">历史遗迹</el-radio>
                        <el-radio :label="3">文化遗产</el-radio>
                        <el-radio :label="4">娱乐体验</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="景点门票" prop="fee">
                    <el-input v-model="ruleForm.fee" placeholder="请输入景点门票"></el-input>
                </el-form-item>
                <el-form-item label="开放时间" prop="open_time">
                    <el-time-picker v-model="ruleForm.open_time" placeholder="选择开放时间"></el-time-picker>
                </el-form-item>
                <el-form-item label="关闭时间" prop="close_time">
                    <el-time-picker v-model="ruleForm.close_time" placeholder="选择关闭时间"></el-time-picker>
                </el-form-item>
                <el-form-item label="人流量限制" prop="flow_limit">
                    <el-input v-model="ruleForm.flow_limit" placeholder="请输入人流量限制"></el-input>
                </el-form-item>
                <el-form-item label="景点状态" prop="status">
                    <el-radio-group v-model="ruleForm.status">
                        <el-radio :label="0">未开放</el-radio>
                        <el-radio :label="1">开放中</el-radio>
                        <el-radio :label="2">人流预警</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="景点电话" prop="phone">
                    <el-input v-model="ruleForm.phone" placeholder="请输入景点电话"></el-input>
                </el-form-item>
                <el-form-item label="景点图片">
                    <el-upload name="image" class="upload-demo" action="http://localhost:8000/api/image/upload/"
                        :on-preview="handlePreview" :on-remove="handleRemove" :before-remove="beforeRemove"
                        :on-exceed="handleExceed" :on-success="handleSuccess">
                        <el-button size="small" type="primary">点击上传</el-button>
                    </el-upload>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import router from '@/router';
export default {
    data() {
        return {
            mapCenter: [120.146465, 30.244667],
            zoom: 14,
            events: {
                // 当地图容器完成初始化，即地图完成所有绘制工作后触发  
                init: (instance) => {
                    this.mapInstance = instance; // 保存地图实例  
                    this.setCenter(); // 初始化后设置中心点  
                },
                click: this.handleMapClick,
            },
            ruleForm: {
                attraction_name: '',
                scenic: null,
                address: '',
                attraction_lng: '', // 景点经度
                attraction_lat: '', // 景点纬度
                description: '',
                category: '',
                fee: '',
                open_time: '',
                close_time: '',
                flow_limit: '',
                status: '',
                phone: '',
                // image: ''
            },
            rules: {
                attraction_name: [
                    { required: true, message: '请输入景点名称', trigger: 'blur' }
                ],
                scenic: [
                    { required: true, message: '请选择所属景区', trigger: 'change' }
                ],
                address: [
                    { required: true, message: '请输入景点地址', trigger: 'blur' }
                ],
                category: [
                    { required: true, message: '请选择景点类别', trigger: 'change' }
                ],
                // 其他规则
            },
            selectedScenic: {}
        };
    },
    computed: {
        scenicOptions() {
            return this.$store.state.scenicOptions;
        }
    },
    mounted() {
        this.handleScenicChange();
    },
    created() {
        // 在组件创建时获取 scenic options  
        this.$store.dispatch('fetchScenicOptions');
    },
    methods: {
        setCenter() {
            if (this.mapInstance) {
                this.mapInstance.setCenter(this.mapCenter); // 调用高德地图API的setCenter方法  
            }
        },
        handleScenicChange() {
            if (this.ruleForm.scenic) {
                // 使用 Array.prototype.find 方法找到匹配的 scenic 对象  
                this.selectedScenic = this.scenicOptions.find(scenic => scenic.scenic_id === this.ruleForm.scenic);
                if (this.selectedScenic) {
                    // 现在你可以使用 scenicLat 和 scenicLng 了  
                    console.log(`Latitude: ${this.selectedScenic.scenic_lat}, Longitude: ${this.selectedScenic.scenic_lng}`);
                } else {
                    // 如果没有找到匹配的 scenic 对象，则处理这种情况  
                    console.log('No scenic found with the given scenic_id.');
                }
                this.mapCenter = [this.selectedScenic.scenic_lng, this.selectedScenic.scenic_lat];
                this.setCenter();
                console.log(this.mapCenter);
            } else {
                // 如果未选择景区，默认地图中心为某个默认位置
                this.mapCenter = [120.146465, 30.244667]; // 这里可以设置默认的中心点经纬度
            }
        },
        handleMapClick(e) {
            this.ruleForm.attraction_lng = e.lnglat.getLng();
            this.ruleForm.attraction_lat = e.lnglat.getLat();
        },
        handleSuccess(response, file, fileList) {
            console.log('上传成功，文件对象:', response);
            // this.ruleForm.image = response.url;
        },
        // 提交表单
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    const openTime = this.ruleForm.open_time.toLocaleTimeString('en-US', { hour12: false });
                    this.ruleForm.open_time = openTime.split(' ')[0]; // 保留时间部分
                    const closeTime = this.ruleForm.close_time.toLocaleTimeString('en-US', { hour12: false });
                    this.ruleForm.close_time = closeTime.split(' ')[0];
                    console.log(this.ruleForm);
                    const formData = new FormData(); // 创建一个 FormData 对象
                    for (let key in this.ruleForm) {
                        // 将表单数据添加到 FormData 对象中
                        formData.append(key, this.ruleForm[key]);
                    }
                    // 提交表单数据到后端 API
                    axios.post('http://localhost:8000/attraction/', formData, {
                        headers: {
                            'Content-Type': 'multipart/form-data' // 设置 Content-Type 头部
                        }
                    })
                        .then(response => {
                            // 提交成功后的处理逻辑
                            console.log('Attraction submitted successfully:', response.data);
                            router.push('/attractions'); 
                        })
                        .catch(error => {
                            console.error('Error submitting attraction:', error);
                        });
                } else {
                    console.log('Form validation failed');
                    return false;
                }
            });
        },

    }
};
</script>
  
<style scoped>
.container {
    display: flex;
    justify-content: space-between;
    /* 或者使用其他值来调整元素间的空间 */
}

.map-add,
.form {
    flex: 1;
    /* 使得两个div各占据一半的容器宽度 */
}
</style>