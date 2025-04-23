<template>
    <el-container>
      <el-header style="background-color: #82adfc">
        <span id="title">SmartTravel</span>
        <!-- <div id="out">
          <el-avatar icon="el-icon-user-solid" ></el-avatar>
          <div id="logout" @click="logout">
            退出
          </div>
        </div> -->
      </el-header>
      <el-container>
            <el-aside width="auto">
                <CommonAside/>
            </el-aside>
            <el-main>
                <router-view></router-view>
            </el-main>
      </el-container>
    </el-container>
</template>

<script>
import CommonAside from '../components/CommonAside'

export default {
    name: 'Index',
    components: {
        CommonAside
    },
    data() {
        return {}
    },
    methods: {

    },
}
</script>

<style>
.el-header{
    padding:0;
    margin-top: -60px;
}
.el-main{
    float: left;
}
.el-group-radio{
    clear: left;
}
#title{
  font-size: 40px;
  margin-left: 40px;
  /*top: 50px;*/
  /*float: left;*/
  color: white;
  display: block;
  width: 100%;
  /*padding-top: 10px;*/
}
</style>