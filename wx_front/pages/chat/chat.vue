<template>
  <view class="chat-container">
    <NavBar :fixed="true">
      <template slot="left">
        <view class="back-button" @tap="goBack">
          <text class="iconfont icon-back">&#xe60e;</text>
        </view>
      </template>
      <template slot="title">
        <view>AI Assistant</view>
      </template>
    </NavBar>

    <scroll-view
      class="chat-messages"
      scroll-y
      :scroll-top="scrollTop"
      :scroll-with-animation="true"
      @scrolltoupper="loadMoreMessages"
      :upper-threshold="100"
      ref="messageScroll"
    >
      <view class="welcome-message" v-if="messages.length === 0">
        <view class="ai-avatar">
          <image src="/static/AI.png" mode="aspectFill"></image>
        </view>
        <view class="message-content ai-message">
          <text user-select="true">Hello, I am the scenic AI assistant! I can help you plan your visit, check real-time visitor flow, provide attraction information, etc. What can I help you with?</text>
        </view>
      </view>

      <view
        v-for="(message, index) in messages"
        :key="index"
        :class="[
          'message-item',
          message.message_type === 'user'
            ? 'user-message-item'
            : 'ai-message-item',
        ]"
      >
        <view class="message-avatar" v-if="message.message_type === 'ai'">
          <image src="/static/AI.png" mode="aspectFill"></image>
        </view>
        <view
          :class="[
            'message-content',
            message.message_type === 'user' ? 'user-message' : 'ai-message',
          ]"
        >
          <text v-if="message.message_type === 'user'" user-select="true">{{ message.content }}</text>
          <rich-text v-else user-select="true" :nodes="message.content"></rich-text>
        </view>
        <view class="message-avatar" v-if="message.message_type === 'user'">
          <image src="/static/avatar.png" mode="aspectFill"></image>
        </view>
      </view>

      <view class="loading-message" v-if="loading">
        <view class="ai-avatar">
          <image src="/static/images/ai-avatar.png" mode="aspectFill"></image>
        </view>
        <view class="message-content ai-message">
          <view class="dot-loading">
            <view class="dot"></view>
            <view class="dot"></view>
            <view class="dot"></view>
          </view>
        </view>
      </view>

      <!-- 用于自动滚动到底部的标记元素 -->
      <view id="message-bottom"></view>
    </scroll-view>

    <!-- 添加快速问题按钮区域 -->
    <view class="quick-buttons">
      <view 
        v-for="(button, index) in quickButtons" 
        :key="index" 
        class="quick-button"
        @tap="handleQuickButton(button)"
      >
        {{ button.label }}
      </view>
    </view>

    <view class="chat-input-area">
      <textarea
        class="chat-input"
        v-model="inputMessage"
        :style="{ height: textareaHeight + 'px' }"
        placeholder="Please enter your message..."
        :disabled="loading"
        auto-height
        :maxlength="-1"
        :cursor-spacing="20"
        @input="adjustTextareaHeight"
        @confirm="sendMessage"
      />
      <view
        class="send-button"
        :class="{ disabled: loading || !inputMessage.trim() }"
        @tap="sendMessage"
      >
        <!-- <text class="iconfont icon-send">&#xe693;</text> -->
        <image class="chat-icon" src="/static/send.png" mode="aspectFit" style="height: 35px;"></image>
      </view>
    </view>
  </view>
</template>

