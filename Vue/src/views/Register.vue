<template>
  <div v-title data-title="注册Spect账号">
    <div class="register-background">
      <img class="register-background-img" v-lazy="background_src" alt="">
    </div>
    <el-col :xs="24" :sm="{span: 13, offset: 6}" :md="{span: 11, offset: 7}" :lg="{span: 9, offset: 8}">
      <div id="register-dialog">
        <div class="header">
          <p class="header-title">欢迎注册</p>
          <p class="header-error">{{ error_info }}</p>
        </div>

        <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="auto" id="register-form">
            <el-form-item label="用户名" prop="username">
              <el-popover
                ref="popover-username"
                placement="top-start"
                trigger="focus"
                content="设置后不可更改，仅支持中英文、数字和下划线">
              </el-popover>
              <el-input type="text" v-popover:popover-username placeholder="请输入用户名" v-model="ruleForm.username"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input placeholder="请输入邮箱地址" v-model="ruleForm.email" autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-popover
                ref="popover-password"
                placement="top-start"
                trigger="focus"
                content="长度在5个字符以上">
              </el-popover>
              <el-input type="password" v-popover:popover-password placeholder="请输入密码" v-model="ruleForm.password"  autocomplete="off"></el-input>
            </el-form-item>
            <el-form-item label="激活码" prop="check">
              <el-col :span="12">
                <el-input placeholder="请输入激活码" v-model="ruleForm.check" autocomplete="off"></el-input>
              </el-col>
              <el-col :span="12">
                <el-button 
                :disabled="codeDisabled" 
                @click="codeVisible = true;" 
                class="check-button">{{ btntxt }}</el-button>
              </el-col>
              <div class="form-item__tip" v-show="disabled">
                {{ restxt }}
              </div>
            </el-form-item>
        </el-form>
        
        <div class="footer">
          <el-button type="primary"
                      :disabled="registerDisabled"
                      v-on:click="register()"
                      >注册</el-button>
          <p style="font-size: 16px;">已有账号？马上<span class="login" v-on:click="dialogVisible=true">登录</span></p>
        </div>
      </div>
    </el-col>

    <LoginDialog 
      v-bind:dialogVisible="dialogVisible"
      v-bind:state="state"
      v-on:success="login_success"
      v-on:hide="dialogVisible=false">
    </LoginDialog>
    <AuthCode
      v-bind:dialogVisible="codeVisible"
      v-on:hide="codeVisible=false"
      v-on:success="code_success">
    </AuthCode>
  </div>
</template>

