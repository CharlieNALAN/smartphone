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
        { msg: 'Attraction Prince Bay Park has exceeded the warning value, please configure strategy!' },
        { msg: 'Attraction Lingyin Temple has exceeded the warning value, please configure strategy!' },
        { msg: 'Attraction First Gorge has exceeded the warning value, please configure strategy!' },
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