<script>
import { mapState } from "vuex";
import NavBar from "@/components/NavBar.vue";

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      sessionId: null,
      messages: [],
      inputMessage: "",
      loading: false,
      scrollTop: 0,
      userAvatar: "/static/images/user-avatar.png",
      pageSize: 20,
      hasMoreMessages: true,
      currentUser: null,
      currentScenic: getApp().globalData.global_scenic_id,
      textareaHeight: 35, // 添加初始文本框高度
      
      // 添加快速问题按钮配置
      quickButtons: [
        {
          label: "Route Recommend",
          type: "route",
          prompt: "Please tell me your preferences and visiting time, and I'll recommend a route. You can say something like 'I want a route for history sites with 4 hours to spend'."
        },
        {
          label: "Ticket Info",
          type: "ticket_info",
          prompt: "Which attraction's ticket information would you like to know about?"
        },
        {
          label: "Real-time Info",
          type: "real_time",
          prompt: "Here's the current visitor flow information at this scenic."
        },
        {
          label: "Attraction Info",
          type: "attraction_info",
          prompt: "Which attraction would you like to learn more about?"
        }
      ],
    };
  },
  computed: {
    ...mapState(["user", "currentScenic"]),
  },
  onLoad() {
    this.getUserInfo();
    this.initChatSession();
  },
  methods: {
    getUserInfo() {
      if (this.user && (this.user.id || this.user.user_id)) {
        this.currentUser = this.user;
        return;
      }

      const app = getApp();
      if (app.globalData && app.globalData.userInfo) {
        this.currentUser = app.globalData.userInfo;
        return;
      }

      try {
        const userInfo = uni.getStorageSync("userInfo");
        if (userInfo) {
          this.currentUser =
            typeof userInfo === "string" ? JSON.parse(userInfo) : userInfo;
        }
      } catch (e) {
        console.error("获取本地用户信息失败:", e);
      }
    },
    goBack() {
      uni.navigateBack();
    },
    async initChatSession() {
      const userId = this.currentUser?.id || this.currentUser?.user_id;
      const scenicId = this.currentScenic;
      console.log("scenicId: ", scenicId);
      if (!this.currentUser || !userId) {
        uni.showToast({
          title: "请先登录",
          icon: "none",
        });
        setTimeout(() => {
          uni.navigateTo({
            url: "/pages/user/login",
          });
        }, 1500);
        return;
      }

      try {
        const res = await uni.request({
          url: "http://localhost:8000/api/chat/sessions/",
          method: "POST",
          data: {
            user_id: userId,
            scenic_id: scenicId,
            initial_intent: 'general'  // 默认为一般意图
          },
        });

        if (res.statusCode === 201) {
          this.sessionId = res.data.session_id;
          this.loadMessages();
        } else {
          throw new Error(res.data.error || "创建会话失败");
        }
      } catch (error) {
        console.error("创建会话错误:", error);
        uni.showToast({
          title: "创建会话失败，请重试",
          icon: "none",
        });
      }
    },
    async loadMessages() {
      if (!this.sessionId || !this.hasMoreMessages) return;

      try {
        const res = await uni.request({
          url: `http://localhost:8000/api/chat/sessions/${this.sessionId}/messages/`,
          method: "GET",
        });

        if (res.statusCode === 200) {
          this.messages = res.data;
          this.scrollToBottom();

          if (res.data.length < this.pageSize) {
            this.hasMoreMessages = false;
          }
        } else {
          throw new Error(res.data.error || "加载消息失败");
        }
      } catch (error) {
        console.error("加载消息错误:", error);
        uni.showToast({
          title: "加载消息失败",
          icon: "none",
        });
      }
    },
    loadMoreMessages() {
      if (this.hasMoreMessages) {
        // 实际项目中可以实现分页加载
        // 这里暂时不实现
      }
    },
    async sendMessage() {
      const message = this.inputMessage.trim();
      if (!message || this.loading) return;

      this.inputMessage = "";
      this.loading = true;

      const userMessage = {
        message_id: Date.now(),
        message_type: "user",
        content: message,
        timestamp: new Date().toISOString(),
      };

      this.messages.push(userMessage);
      this.scrollToBottom();

      try {
        const res = await uni.request({
          url: `http://localhost:8000/api/chat/sessions/${this.sessionId}/messages/`,
          method: "POST",
          data: {
            message: message,
          },
        });

        if (res.statusCode === 201) {
          this.messages.push(res.data.ai_message);
          console.log("ai message:", res.data.ai_message.content);
          this.scrollToBottom();
        } else {
          throw new Error(res.data.error || "发送消息失败");
        }
      } catch (error) {
        console.error("发送消息错误:", error);
        uni.showToast({
          title: "发送消息失败，请重试",
          icon: "none",
        });
        this.messages.pop();
      } finally {
        this.loading = false;
      }
    },
    scrollToBottom() {
      setTimeout(() => {
        const query = uni.createSelectorQuery().in(this);
        query
          .select("#message-bottom")
          .boundingClientRect((data) => {
            if (data) {
              this.scrollTop = data.top;
            }
          })
          .exec();
      }, 100);
    },
    // 修改快速按钮处理方法
    async handleQuickButton(button) {
      if (this.loading) return;
      
      this.loading = true;
      console.log("button: ", button.type);
      try {
        // 检查是否已有会话ID
        if (!this.sessionId) {
          // 创建新的会话并指定初始意图
          const userId = this.currentUser?.id || this.currentUser?.user_id;
          const res = await uni.request({
            url: "http://localhost:8000/api/chat/sessions/",
            method: "POST",
            data: {
              user_id: userId,
              scenic_id: this.currentScenic,
              initial_intent: button.type  // 设置初始意图为按钮类型
            },
          });
          
          if (res.statusCode === 201) {
            this.sessionId = res.data.session_id;
          } else {
            throw new Error("创建会话失败");
          }
        }
        
        // 1. 发送用户点击按钮的消息到后端
        const userMessageResponse = await uni.request({
          url: `http://localhost:8000/api/chat/sessions/${this.sessionId}/messages/`,
          method: "POST",
          data: {
            message: button.label,
            intent_type: button.type  // 指定意图类型，这是关键
          },
        });
        
        if (userMessageResponse.statusCode !== 201) {
          throw new Error("发送用户消息失败");
        }
        
        // 更新前端消息显示
        this.messages.push(userMessageResponse.data.user_message);
        this.scrollToBottom();
        
        // 2. 发送AI提示消息到后端
        const aiPromptResponse = await uni.request({
          url: `http://localhost:8000/api/chat/sessions/${this.sessionId}/messages/`,
          method: "POST",
          data: {
            message: button.prompt,
            is_prompt: true,
            intent_type: button.type
          },
        });
        
        if (aiPromptResponse.statusCode === 201) {
          this.messages.push(aiPromptResponse.data.ai_message);
          this.scrollToBottom();
        }
        
        // 3. 如果是实时数据类型，可以直接获取数据
        if (button.type === "real_time") {
          const res = await uni.request({
            url: `http://localhost:8000/api/chat/sessions/${this.sessionId}/messages/`,
            method: "POST",
            data: {
              message: "Show me real-time visitor flow information",
              intent_type: "real_time"
            },
          });
          
          if (res.statusCode === 201) {
            setTimeout(() => {
              this.messages.push(res.data.ai_message);
              this.scrollToBottom();
            }, 800);
          }
        }
      } catch (error) {
        console.error("处理快捷按钮错误:", error);
        uni.showToast({
          title: "操作失败，请重试",
          icon: "none",
        });
      } finally {
        this.loading = false;
      }
    },
    // 添加自适应高度方法
    adjustTextareaHeight(e) {
      // 获取内容行数
      const lineCount = this.inputMessage.split('\n').length;
      // 单行文本的基本高度
      const baseHeight = 35;
      // 每增加一行，增加20px高度，最大高度为115px (约4行)
      this.textareaHeight = Math.min(baseHeight + (lineCount - 1) * 20, 115);
    },
  },
};
</script>

