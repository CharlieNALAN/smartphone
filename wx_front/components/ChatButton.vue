<template>
  <view class="chat-button-container" :style="{ bottom: positionBottom + 'rpx' }">
    <view class="chat-button" @tap="openChat">
      <image class="chat-icon" src="/static/images/chat-icon.png" mode="aspectFit"></image>
    </view>
  </view>
</template>

<script>
export default {
  name: 'ChatButton',
  props: {
    positionBottom: {
      type: Number,
      default: 200
    }
  },
  methods: {
    openChat() {
      uni.navigateTo({
        url: '/pages/chat/chat'
      });
    }
  }
}
</script>

<style lang="scss">
.chat-button-container {
  position: fixed;
  right: 30rpx;
  z-index: 999;
  
  .chat-button {
    width: 100rpx;
    height: 100rpx;
    background-color: #3C88FD;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.2);
    
    .chat-icon {
      width: 60rpx;
      height: 60rpx;
    }
  }
}
</style> 