<script>
import communication from "@/utils/communication"
import cookie from "@/utils/cookie"
import LoginDialog from "@/components/LoginDialog"
import AuthCode from "@/components/AuthCode"
var debounce = require("lodash/debounce")
export default {
  name: "Register",
  components: {
    LoginDialog,
    AuthCode
  },
  data(){
    var validateUsername = (rule, value, callback) => {
      if (!/^[A-Za-z\u4e00-\u9fa5][-A-Za-z0-9\u4e00-\u9fa5_]*$/.test(value)){
        callback(new Error('用户名格式错误'));
      } else{
        callback();
      }
    };
    return {
      background_src: require('../assets/register-backgroud.jpg'),

      error_info:"",

      ruleForm:{
        username: "",
        email: "",
        password: "",
        check: ""
      },
      rules: {
        username: [
          { required: true, message: '用户名不能为空', trigger: 'blur' },
          { validator: validateUsername, trigger: 'blur' }
        ],
        email: [
          { required: true, message: '邮箱地址不能为空', trigger: 'blur' },
          { type: 'email', message: '邮箱地址格式错误', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '密码不能为空', trigger: 'blur' },
          { min: 5, message: '密码长度不足', trigger: 'blur' }
        ]
      },
      valid: false,

      disabled: false,
      time: 0,
      btntxt: "获取激活码",
      restxt: "邮箱激活码已发送，请您在30分钟内填写",

      codeVisible: false,
      alreadySent: false,
      
      dialogVisible:false,
      state:{
        username:"",
        password:""
      } 
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.respondInner()
    })
    window.addEventListener('resize', this.respond) 
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.respond)
  },
  methods: {
    respond: debounce(function(){
        this.respondInner()
      }, 100),
    respondInner(){
      let wh = document.documentElement.clientHeight
      let height = document.getElementById("register-dialog").clientHeight
      if (height + 15 > wh){
        document.getElementsByClassName("register-background-img")[0].style['height'] = height + 15 + "px";
      }
      else{
        document.getElementsByClassName("register-background-img")[0].style['height'] = wh + "px"
      }
      let ww = document.documentElement.clientWidth
      if (ww <= 480){
        for (let i = 0; i < 4; i ++){
          document.getElementsByClassName("el-form-item__label-wrap")[i].style["display"] = "none"
          document.getElementsByClassName("el-form-item__content")[i].style["marginLeft"] = 0
        }
      }else{
        for (let i = 0; i < 4; i ++){
          document.getElementsByClassName("el-form-item__label-wrap")[i].style["display"] = ""
          document.getElementsByClassName("el-form-item__content")[i].style["marginLeft"] = 76 + "px"
        }
      }
    },
    sendCode(){
      if (!this.codeDisabled) {
        communication.send_email({
        "email": this.ruleForm.email},  
        this.emailRes)
      }
      else{
        this.restxt = "邮箱激活码发送失败，请您稍后重试"
        this.time = 10;
        this.disabled = true;
        this.timer();
      }    
    },
    emailRes(success, error_info){
      if (success){
        this.restxt = "邮箱激活码已发送，请您在30分钟内填写"
        this.alreadySent = true;
      }
      else{
        this.restxt = error_info
      }
      this.time = 60;
      this.disabled = true;
      this.timer();
    },
    timer() {
      if (this.time > 0) {
        this.time --;
        this.btntxt=this.time + "s后重新获取";
        setTimeout(this.timer, 1000);
      } else{
        this.time = 0;
        this.btntxt = "获取激活码";
        this.disabled = false;
      }
    },

    register(){
      if (!this.registerDisabled) {
        communication.send_register({
          "username": this.ruleForm.username,
          "email":this.ruleForm.email,
          "password": this.ruleForm.password,
          "authcode": this.ruleForm.check}, 
        this.callback)
      } else {
        this.error_info = "注册失败，请您检查注册信息"
      }
    },
    callback(success, error_info){
      if (success){
        this.error_info=""
        cookie.add_cookie("username", this.ruleForm.username, 24)
        cookie.add_cookie("password", this.ruleForm.password, 24)
        this.$router.push({name:'Home'})
      }
      else{
        this.error_info = error_info
      }
    },
    code_success(){
      this.codeVisible = false
      this.sendCode()
    },
    login_success(){
      this.dialogVisible=false
      this.$router.push({name:'Home'})
    }
  },
  computed: {
    codeDisabled() {
      return !this.valid || this.disabled
    },
    registerDisabled() {
      return !this.valid || this.ruleForm.check == '' || !this.alreadySent
    }
  },
  watch: {
    ruleForm:{
      handler(){
        this.$refs['ruleForm'].validate((valid) => {
          this.valid = valid
        });
      },
      deep:true
    }
  }
}
</script>

<style scoped>
    .register-background{
      width: 100%;
      height: 100%; 
      z-index: -1;
      position: absolute;
      top: 50%;
      left: 50%;
      transform:translate(-50%,-50%);
    }
    .register-background-img{
      width: 100%; 
      object-fit: cover;
    }

    #register-dialog{ 
      height: fit-content;
      padding: 0.3rem;
      margin: 0.1rem;
      background-color: rgba(255,255,255, 0.9);
      border-radius: 10px;
      font-size: 16px;
    }
    
    #register-dialog .header{
      float: top;
      margin-bottom: 40px;
    }
    #register-dialog .header-title{
      margin-top: 0;
      font-size: 0.4rem;
      font-weight: bold;
      margin-bottom: -0.1rem;
    }
    #register-dialog .header-error{
      font-size: 15px;
      color: red;
      position: absolute;
    }

    #register-form .el-form-item{
      margin-bottom: 35px;
    }
    #register-form >>> .el-form-item__label{
      font-size: 16px !important;
    }
    #register-form >>> .el-input{
      font-size: 15px !important;
    }
    #register-dialog >>> .el-input__inner{
      padding-left: 11px !important;
      padding-right: 11px !important;
    }
    
    #register-form >>> .el-form-item__error{
      font-size: 13px !important;
    }
    #register-dialog .check-button{
      font-size: 0.14rem;
      height: 40px;
      padding-left: 0.1rem;
      padding-right: 0.1rem;
      width: 1.2rem;
      float: right;
    }
    #register-dialog .form-item__tip{
      font-size: 13px;
      line-height: 1;
      padding-top: 4px;
      position: absolute;
      top: 100%;
      left: 0;
    }

    #register-dialog .footer{
      float: bottom;
      margin-top: 0.4rem;
    }
    #register-dialog .footer .el-button{
      width: 100%;
      border-radius: 10px;
      font-size: 17px;
      padding-top: 12px;
      padding-bottom: 12px;
    }
    #register-dialog .login{
      cursor: pointer; 
      color: #0000ff;
      text-decoration: underline;
    }
</style>

<style>
  .el-popover{
    font-size: 13px !important;
    padding: 6px 8px !important;
  }
</style>