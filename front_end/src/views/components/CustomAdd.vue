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
        </el-form>
        <el-table :data="form.custom_lists" style="width: 100%" ref="table">
            <el-table-column prop="order" label="顺序"></el-table-column>
            <el-table-column prop="attraction.attraction_name" label="景点名称"></el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button @click="handleDelete(scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-button style="margin-top: 10px" @click="handleAdd">新增景点</el-button>
        <el-button style="margin-top: 10px" @click="handleSafe" :disabled="isSaveDisabled">保存</el-button>
        <el-dialog title="新增景点" :visible.sync="dialogFormVisible">
            <el-table ref="multipleTable" :data="filteredAttractions" row-key="attraction_id"
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
    data() {
        return {
            form: {
                strategy_name: '',
                scenic: '',
                custom_lists: []
            },
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
        isSaveDisabled() {
            // 当 custom_lists 数组为空时禁用保存按钮，否则启用  
            return this.form.custom_lists.length === 0;
        }
    },
    mounted() {
        this.fetchAllAttractions();
        this.$nextTick(() => {
            this.initializeSortable();
        });
    },
    created() {
        this.$store.dispatch('fetchScenicOptions');
    },
    methods: {
        generateCategoryFilters() {
            // 生成筛选标签数组  
            // 假设你有一个包含所有可能的category值的数组categories  
            const categories = ['1', '2', '3', '4']; // 假设的categories数组  
            return categories.map(category => ({
                text: this.setCategory(category), // 筛选标签的文本  
                value: category // 筛选标签对应的category值  
            }));
        },
        fetchAllAttractions() {
            axios.get('http://localhost:8000/api/attractions/')
                .then(response => {
                    this.allAttractions = response.data;
                    console.log('All Attractions:', this.allAttractions);
                })
                .catch(error => {
                    console.error('Error fetching all attractions:', error);
                });
        },
        handleAdd() {
            // 弹出景点选择框，选择景点后执行以下操作
            // 假设selectedAttraction为选中的景点数据
            this.dialogFormVisible = true
        },
        handleDelete(row) {
            const index = this.form.custom_lists.findIndex(item => item.id === row.id);
            this.form.custom_lists.splice(index, 1);
            this.updateOrders();
        },
        updateOrders() {
            this.form.custom_lists.forEach((item, index) => {
                item.order = index + 1;
            });
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
        // 处理多选时的选择事件
        handleSelectionChange(selection) {
            this.selectedAttractions = selection;
        },
        // 操作确认后触发，传入已选择的景点数组
        confirmAdd() {
            this.dialogFormVisible = false;
            // 遍历已选择的景点数组，依次添加到推荐列表中
            this.selectedAttractions.forEach(selectedAttraction => {
                this.form.custom_lists.push({
                    attraction: selectedAttraction,
                    order: this.form.custom_lists.length + 1
                });
            });
        },
        // async handleSafe() {
        //     try {
        //         const response = await axios.post('http://localhost:8000/recommendation-strategies/', this.form);
        //         console.log('Saved data:', response.data);
        //         // 保存成功后的操作，比如重置表单
        //         this.form = {
        //             strategy_name: '',
        //             scenic: '',
        //             custom_lists: []
        //         };
        //     } catch (error) {
        //         console.error('Failed to save data:', error);
        //     }

        // }
    },
    watch: {
        'form.scenic': {
            handler(newVal, oldVal) {
                this.filteredAttractions = this.allAttractions.filter(attraction => attraction.scenic_id === this.form.scenic);
            },
            deep: true, // 深度监听，因为form.scenic可能是一个对象或数组
        },
    },
    beforeDestroy() {
        if (this.sortableInstance) {
            this.sortableInstance.destroy();
        }
    }
}
</script>

  