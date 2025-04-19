# csr-tab
具体用法请下载示例查看
# 属性
|属性名			|类型	|默认值	|说明									|
|:-:			|:-:	|:-:	|:-:									|
|value			|Number	|0		|默认下标(双向绑定)						|
|tabList		|Array	|[]		|可以是一维数组或是数组对象				|
|bgColor		|String	|#FFFFFF|背景颜色								|
|defaultColor	|String	|#000000|默认未选中文字颜色						|
|activeColor	|String	|#1e9fff|选中时文字颜色 线条颜色				|
|scroll			|Boolean|false	|横向滑动								|
|rangeKey		|String	|''		|当tabList为数组对象时指定显示对象key	|

# 事件
|事件名	|说明						|
|:-:	|:-:						|
|change	|点击事件时触发,返回对应数据|