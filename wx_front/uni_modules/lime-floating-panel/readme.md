# lime-floating-panel 浮动面板
- 浮动在页面底部的面板，可以上下拖动来浏览内容，常用于提供额外的功能或信息。

## 代码演示

### 基础用法

FloatingPanel 的默认高度为 `100px`，用户可以拖动来展开面板，使高度达到 `60%` 的屏幕高度。

```html
<l-floating-panel>
  <view>内容</view>
</l-floating-panel>
```

### 自定义锚点

你可以通过 `anchors` 属性来设置 FloatingPanel 的锚点位置，并通过 `v-model:height` 来控制当前面板的显示高度

比如，使面板的高度在 `100px`、40% 屏幕高度和 70% 屏幕高度三个位置停靠：

```html
// vue3 v-model:height
// vue2 :height.sync
<l-floating-panel v-model:height="height" :anchors="anchors">
  <view style="text-align: center; padding: 15px">
    <p>面板显示高度 {{ height.toFixed(0) }} px</p>
  </view>
</l-floating-panel>
```

```js
import { ref } from 'vue';

export default {
  setup() {
	const {windowHeight} = uni.getSystemInfoSync()
	const anchors = [
	        100,
	        Math.round(0.4 * windowHeight),
	        Math.round(0.7 * windowHeight),
	];
    const height = ref(anchors[0]);

    return { anchors, height };
  },
};
```

### 仅头部拖拽

默认情况下，FloatingPanel 的头部区域和内容区域都可以被拖拽，你可以通过 `content-draggable` 属性来禁用内容区域的拖拽。

```html
<l-floating-panel :content-draggable="false">
  <view style="text-align: center; padding: 15px">
    <text>内容不可拖拽</text>
  </view>
</l-floating-panel>
```

### 设置初始锚点位

默认情况下，FloatingPanel 的初始锚点位为0，可以通过设置 `defaultAnchor` 改变初始锚点位。

```html
<l-floating-panel :defaultAnchor="1">
  <view style="text-align: center; padding: 15px">
    <text>内容</text>
  </view>
</l-floating-panel>
```


### 跳到指定锚点位

FloatingPanel 暴露 `toAnchor` 方法，可以跳到指点的锚点位。

```html
<l-floating-panel ref="floatingPanelRef>
  <view style="text-align: center; padding: 15px">
    <text>内容</text>
  </view>
</l-floating-panel>
<button @click="to">跳到1</button>
```
```js
 const floatingPanelRef = ref(null)

 const to = () => floatingPanelRef.value.toAnchor(1)
```

### 查看示例
- 导入后直接使用这个标签查看演示效果

```html
<!-- // 代码位于 uni_modules/lime-floating-panel/compoents/lime-floating-panel -->
<lime-floating-panel />
```


### 插件标签
- 默认 l-floating-panel 为 component
- 默认 lime-floating-panel 为 demo

### 关于vue2的使用方式
- 插件使用了`composition-api`, 如果你希望在vue2中使用请按官方的教程[vue-composition-api](https://uniapp.dcloud.net.cn/tutorial/vue-composition-api.html)配置
- 关键代码是: 在main.js中 在vue2部分加上这一段即可.
```js
// vue2
import Vue from 'vue'
import VueCompositionAPI from '@vue/composition-api'
Vue.use(VueCompositionAPI)
```


## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| v-model:height | 当前面板的显示高度 | _number \| string_ | `0` |
| anchors | 设置自定义锚点, 单位 `px` | _number[]_ | `[100, windowHeight * 0.6]` |
| animation | 是否开启动画 |  _boolean_ | `true` |
| content-draggable | 允许拖拽内容容器 | _boolean_ | `true` |
| safe-area-inset-bottom | 是否开启底部安全区域 | _boolean_ | `true` |
| defaultAnchor | 默认的锚点下标，如果指定了就在会`anchors`里找到相应的高度 | _number_ | `0` |

### Events

| 事件名        | 说明                             | 回调参数             |
| ------------- | -------------------------------- | -------------------- |
| height-change | 面板显示高度改变且结束拖动后触发 | _{ height: number }_ |

### Slots

| Name    | Description    |
| ------- | -------------- |
| default | 自定义面板内容 |


## 主题定制

### 样式变量
- nvue 不支持
组件提供了下列 CSS 变量，可用于自定义样式。

| Name                               | Default Value             | Description |
| ---------------------------------- | ------------------------- | ----------- |
| --l-floating-panel-border-radius | _16px_                    | -           |
| --l-floating-panel-header-height | _30px_                    | -           |
| --l-floating-panel-z-index       | _999_                     | -           |
| --l-floating-panel-background    | _white_ | -           |
| --l-floating-panel-bar-width     | _20px_                    | -           |
| --l-floating-panel-bar-height    | _3px_                     | -           |
| --l-floating-panel-bar-color     | _#ddd_       | -           |
