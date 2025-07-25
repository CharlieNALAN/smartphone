# 按钮组 wo-btn-group

> 采用uniapp-vue3实现, 是一款支持高度自定义的按钮组组件，支持H5、微信小程序（其他小程序未测试过，可自行尝试）

## props属性

### shape

> 按钮组形状：椭圆(默认)、方形、圆形

~~~js
shape: {
    type: 'round' | 'space' | 'default',
    default: 'default',
},
~~~

### outline

> 轮廓显示

~~~js
outline: {
    type: Boolean,
    default: false
},
~~~

### color

> 按钮组色调

~~~js
color: {
    type: String,
    default: '#3370FF'
}
~~~

### defaultValue

> 初始默认选中值

~~~js
defaultValue: {
    type: string | number,
    default: 1
}
~~~

### options

> 按钮数据

~~~js
options: {
    type: any[],
    default: () => [
        {
            label: '按钮1',
            value: 1,
        },
        {
            label: '按钮2',
            value: 2,
            disabled: true
        },
        {
            label: '按钮3',
            value: 3,
        },
        {
            label: '按钮4',
            value: 4,
        }
    ]
}
~~~

### borderObj

> 自定义边框，包括：是否显示边框、边框粗细、边框风格、按钮组圆角幅度

~~~js
borderObj: {
    type: Object,
    default: () => {
        return {
            isShow: true,
            size: '1rpx',
            style: 'solid',
            radius: '70rpx'
        }
    }
},
~~~

## 事件

### @change

> 点击选项时触发，返回包含了选项数据的对象

