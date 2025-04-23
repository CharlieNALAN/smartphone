<template>
    <div>
        <el-form :model="editFormData" label-width="80px">
            <el-form-item label="路线名称">
                <el-input v-model="editFormData.route_name"></el-input>
            </el-form-item>
            <el-form-item label="所属景区">
                <el-select v-model="editFormData.scenic" :disabled="true">
                    <el-option v-for="scenic in scenicOptions" :key="scenic.scenic_id" :label="scenic.scenic_name"
                        :value="scenic.scenic_id"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="路线描述">
                <el-input type="textarea" v-model="editFormData.route_description"></el-input>
            </el-form-item>
            <el-form-item label="景点顺序">
                <el-row>
                    <el-button style="margin-top: 10px" @click="handleAdd" type="primary" plain>新增景点</el-button>
                </el-row>
                <el-row>
                    <el-col :span="24" v-for="(attraction, index) in editFormData.custom_lists"
                        :key="attraction.attraction.attraction_id">
                        <div>{{ attraction.attraction.attraction_name }}</div>
                        <!-- 拖拽按钮 -->
                        <el-button size="mini" v-if="index > 0" @click="moveUp(index)">上移</el-button>
                        <el-button size="mini" v-if="index < editFormData.custom_lists.length - 1"
                            @click="moveDown(index)">下移</el-button>
                        <el-button size="mini" @click="removeAttraction(index)">删除</el-button>
                    </el-col>
                </el-row>
            </el-form-item>
        </el-form>
        <!-- 确定和取消按钮 -->
        <span slot="footer" class="dialog-footer footer-button-container">
            <el-button type="primary" @click="saveEdit">确 定</el-button>
        </span>
        <el-dialog title="新增景点" :visible.sync="dialogFormVisible">
            <el-table ref="multipleTable" :data="attractions" row-key="attraction_id"
                @selection-change="handleSelectionChange">
                <el-table-column type="selection" width="55" />
                <el-table-column prop="attraction_name" label="景点名称" width="200" />
                <el-table-column prop="category" label="景点类别" :filters="categoryFilters" :filter-method="filterTag"
                    filter-placement="bottom-end">
                    <template slot-scope="scope">
                        <el-tag :type="getTagType(scope.row.category)" disable-transitions>
                            {{ setCategory(scope.row.category) }}
                        </el-tag>
                    </template>
                </el-table-column>
            </el-table>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="confirmAdd">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    props: {
        routeId: { // 接收父组件传递的路线ID
            type: Number,
            required: true
        }
    },
    data() {
        return {
            editFormData: {
                route_name: '',
                scenic: '',
                route_description: '',
                custom_lists: [] // 景点顺序列表
                // 其他订单信息字段
            },
            categoryFilters: [
                { text: '自然风光', value: '1' },
                { text: '历史遗迹', value: '2' },
                { text: '文化遗产', value: '3' },
                { text: '娱乐体验', value: '4' }
            ],
            dialogFormVisible: false,
            attractions: [],
        }
    },
    computed: {
        scenicOptions() {
            return this.$store.state.scenicOptions;
        }
    },
    created() {
        // 在组件创建时获取 scenic options  
        this.$store.dispatch('fetchScenicOptions');
    },
    mounted() {
        this.fetchRouteDetail();
    },
    methods: {
        fetchRouteDetail() {
            axios.get(`http://localhost:8000/route/${this.routeId}/`).then(response => {
                const data = response.data;
                // 填充编辑表单数据
                this.editFormData = {
                    route_name: data.route_name,
                    scenic: data.scenic,
                    route_description: data.route_description,
                    custom_lists: data.custom_lists
                    // 其他订单信息字段
                };
            }).catch(error => {
                console.error('获取编辑数据失败:', error);
            });
        },
        fetchAttractions() {
            axios.get(`http://localhost:8000/api/attractions?scenic=${this.editFormData.scenic}`)
                .then(response => {
                    this.attractions = response.data;
                })
                .catch(error => {
                    console.error('Error fetching attractions:', error);
                });
        },
        setScenicName() {
            // 根据编辑表单的所属景区ID，设置对应的景区名称
            const foundOption = this.scenicOptions.find(option => option.scenic_id === this.editForm.scenic);
            if (foundOption) {
                this.editFormData.scenic = foundOption.scenic_name;
            }
        },
        // 上移景点
        moveUp(index) {
            if (index > 0) {
                const temp = this.editFormData.custom_lists[index];
                this.$set(this.editFormData.custom_lists, index, this.editFormData.custom_lists[index - 1]);
                this.$set(this.editFormData.custom_lists, index - 1, temp);
                // 更新 order 字段
                const currentOrder = this.editFormData.custom_lists[index].order;
                const previousOrder = this.editFormData.custom_lists[index - 1].order;
                this.editFormData.custom_lists[index].order = previousOrder;
                this.editFormData.custom_lists[index - 1].order = currentOrder;
            }
        },
        // 下移景点
        moveDown(index) {
            if (index < this.editFormData.custom_lists.length - 1) {
                const temp = this.editFormData.custom_lists[index];
                this.$set(this.editFormData.custom_lists, index, this.editFormData.custom_lists[index + 1]);
                this.$set(this.editFormData.custom_lists, index + 1, temp);
                // 更新 order 字段
                const currentOrder = this.editFormData.custom_lists[index].order;
                const nextOrder = this.editFormData.custom_lists[index + 1].order;
                this.editFormData.custom_lists[index].order = nextOrder;
                this.editFormData.custom_lists[index + 1].order = currentOrder;
            }
        },
        // 删除景点
        removeAttraction(index) {
            console.log(this.editFormData.custom_lists);
            this.editFormData.custom_lists.splice(index, 1);
            for (let i = index; i < this.editFormData.custom_lists.length; i++) {
                this.editFormData.custom_lists[i].order--;
            }
            console.log(this.editFormData.custom_lists);
        },
        saveEdit() {
            // 构造包含编辑后的新route信息的对象
            const updatedRoute = {
                route_name: this.editFormData.route_name,
                scenic: this.editFormData.scenic,
                route_description: this.editFormData.route_description,
                custom_lists: this.editFormData.custom_lists
                // 其他编辑的路线信息字段
            };
            // 发送HTTP请求
            axios.patch(`http://localhost:8000/route/${this.routeId}/`, updatedRoute)
                .then(response => {
                    // 处理响应
                    console.log('路线编辑保存成功:', response.data);
                    this.$emit('save-edit');
                })
                .catch(error => {
                    // 处理错误
                    console.error('路线编辑保存失败:', error);
                    // 可以在这里触发一些保存失败的提示或者操作
                });
        },
        handleAdd() {
            // 弹出景点选择框，选择景点后执行以下操作
            // 假设selectedAttraction为选中的景点数据
            this.dialogFormVisible = true;
            this.fetchAttractions();
        },
        handleSelectionChange(selection) {
            this.selectedAttractions = selection;
        },
        confirmAdd() {
            // 获取当前选择的景点
            const selectedAttractions = this.$refs.multipleTable.selection;
            // 遍历当前选择的景点
            selectedAttractions.forEach(attraction => {
                // 检查是否已存在于custom_lists中
                const exists = this.editFormData.custom_lists.some(item => item.attraction.attraction_id === attraction.attraction_id);
                // 如果景点已存在，则提示用户不要重复添加
                if (exists) {
                    this.$message.warning(`${attraction.attraction_name} 景点已存在，请勿重复添加`);
                } else {
                    // 否则，将景点添加到custom_lists中
                    this.editFormData.custom_lists.push({
                        attraction: attraction,
                        order: this.editFormData.custom_lists.length + 1 // 设置默认顺序为当前custom_lists长度加1
                    });
                }
            });
            // 关闭弹窗
            this.dialogFormVisible = false;
        },
        getTagType(category) {
            // 根据 scenicName 返回相应的标签类型
            if (category == '1') {
                return 'success';
            } else if (category == '2') {
                return 'danger';
            } else if (category == '4') {
                return 'warning';
            }
            return 'primary';
        },
        setCategory(category) {
            if (category == '1') {
                return '自然风光';
            } else if (category == '3') {
                return '文化遗产';
            } else if (category == '4') {
                return '娱乐体验';
            }
            return '历史遗迹';
        },
        filterTag(value, row) {
            return row.category == value;
        },
    }
}
</script>

<style>
.footer-button-container {  
    display: flex;  
    justify-content: flex-end;  
}
</style>