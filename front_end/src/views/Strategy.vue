<template>
    <div>
        <el-dropdown @command="handleCommand">
            <span class="el-dropdown-link">
                <el-button type="primary" size="medium" plain class="el-dropdown-link">
                    新建策略<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
            </span>
            <el-dropdown-menu slot="dropdown" class="drop">
                <el-dropdown-item command="a">单一策略-基础选项</el-dropdown-item>
                <el-dropdown-item command="b">单一策略-自定义推荐列表</el-dropdown-item>
                <el-dropdown-item command="c">组合策略</el-dropdown-item>
            </el-dropdown-menu>
        </el-dropdown>
        <el-dialog title="单策略-基础推荐策略" :visible.sync="a_dialogVisible" width="60%" :before-close="handleClose">
            <BaseAdd @close-dialog="closeDialog"></BaseAdd>
        </el-dialog>
        <el-dialog title="单策略-自定义推荐列表" :visible.sync="b_dialogVisible" width="60%" :before-close="handleClose">
            <CustomAdd></CustomAdd>
        </el-dialog>
        <el-dialog title="组合策略" :visible.sync="c_dialogVisible" width="80%" :before-close="handleClose">
            <CombinedAdd></CombinedAdd>
            <span slot="footer" class="dialog-footer">
                <el-button @click="c_dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="handleCombinedSave">保 存</el-button>
            </span>
        </el-dialog>
        <el-table :data="strategies" style="width: 100%">
            <el-table-column prop="id" label="策略编号" width="150" />
            <el-table-column prop="strategy_name" label="策略名称" width="250" />
            <el-table-column prop="strategy_type" label="策略类型" width="200">
                <template slot-scope="scope">
                    <span v-if="scope.row.strategy_type == 1">按实时人数推荐</span>
                    <span v-if="scope.row.strategy_type == 2">按景点热度推荐</span>
                    <span v-if="scope.row.strategy_type == 3">自定义推荐列表</span>
                    <span v-if="scope.row.strategy_type == 4">组合策略</span>
                    <span v-if="scope.row.strategy_type == 5">个性化推荐</span>
                </template>
            </el-table-column>
            <el-table-column prop="scenic" label="所属景区" :filters="scenicFilters" :filter-method="filterTag"
                filter-placement="bottom-end" width="180">
                <template slot-scope="scope">
                    <el-tag :type="getTagType(scope.row.scenic)" disable-transitions>
                        {{ setTagName(scope.row.scenic) }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="策略状态" width="150">
                <template slot-scope="scope">
                    <el-tag type="success" effect="dark" v-if="scope.row.status == 1">已启用</el-tag>
                    <el-tag type="warning" effect="dark" v-if="scope.row.status == 0">未启用</el-tag>
                </template>
            </el-table-column>
            <el-table-column fixed="right" width="250" label="操作">
                <template slot-scope="scope">
                    <el-button size="mini" type="success" plain @click="able(scope.$index, scope.row)">启用</el-button>
                    <el-button size="mini" type="danger" plain @click="disable(scope.$index, scope.row)">禁用</el-button>
                    <el-button size="mini" type="primary" plain @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-button type="primary" @click="d_dialogVisible = true" class="add-route">新增游览路线</el-button>
        <el-table :data="routes" style="width: 100%">
            <el-table-column prop="id" label="路线编号" width="150" />
            <el-table-column prop="route_name" label="路线名称" width="250" />
            <el-table-column prop="scenic" label="所属景区" :filters="scenicFilters" :filter-method="filterTag"
                filter-placement="bottom-end" width="200">
                <template slot-scope="scope">
                    <el-tag :type="getTagType(scope.row.scenic)" disable-transitions>
                        {{ setTagName(scope.row.scenic) }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="策略状态" width="150">
                <template slot-scope="scope">
                    <el-tag type="success" effect="dark" v-if="scope.row.status == 1">已启用</el-tag>
                    <el-tag type="warning" effect="dark" v-if="scope.row.status == 0">未启用</el-tag>
                </template>
            </el-table-column>
            <el-table-column fixed="right" width="320" label="操作">
                <template slot-scope="scope">
                    <el-button size="mini" type="success" plain @click="able(scope.$index, scope.row)">启用</el-button>
                    <el-button size="mini" type="danger" plain @click="disable(scope.$index, scope.row)">禁用</el-button>
                    <el-button size="mini" type="primary" plain @click="RouteEdit(scope.row)">编辑</el-button>
                    <el-button size="mini" plain @click="delete (scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-dialog title="新增游览路线" :visible.sync="d_dialogVisible" width="60%" :before-close="handleClose">
            <RouteAdd></RouteAdd>
        </el-dialog>
        <el-dialog :visible.sync="e_dialogVisible" title="编辑" width="60%" :before-close="handleClose">
            <RouteEdit :routeId="currentRouteId" @save-edit="handleSaveEdit"></RouteEdit>
        </el-dialog>
    </div>
</template>

<script>
import axios from 'axios';
import CustomAdd from "./components/CustomAdd.vue";
import CombinedAdd from "./components/CombinedAdd.vue";
import BaseAdd from './components/BaseAdd.vue';
import RouteAdd from "./components/route/RouteAdd.vue";
import RouteEdit from "./components/route/RouteEdit.vue";
import scenicFilterMixin from '../mixin/scenicFilterMixin.js';
export default {
    components: {
        CustomAdd,
        CombinedAdd,
        BaseAdd,
        RouteAdd,
        RouteEdit,
    },
    mixins: [scenicFilterMixin],
    data() {
        return {
            a_dialogVisible: false,
            b_dialogVisible: false,
            c_dialogVisible: false,
            d_dialogVisible: false,
            e_dialogVisible: false,
            strategies: [],
            routes: [],
            currentRouteId: null
        }
    },
    mounted() {
        this.fetchStrategy();
        this.fetchRoute();
    },
    methods: {
        fetchStrategy() {
            axios.get('http://localhost:8000/recommendation-strategies/')
                .then(response => {
                    this.strategies = response.data;
                })
                .catch(error => {
                    console.error('Error fetching all strategies:', error);
                });
        },
        fetchRoute() {
            axios.get('http://localhost:8000/route/')
                .then(response => {
                    this.routes = response.data;
                })
                .catch(error => {
                    console.error('Error fetching all routes:', error);
                });
        },
        handleCommand(command) {
            switch (command) {
                case 'a': {
                    this.a_dialogVisible = true;
                    break;
                }
                case 'b': {
                    this.b_dialogVisible = true;
                    break;
                }
                case 'c': {
                    this.c_dialogVisible = true;
                    break;
                }
            }
        },
        handleClose(done) {
            this.$confirm('确认关闭？')
                .then(_ => {
                    done();
                })
                .catch(_ => { });
        },
        able(index, row) {
            if (row.status == 0) {
                axios.patch(`http://localhost:8000/recommendation-strategies/${row.id}/`, { status: 1 })
                    .then(response => {
                        if (response.status === 200) {
                            row.status = 1;
                            this.$message.info("启用成功");
                        } else {
                            this.$message.error("启用失败，请重试");
                        }
                    })
                    .catch(error => {
                        console.error(error);
                        this.$message.error("启用失败，请重试");
                    });
                row.status = 1;

            } else {
                this.$message.info("该策略启用中")
            }
        },
        disable(index, row) {
            if (row.status == 1) {
                axios.patch(`http://localhost:8000/recommendation-strategies/${row.id}/`, {
                    status: 0
                })
                    .then(response => {
                        if (response.status === 200) {
                            row.status = 0;
                            this.$message.info("禁用成功");
                        } else {
                            this.$message.error("禁用失败，请重试");
                        }
                    })
                    .catch(error => {
                        console.error(error);
                        this.$message.error("禁用失败，请重试");
                    });
            } else {
                this.$message.info("该策略已禁用");
            }
        },
        handleCombinedSave() {
            this.c_dialogVisible = false;
        },
        RouteEdit(row) {
            this.e_dialogVisible = true;
            this.currentRouteId = row.id; // 将当前路线的ID保存
        },
        handleSaveEdit() {
            // 关闭弹窗
            this.fetchRoute();
            this.e_dialogVisible = false;

        },
        closeDialog() {
            // 关闭对话框
            this.fetchStrategy();
            this.a_dialogVisible = false;
        }
    },
}
</script>

<style>
.add-route {
    margin-top: 20px;
}
</style>