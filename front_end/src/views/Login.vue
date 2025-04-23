<template>
    <div class="login-page">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span class="login-title">🔐景区管理系统后台</span>
        </div>
        <div class="login-form">
          <el-form :model="form" :rules="loginRules" ref="loginForm">
            <el-form-item prop="userName">
              <el-input type="text" v-model="form.userName" auto-complete="off" placeholder="请输入用户名">
                <template slot="prepend"><i style="font-size:20px" class="el-icon-user"></i></template>
              </el-input>
            </el-form-item>
            <el-form-item prop="passWord">
              <el-input type="password" v-model="form.passWord" auto-complete="off" placeholder="请输入密码">
                <template slot="prepend"><i style="font-size:20px" class="el-icon-key"></i></template>
              </el-input>
            </el-form-item>
  
            <!-- <el-form-item prop="vertify_code">
              <el-input v-model="form.vertify_code" placeholder="验证码" prefix-icon="el-icon-key">
                <template slot="append">
                  <div class="login-code" @click="refreshCode" title="看不清？点击切换">
                    <verifyCode :identifyCode="identifyCode"></verifyCode>
                  </div>
                </template>
              </el-input>
            </el-form-item> -->
  
            <el-form-item>
              <el-button style="width:100%;" type="primary" @click="handleLogin" :loading="loading">登录</el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>
    </div>
  </template>
  
  <script>
  
//   import verifyCode from './components/VerifyCode'
  
  export default {
    name: 'Login',
    components:{
    //   verifyCode
    },
    data(){
      return {
        // 验证码组件
        // identifyCodes: 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz0123456789',
        // identifyCode: '',
  
        loading: false,
        form:{
          userName: '',
          passWord: ''
        },
        loginRules:{
          userName: [
            { required: true, message: '请输入账户', trigger: 'blur' },
          ],
          passWord: [
            { required: true, message: '请输入密码', trigger: 'blur'}
          ]
        }
      }
    },
    created () {
      this.refreshCode()
    },
    methods:{
      handleLogin(){
        this.$router.push('/home');
      },
    //   // 验证码
    //   randomNum (min, max) {
    //     return Math.floor(Math.random() * (max - min) + min)
    //   },
    //   // 生成随机验证码
    //   makeCode (o, l) {
    //     for (let i = 0; i < l; i++) {
    //       this.identifyCode += this.identifyCodes[
    //         this.randomNum(0, this.identifyCodes.length)
    //         ]
    //     }
    //     // console.log('identifyCode: ' + this.identifyCode)
    //   },
    //   // 验证码刷新
    //   refreshCode () {
    //     this.identifyCode = ''
    //     this.makeCode(this.identifyCodes, 4)
    //   },
    //   // 验证码输入校验
    //   validateCode (rule, value, callback) {
    //     if (value !== this.identifyCode) {
    //       callback(new Error('验证码验证错误！请输入正确的验证码！'))
    //     } else {
    //       callback()
    //     }
    //   }
      // handleLogin(){
      //   this.$refs.loginForm.validate().then(()=>{
      //     this.loading = true;
      //
      //     //模拟异步请求后台接口 登录操作
      //     setTimeout(()=>{
      //       this.$router.push('/home');
      //       this.loading = false;
      //     }, 1000)
      //   }).catch((error=>{
      //     this.$message({
      //       message: '输入错误！',
      //       type: 'warning'
      //     });
      //   }))
      // }
    }
  }
  </script>
  
  <style scoped>
  .login-page{
    margin-top: -60px;
    margin-left: -10px;
    background-image: linear-gradient(180deg, #090948 0%, #f5f5f5 100%);
    height: 800px;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .login-title{
    font-size: 20px;
  }
  
  .box-card {
    width: 375px;
  }
  
  </style>
  
  