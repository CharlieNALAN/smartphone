<template>
    <div>
        <el-row>
            <el-col :span="22">
                <el-button class="clear_filter" @click="clearFilter">清除所有过滤器</el-button>
                <router-link :to="{ name: 'AttractionAdd' }">
                    <el-button type="primary" plain>新增景点</el-button>
                </router-link>
                <el-form @submit.native.prevent="search" class="search">
                    <el-form-item>
                        <el-input v-model="searchData" placeholder="搜索景点"></el-input>
                        <el-button type="primary" native-type="submit">搜索</el-button>
                    </el-form-item>
                </el-form>
            </el-col>
        </el-row>
        <el-table ref="filterTable" :data="querysetData" style="width: 100%">
            <el-table-column prop="attraction_id" label="ID" width="70"></el-table-column>
            <el-table-column prop="attraction_name" label="景点名称" width="200"></el-table-column>
            <el-table-column prop="address" label="景点地址" :formatter="formatter" width="470">
            </el-table-column>
            <el-table-column prop="scenic" label="所属景区" :filters="scenicFilters" :filter-method="filterScenic"
                filter-placement="bottom-end">
                <template slot-scope="scope">
                    <el-tag :type="getScenicType(scope.row.scenic)" disable-transitions>
                        {{ setScenicName(scope.row.scenic) }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="景点状态" :filters="statusFilters" :filter-method="filterStatus">
                <template slot-scope="scope">
                    <el-tag :type="getStatusType(scope.row.status)" disable-transitions>
                        {{ setStatusName(scope.row.status) }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column fixed="right" label="操作">
                <template #default="scope">
                    <el-button @click="handleView(scope.row)" type="text" size="small">查看</el-button>
                    <el-button @click="handleEdit(scope.row)" type="text" size="small">编辑</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination :total="totalItems" :current-page.sync="currentPage" @current-change="handleCurrentChange"
            @prev-click="prevPage" @next-click="nextPage">
        </el-pagination>

        <!-- 编辑和查看对话框 -->
        <el-dialog :visible.sync="dialogVisible" :title="dialogTitle" width="50%" :before-close="handleClose">
            <!-- 编辑表单 -->
            <template v-if="dialogType === 'edit'">
                <el-form ref="editForm" :model="editForm" label-width="120px">
                    <el-form-item label="景点名称" prop="attraction_name">
                        <el-input v-model="editForm.attraction_name"></el-input>
                    </el-form-item>
                    <el-form-item label="所属景区">
                        <el-select v-model="editForm.scenic" :disabled="true">
                            <el-option v-for="scenic in scenicOptions" :key="scenic.scenic_id" :label="scenic.scenic_name"
                                :value="scenic.scenic_id"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="景点地址">
                        <el-input v-model="editForm.address" placeholder="请输入景点地址"></el-input>
                    </el-form-item>
                    <el-form-item label="景点描述">
                        <el-input type="textarea" v-model="editForm.description" placeholder="请输入景点描述"></el-input>
                    </el-form-item>
                    <el-form-item label="景点类别">
                        <el-radio-group v-model="editForm.category">
                            <el-radio :label="1">自然风光</el-radio>
                            <el-radio :label="2">历史遗迹</el-radio>
                            <el-radio :label="3">文化遗产</el-radio>
                            <el-radio :label="4">娱乐体验</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="景点门票">
                        <el-input v-model="editForm.fee" placeholder="请输入景点门票"></el-input>
                    </el-form-item>
                    <el-form-item label="开放时间">
                        <el-time-picker v-model="editForm.open_time" placeholder="选择开放时间"></el-time-picker>
                    </el-form-item>
                    <el-form-item label="关闭时间">
                        <el-time-picker v-model="editForm.close_time" placeholder="选择关闭时间"></el-time-picker>
                    </el-form-item>
                    <el-form-item label="人流量限制">
                        <el-input v-model="editForm.flow_limit" placeholder="请输入人流量限制"></el-input>
                    </el-form-item>
                    <el-form-item label="景点状态">
                        <el-radio-group v-model="editForm.status">
                            <el-radio :label="0">未开放</el-radio>
                            <el-radio :label="1">开放中</el-radio>
                            <el-radio :label="2">人流预警</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="景点电话">
                        <el-input v-model="editForm.phone" placeholder="请输入景点电话"></el-input>
                    </el-form-item>
                    <el-form-item label="景点图片">
                        <el-upload :action="'http://localhost:8000/attraction/' + editForm.attraction_id + '/'"
                            :show-file-list="false" :on-success="handleUploadSuccess" name="image"
                            :http-request="uploadImage" :before-upload="beforeUpload">
                            <!-- 添加 name 属性，确保上传的文件字段名为 'image' -->
                            <el-button size="small" type="primary">点击上传</el-button>
                        </el-upload>
                        <!-- <el-upload class="upload-demo"
                            action="http://localhost:8000/media/attraction_images/"
                            :on-success="handleUploadSuccess" :show-file-list="false" >
                            <el-button size="small" type="primary">点击上传</el-button>
                        </el-upload> -->
                        <!-- <el-upload class="upload-demo" drag
                                :action="'http://localhost:8000/attraction/' + editForm.attraction_id + '/'"
                                :on-success="handleUploadSuccess" :show-file-list="true" :http-request="uploadImage"
                                multiple>
                                <i class="el-icon-upload"></i>
                                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                                <div class="el-upload__tip" slot="tip">只能上传jpg/png文件，且不超过500kb</div>
                            </el-upload> -->
                    </el-form-item>
                </el-form>
            </template>

            <!-- 查看表单 -->
            <template v-else-if="dialogType === 'view'">
                <!-- 查看表单内容 -->
                <!-- 表单内容省略 -->
                <!-- 示例： -->
                <!-- <el-input v-model="viewForm.attraction_name" placeholder="景点名称" disabled></el-input> -->
                <!-- 其他表单项 -->
            </template>

            <!-- 底部操作按钮 -->
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <!-- 保存按钮仅在编辑对话框中显示 -->
                <el-button v-if="dialogType === 'edit'" type="primary" @click="saveEdit">保存</el-button>
            </span>
        </el-dialog>
    </div>
</template>
  
<script>
import axios from 'axios';

export default {
    data() {
        return {
            searchData: '',
            querysetData: [],
            totalItems: 0,
            currentPage: 1,
            scenicFilters: [], // 景区过滤器选项
            statusFilters: [
            { text: '未开放', value: '0' }, { text: '开放中', value: '1' }, { text: '人流预警', value: '2' }
            ],
            selectedScenic: '',
            imageUrl: '',
            // 对话框可见性
            dialogVisible: false,
            // 对话框类型（'edit' 或 'view'）
            dialogType: '',
            // 对话框标题
            dialogTitle: '',
            // 编辑表单数据
            editForm: {},
            // 查看表单数据
            viewForm: {},
            // scenicOptions: []  // 所属景区选项
        };
    },
    computed: {
        scenicOptions() {
            return this.$store.state.scenicOptions;
        }
    },
    mounted() {
        this.fetchData(); // 在组件挂载后立即获取数据
        this.fetchScenicFilters(); // 获取标签过滤器选项
        // 页面加载时获取所属景区数据
        // this.fetchScenicOptions();
    },
    created() {
        // 在组件创建时获取 scenic options  
        this.$store.dispatch('fetchScenicOptions');
    },
    methods: {
        // fetchData() {
        //     const params = {
        //         search: this.searchData,
        //         scenic: this.selectedScenic // 将选择的所属景区作为参数发送给后端
        //     };
        //     axios.get('http://localhost:8000/api/attractionlist/', { params })  // 发送 GET 请求获取数据
        //         .then(response => {
        //             // 请求成功，将返回的数据赋值给相应的数据属性
        //             this.querysetData = response.data.queryset;
        //             this.totalItems = response.data.totalItems;
        //             this.currentPage = response.data.currentPage;
        //         })
        //         .catch(error => {
        //             // 请求失败，打印错误信息
        //             console.error('Error fetching data:', error);
        //         });
        // },
        fetchData() {
            const params = {
                search: this.searchData,
                scenic: this.selectedScenic, // 将选择的所属景区作为参数发送给后端
                page: this.currentPage
            };
            axios.get('http://localhost:8000/attraction', { params })  // 发送 GET 请求获取数据
                .then(response => {
                    // 请求成功，将返回的数据赋值给相应的数据属性
                    this.querysetData = response.data.results;
                    this.totalItems = response.data.count;
                    console.log(this.totalItems);
                    // this.currentPage = response.data.currentPage;
                })
                .catch(error => {
                    // 请求失败，打印错误信息
                    console.error('Error fetching data:', error);
                });
        },
        fetchScenicFilters() {
            axios.get('http://localhost:8000/api/scenic/')
                .then(response => {
                    this.scenicFilters = response.data.map(scenic => ({
                        text: scenic.scenic_name,
                        value: scenic.scenic_id,
                    }));
                })
                .catch(error => {
                    // 请求失败，打印错误信息
                    console.error('Error fetching data:', error);
                });
        },
        // fetchScenicOptions() {
        //     // 发送请求获取所属景区数据
        //     axios.get('http://localhost:8000/api/scenic/')
        //         .then(response => {
        //             // 将获取到的数据赋值给 scenicOptions
        //             this.scenicOptions = response.data;
        //             // 设置编辑表单的所属景区名称
        //             this.setScenicName();
        //         })
        //         .catch(error => {
        //             console.error('Error fetching scenic options:', error);
        //         });
        // },
        setScenicName() {
            // 根据编辑表单的所属景区ID，设置对应的景区名称
            const foundOption = this.scenicOptions.find(option => option.scenic_id === this.editForm.scenic);
            if (foundOption) {
                this.editForm.scenic = foundOption.scenic_name;
            }
        },
        search() {
            // 处理搜索功能
            this.fetchData(); // 搜索后重新获取数据
        },
        filterScenic(value, row) {
            // this.selectedScenic = value;
            // this.fetchData();
            return row.scenic == value; // 根据过滤器的值来过滤表格数据
        },
        filterStatus(value, row) {
            return row.status == value; // 根据过滤器的值来过滤表格数据
        },
        getScenicType(scenic) {
            // 根据 scenicName 返回相应的标签类型
            if (scenic == '1') {
                return 'primary';
            } else if (scenic == '3') {
                return 'primary';
            } else if (scenic == '5') {
                return 'primary';
            }
            return 'warning';
        },
        setScenicName(scenic) {
            if (scenic == '1') {
                return '西湖';
            } else if (scenic == '2') {
                return '西溪湿地';
            } else if (scenic == '3') {
                return '千岛湖';
            } else if (scenic == '4') {
                return '良渚古城';
            }
            return '大明山';
        },
        getStatusType(status) {
            // 根据 scenicName 返回相应的标签类型
            if (status == '1') {
                return 'success';
            } else if (status == '2') {
                return 'danger';
            } else if (status == '0') {
                return 'info';
            }
            return 'success';
        },
        setStatusName(status) {
            if (status == '0') {
                return '未开放';
            } else if (status == '1') {
                return '开放中';
            } else if (status == '2') {
                return '人流预警';
            }
            return '未开放';
        },
        clearFilter() {
            // 清除过滤器
            // this.searchData = ''; // 清空搜索框
            this.selectedScenic = ''; // 清空所属景区筛选条件
            this.fetchData(); // 清除过滤器后重新获取数据
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.fetchData(); // 切换页面时重新获取数据
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
                this.fetchData(); // 切换页面时重新获取数据
            }
        },
        // 编辑景点信息
        handleEdit(row) {
            // 发送 GET 请求获取景点详细信息
            axios.get(`http://localhost:8000/attraction/${row.attraction_id}/`)
                .then(response => {
                    this.editForm = response.data;
                    this.imageUrl = response.data.image;
                    this.dialogType = 'edit';
                    this.dialogVisible = true;
                    this.dialogTitle = '编辑景点信息';
                })
                .catch(error => {
                    console.error('Error fetching attraction details:', error);
                });
        },
        // 查看景点信息
        handleView(row) {
            // 发送 GET 请求获取景点详细信息
            axios.get(`http://localhost:8000/attraction/${row.attraction_id}/`)
                .then(response => {
                    this.dialogType = 'view';
                    this.dialogVisible = true;
                    this.dialogTitle = '查看景点信息';
                    // 为查看表单赋值
                    this.viewForm = response.data;
                })
                .catch(error => {
                    console.error('Error fetching attraction details:', error);
                });
        },
        // 保存编辑
        saveEdit() {
            axios.put(`http://localhost:8000/attraction/${this.editForm.attraction_id}/`, this.editForm)
                .then(response => {
                    console.log('Edit saved successfully:', response.data);
                    this.dialogVisible = false;
                    // 刷新页面或重新加载数据
                    this.fetchData();
                })
                .catch(error => {
                    console.error('Error saving edit:', error);
                });
        },
        beforeUpload(file) {
            console.log('File object:', file);
            const formData = new FormData();
            formData.set('image', file); // 确保文件对象被正确添加到 FormData 中
            console.log('FormData:', formData);
            return true;
        },
        handleUploadSuccess(response, file, fileList) {
            console.log('上传成功，文件对象:', response);
            // this.imageUrl = URL.createObjectURL(file.raw);
            // console.log('上传成功:', response);
            this.editForm.image = response.image;
        },
        uploadImage(file) {
            let formData = new FormData();
            if (this.editForm) {
                Object.keys(this.editForm).forEach(key => {
                    formData.append(key, this.editForm[key]);
                });
            }
            formData.append('image', file.raw);
            console.log(formData);
            return axios.put(`http://localhost:8000/attraction/${this.editForm.attraction_id}/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
        },
        deleteItem(attractionId) {
            // 处理删除功能
        },
        handleCurrentChange(val) {
            // 处理分页变更
            this.currentPage = val;
            // 发起 API 调用以获取新页的数据
            this.fetchData(); // 分页变更后重新获取数据
        },
        handleClose() {
            this.$confirm('确认关闭？')
                .then(_ => {
                    this.dialogVisible = false;
                })
                .catch(_ => { });
        },
        formatter(row, column) {
            return row.address;
        },
    }
};
</script>
  
<style scoped>
.search {
    position: relative;
    float: right;
}

.search .el-button {
    position: absolute;
    margin-left: 20px;
}

.clear_filter {
    float: left;
}
</style>
  