<style lang="scss">
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f7f7f7;

  .back-button {
    color: #ffffff;
    font-size: 40rpx;
  }

  .chat-messages {
    flex: 1;
    padding: 20rpx;
    padding-top: 100rpx;
    overflow-y: auto;

    .welcome-message {
      display: flex;
      margin-bottom: 30rpx;
    }

    .message-item {
      display: flex;
      margin-bottom: 30rpx;
      width: 95%;
    }

    .user-message-item {
      justify-content: flex-end;
    }

    .ai-message-item {
      justify-content: flex-start;
    }

    .message-avatar {
      width: 80rpx;
      height: 80rpx;
      border-radius: 50%;
      overflow: hidden;

      image {
        width: 100%;
        height: 100%;
      }
    }

    .ai-avatar {
      width: 80rpx;
      height: 80rpx;
      border-radius: 50%;
      overflow: hidden;

      image {
        width: 100%;
        height: 100%;
      }
    }

    .message-content {
      max-width: 70%;
      border-radius: 20rpx;
      padding: 20rpx;
      word-break: normal; /* 修改：不允许单词中间断开 */
      overflow-wrap: break-word; /* 添加：允许长单词在必要时换行 */
    //   white-space: pre-wrap; /* 添加：保留空格和换行 */
      margin: 0 20rpx;
    }

    .user-message {
      background-color: #3c88fd;
      color: #ffffff;
      border-top-right-radius: 0;
    }

    .ai-message {
      background-color: #ffffff;
      color: #333333;
      border-top-left-radius: 0;
      
      /deep/ rich-text {
        display: block;
        width: 100%;
      }
    }

    .loading-message {
      display: flex;
      margin-bottom: 30rpx;
    }

    .dot-loading {
      display: flex;
      align-items: center;

      .dot {
        width: 12rpx;
        height: 12rpx;
        background-color: #999;
        border-radius: 50%;
        margin: 0 6rpx;
        animation: dot-animation 1.4s infinite ease-in-out both;

        &:nth-child(1) {
          animation-delay: -0.32s;
        }

        &:nth-child(2) {
          animation-delay: -0.16s;
        }
      }
    }
  }

  .chat-input-area {
    display: flex;
    padding: 20rpx;
    background-color: #ffffff;
    border-top: 1px solid #eeeeee;

    .chat-input {
      flex: 1;
      min-height: 70rpx;
      max-height: 230rpx; /* 允许最大高度约4行 */
      background-color: #f5f5f5;
      border-radius: 35rpx;
      padding: 15rpx 30rpx;
      font-size: 28rpx;
      line-height: 40rpx;
    }

    .send-button {
      width: 45px;
      height: 45px;
      border-radius: 50%;
      background-color: #3c88fd;
      display: flex;
      justify-content: center;
      align-items: center;
      margin-left: 20rpx;
      color: #ffffff;
      font-size: 40rpx;
      align-self: flex-end; /* 确保发送按钮始终在底部对齐 */

      &.disabled {
        background-color: #cccccc;
      }
    }
  }

  // 添加快速问题按钮样式
  .quick-buttons {
    display: flex;
    flex-wrap: wrap;
    padding: 10rpx 20rpx;
    background-color: #ffffff;
    border-top: 1px solid #eeeeee;
    
    .quick-button {
      font-size: 24rpx;
      padding: 10rpx 20rpx;
      margin: 10rpx;
      background-color: #f0f0f0;
      border-radius: 30rpx;
      color: #333333;
      box-shadow: 0 2rpx 4rpx rgba(0, 0, 0, 0.1);
      
      &:active {
        background-color: #e0e0e0;
      }
    }
  }

  /* 添加rich-text全局样式 */
  :deep(rich-text) {
    width: 100%;
  }
  
  /* 确保列表项没有额外的缩进 */
  :deep(ul), :deep(ol) {
    padding-left: 0;
    margin-left: 15rpx;
    list-style-position: inside;
  }
  
  :deep(li) {
    margin-left: 0;
    padding-left: 0;
  }
  
  :deep(p) {
    margin: 0;
    padding: 0;
  }
  
  :deep(h3) {
    margin: 20rpx 0 10rpx 0;
    padding: 0;
  }
}

@keyframes dot-animation {
  0%,
  80%,
  100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}
</style>
