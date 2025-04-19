<template>
	<movable-area class="l-floating-panel-area" :style="areaStyles" :data-init="init">
		<movable-view 
			class="l-floating-panel" 
			direction="vertical" 
			inertia 
			out-of-bounds 
			:damping="80" 
			:friction="100"
			:disabled="isDraggable"
			:y="currentY"
			:animation="isAnimation"
			@change="onTouchmove"
			@touchstart="onTouchstart"
			@touchend="onTouchend"
			@touchcancel="onTouchend"
			:style="styles">
			<view class="l-floating-panel__header" data-handle="true">
				<view class="l-floating-panel__header-bar"></view>
			</view>
			<view class="l-floating-panel__content">
				<slot></slot>
			</view>
		</movable-view>
	</movable-area>
</template>
<script lang="ts">
	// @ts-nocheck
	import { defineComponent, computed, ref , onMounted} from './vue';
	import FloatingPanelProps from './props'
	import {addUnit} from '@/uni_modules/lime-shared/addUnit';
	import {sleep} from '@/uni_modules/lime-shared/sleep';
	import {closest} from '@/uni_modules/lime-shared/closest';
	const name = 'l-floating-panel'
	/**
	 * LimeFloatingPanel 浮动面板
	 * @description 浮动在页面底部的面板，可以上下拖动来浏览内容
	 * @tutorial https://ext.dcloud.net.cn/plugin?id=13407
	 * @property {Number} height 插件返回的高度
	 * @property {Array} anchors 设置自定义锚点 默认值 [100, windowHeight * 0.6]
	 * @property {Number} defaultAnchor 设置开始锚点的下标
	 * @property {Boolean} animation 是否开启动画
	 * @property {Boolean} contentDraggable = true 允许拖拽内容容器 默认 true
	 * @property {Boolean} safeAreaInsetBottom = true 是否开启底部安全区域 默认 true 
	 * @event {Function} heightChange 高度变化时触发  
	 */
	export default defineComponent({
		name,
		props: FloatingPanelProps,
		emits: ['heightChange', 'update:height'],
		setup(props, {emit, expose}) {
			const {windowHeight, safeAreaInsets } = uni.getSystemInfoSync()
			const isDraggable = ref(!props.contentDraggable)
			const isAnimation = ref(false)
			const dragging = ref(false)
			
			const init = ref(false)
			
			const boundary = computed(() => {
				const anchors = props.anchors as number[]||[];
				return {
					min: anchors[0] ?? 100,
					max:
						anchors[anchors.length - 1] ??
						Math.round(windowHeight * 0.6),
				}
			});
			const calcY = (y: number) => boundary.value.max - y
			const anchors = computed(() => {
				const anchors = props.anchors as number[]||[];
				return anchors.length >= 2
			        ? anchors
			        : [boundary.value.min, boundary.value.max]
			})
			const areaStyles = computed(() => {
				return ({
					height: addUnit(boundary.value.max * 2 - boundary.value.min),
					bottom: addUnit(boundary.value.max * -1 + boundary.value.min +(props.safeAreaInsetBottom ? safeAreaInsets.bottom:0)),
					opacity: init.value ? 1 : 0
				}) 
			})
			const styles = computed(() => {
				return ({
					height: addUnit(boundary.value.max) 
				})
			})
			
			const currentY = ref( props.defaultAnchor && calcY(props.anchors[props.defaultAnchor]) || calcY(boundary.value.min))
			let moveYs = []
			let startY = 0
			const onTouchstart = (e:  WechatMiniprogram.TouchEvent) => {
				startY = e.touches[0].clientY
				dragging.value = true
				moveYs.length = 0
				const { handle } = e.target.dataset
				if(!props.contentDraggable && Boolean(handle)) {
					isDraggable.value = false
					return
				}
				
			}
			const onTouchmove = (e: WechatMiniprogram.MovableViewChange) => {
				const {y}  = e.detail
				if(dragging.value) {
					moveYs.push(y)
				}
				const height = calcY(y) 
				emit('update:height',height)
			}
			
			const setCurrentY = (target: number) => {
				currentY.value = target + 0.1;
				// h5要延迟才能触发
				sleep(50).then(() => {
					currentY.value = target
					emit('heightChange', { height: calcY(target)});
				})
			}
			const toAnchor = (index: number) => {
				if(index >= 0 && index < anchors.value.length) {
					setCurrentY(calcY(anchors.value[index]))
				}
			}
			const reDraggable = () => {
				if(!props.contentDraggable) {
					sleep(50).then(() => isDraggable.value = true)
				}
			}
			const onTouchend = (e: WechatMiniprogram.TouchEvent) => {
				let moveY = 0
				dragging.value = false
				const { handle } = e.target.dataset
				const isClick = Math.abs(e.changedTouches[0].clientY - startY) < 10
				if(isClick && !Boolean(handle)) {
					reDraggable()
					return
				}
				if(isClick) {
					const index = anchors.value.findIndex(item => item == calcY(currentY.value)) + 1
					// setCurrentY(calcY(anchors.value[index % anchors.value.length]))
					toAnchor(index % anchors.value.length)
					reDraggable()
					return
				} else if(moveYs.length) {
					moveY = moveYs[moveYs.length-1]
				}
				moveYs.length = 0
				reDraggable()
				setCurrentY(calcY(closest(anchors.value, calcY(moveY))))
			}
			
			onMounted(() => {
				isAnimation.value = props.animation
				sleep(50).then(() => init.value = true)
			})
			// #ifdef VUE3
			expose({
				toAnchor
			})
			// #endif
			
			return {
				init,
				areaStyles,
				styles,
				isDraggable,
				isAnimation,
				currentY,
				onTouchstart,
				onTouchmove,
				onTouchend,
				// #ifndef VUE3
				toAnchor
				// #endif
			}
		}
	})
</script>
<style lang="scss">
	@import './index.scss';
</style>
