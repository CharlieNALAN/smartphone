# wo-gradient-card
> 采用uniapp-vue3实现，透明辉光移动动画卡片，卡片内容包含标签、标题、副标题、图片
>
> 支持H5、微信小程序（其他小程序未测试过，可自行尝试）
>
> 可用于参考学习

## props属性

### options

> 范围数据

~~~js
interface OptionsItem {
	tag: string;
	tagStyle: {
		bgColor: string,
		color: string
	};
	title: string;
	subtitle: string;
	img: string;
	bgColor: string
} 
options: {
	type: OptionsItem[],
	default: () => []
}
~~~

