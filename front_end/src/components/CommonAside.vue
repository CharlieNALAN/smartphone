<template>
    <el-container style="width: auto; height: 800px; border: 1px solid #eee">
        <el-aside width="200px" style="background-color: rgb(255, 255, 255)">
            <el-menu router="true" :default-active="activeIndex">
                <!-- <el-button class="homepage" type="primary" round>首页</el-button> -->
                <el-menu-item index="/home">
                    <i class="el-icon-time"></i>
                    <span>景区实时情况</span>
                </el-menu-item>
                <el-menu-item index="/attractions">
                    <i class="el-icon-menu"></i>
                    <span>景点信息管理</span>
                </el-menu-item>
                <el-menu-item index="/history">
                    <i class="el-icon-data-board"></i>
                    <span>景区历史数据中心</span>
                </el-menu-item>
                <el-menu-item index="/strategy">
                    <i class="el-icon-setting"></i>
                    <span>推荐信息管理</span>
                </el-menu-item>
                <el-menu-item index="/post">
                    <i class="el-icon-message"></i>
                    <span>景区公告</span>
                </el-menu-item>
            </el-menu>
        </el-aside>
    </el-container>
</template>
  
<script>
/* eslint-disable vue/no-deprecated-slot-attribute */
export default {
    name: "CommonAside",
    data() {
        return {
            activeIndex: '/home',
        }
    },
    mounted() {
        this.activeIndex = this.$route.path;
    },
    methods: {
        handleSelect(key, keyPath) {
            console.log(key, keyPath);
        },
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.el-header {
    background-color: #ddfa98;
    color: #333;
    line-height: 60px;
}

.el-aside {
    color: #333;
}

.el-button {
    width: 100px;
    position: center;
}
</style>
  