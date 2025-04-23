import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter)
// 防止跳转同一路径出异常
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location, onResolve, onReject) {
  if (onResolve || onReject) return originalPush.call(this, location, onResolve, onReject)
  return originalPush.call(this, location).catch(err => err)
}

export default new VueRouter({
    routes: [
        {
            path:'/',
            name:'Login',
            component:()=>import('../views/Login.vue'),
        },
        {
            path: '/index',
            name: ' Index',
            component: ()=>import('../views/Index.vue'),
            children: [
                //景区实时情况
                {
                    path:'/home',
                    name:'Home',
                    component:()=>import('../views/Home.vue'),
                },
                //景点信息管理
                {
                    path: '/attractions',
                    name: 'Attractions',
                    component: ()=>import('../views/Attractions.vue')
                },
                {
                    path: '/attractions/add',
                    name: 'AttractionAdd',
                    component: ()=>import('../views/AttractionAdd.vue')
                },
                //景区历史数据中心
                {
                    path: '/history',
                    name: 'History',
                    component: ()=>import('../views/History.vue')
                },
                //推荐策略配置
                {
                    path: '/strategy',
                    name: 'Strategy',
                    component: ()=>import('../views/Strategy.vue')
                },
                {
                    path: '/post',
                    name: 'Post',
                    component: ()=>import('../views/Post.vue')
                },
            ]
        },
    ]
})