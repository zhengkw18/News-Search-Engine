<template>
  <el-dialog
    style="text-align: center;"
    :visible.sync="dialogVisible"
    :close-on-click-modal=false
    width="3.5rem"
    id="login-dialog"
    @close="close">
    <div class="header">
      <div>
        <img v-lazy="logo_src" alt="" class="login-img">
        <span class="header-title">欢迎登录</span>
      </div>
      <p class="header-error">{{error_info }}</p>
    </div>
    
    <el-form>
      <el-form-item>
        <el-input type="text" placeholder="请输入用户名" v-model="state.username"></el-input>
      </el-form-item>
      <el-form-item>
        <el-input type="password" placeholder="请输入密码" v-model="state.password"></el-input>
      </el-form-item>
    </el-form>

    <el-button type="primary"
      v-on:click="login">登录</el-button>
    <div class="footer-register">
      <router-link target="_blank" to="/register">没有账号？马上注册</router-link>
    </div>
  </el-dialog>
</template>

<script>
import communication from "@/utils/communication"
import cookie from "@/utils/cookie"
export default {
  name: "LoginDialog",
  props: {
    dialogVisible: {
      type: Boolean,
      default: () => true
    },
    state: {
      type: Object,
      default: () => {
          return {
          username: "",
          password:""
        }
      }
    }
  },
  // 请在下方设计自己的数据结构以及事件函数
  data(){
    return {
      error_info:"",
      logo_src: require('../assets/logo.jpg')
    }
  },
  methods: {
    login(){
      communication.send_login({
          "username":this.state.username,
          "password":this.state.password
      }, this.callback)
    },
    close(){
      this.$emit('hide')
    },
    callback(success, error_info){
      if (success){
        this.error_info=""
        cookie.add_cookie("username", this.state.username, 24)
        cookie.add_cookie("password", this.state.password, 24)
        this.$emit('success')
      }
      else{
        this.error_info = error_info
      }
    }
  }
}
</script>

<style scoped>
  #login-dialog{
    font-size: 16px; 
  }
  #login-dialog .header{
    margin-top: -3vh;
    margin-bottom: 0.4rem;
    position: relative;
  }
  #login-dialog .login-img{
    height: 0.35rem;
    vertical-align: middle;
  }
  #login-dialog .header-title{
    font-size: 0.22rem; 
    margin-left: 0.1rem;
  }
  #login-dialog .header-error{
    color: red;
    font-size: 14px;
    position: absolute;
    bottom: -140%;
  }

  #login-dialog >>> .el-form-item__label, #login-dialog >>> .el-input{
    font-size: 14px !important;
  }
  /*
  #login-dialog >>> .el-input__inner{
    height: 0.4rem !important;
  }*/

  #login-dialog .el-button{
    font-size: 16px;
    padding-top: 10px;
    padding-bottom: 10px;
    width: 100%;
  }
  #login-dialog .footer-register{
    margin-top: 0.2rem; 
    font-size: 16px;
    margin-bottom: 2vh;
  }
</style>