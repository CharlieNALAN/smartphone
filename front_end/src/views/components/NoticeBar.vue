<template>
  <div id="demo">
    <ul class="list">
      <li
        v-for="(item, index) in ulList"
        :key="item.id"
        :class="!index && play ? 'toUp' : ''"
      >
<!--        <i class="el-icon-warning"></i>-->
        <el-alert
          type="error"
          show-icon>
          {{ item.msg }}
        </el-alert>

      </li>
    </ul>
  </div>
</template>

<script>
export default {
  mounted() {
    setInterval(this.startPlay, 2000)
  },
  data() {
    return {
      ulList: [
        { msg: '景点 太子湾公园 流量已超过警戒值，请配置策略！' },
        { msg: '景点 灵隐寺 流量已超过警戒值，请配置策略！' },
        { msg: '景点 一线天 流量已超过警戒值，请配置策略！' },
      ],
      play: false
    }
  },
  methods: {
    startPlay() {
      let that = this
      that.play = true //开始播放
      setTimeout(() => {
        that.ulList.push(that.ulList[0]) //将第一条数据塞到最后一个
        that.ulList.shift() //删除第一条数据
        that.play = false //暂停播放
      }, 500)
    }
  }
}
</script>

<style scoped>
.toUp {
  margin-top: -40px;
  transition: all 0.5s;
}

.list {
  list-style: none;
  width: 560px;
  text-align: center;
  overflow: hidden;
  height: 45px;
  padding: 0;
  margin: 0;
}
li {
  /*text-align: left;*/
  /*height: 40px;*/
  /*line-height: 40px;*/
  /*background-color: white;*/
  /*padding-left: 20px;*/
  /*opacity: 0.6;*/
  /*color: #F56C6C ;*/
}
</style>

