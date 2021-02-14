<template>
  <div style="text-align: left;" id="user-password">
      <div class="header">
          <p class="header-title">请设置新密码</p>
          <p class="header-error">{{ error_info }}</p>
        </div>
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="auto" id="user-password-form">
          <p class="label">用户名</p>
          <el-input type="text" :placeholder="username()" :disabled=true></el-input>
          <p class="label">密码</p>
          <el-form-item prop="password">
            <el-popover
              ref="popover-password"
              placement="top-start"
              trigger="focus"
              content="长度在5个字符以上">
            </el-popover>
            <el-input type="password" v-popover:popover-password placeholder="请输入密码" v-model="ruleForm.password"  autocomplete="off"></el-input>
          </el-form-item>
      </el-form>
      <el-col :xs="24" :sm="8" :md="8" :lg="8">
        <el-button type="primary"
          :disabled="valid===false"
          v-on:click="update()">确定</el-button>
      </el-col>
  </div>
</template>

<script>
import communication from "@/utils/communication"
import cookie from "@/utils/cookie"
export default {
  name: "UserPassword",
  data(){
    var validatePassword = (rule, value, callback) => {
      if (value == cookie.get_cookie("password")) {
        callback(new Error('新密码不能与旧密码相同'));
      } else {
        callback();
      }
    };
    return{
      error_info:"",

      ruleForm:{
        password: ""
      },
      rules: {
        password: [
          { required: true, message: '密码不能为空', trigger: 'blur' },
          { min: 5, message: '密码长度不足', trigger: 'blur' },
          { validator: validatePassword, trigger: 'blur' }
        ]
      },
      valid: false,
    }
  },
  methods: {
    update(){
      if (this.valid) {
        communication.send_user_update({
          "password": this.ruleForm.password}, 
        this.callback)
      } else {
        this.error_info = "密码修改失败"
      }
    },
    callback(success, error_info){
      if (success){
        this.error_info=""
        cookie.add_cookie("password", this.ruleForm.password, 24)
        this.$emit("success", "密码修改成功！")
      }
      else{
        this.error_info = error_info
      }
    },
    username(){
      let username = cookie.get_cookie("username")
      if (username == ""){
        this.$router.push({name: "Home"})
      }
      return username
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
  #user-password{
    font-size: 0.26rem;
    padding: 0.1rem;
  }
  #user-password .header{
    float: top;
    margin-bottom: 60px;
  }
  #user-password .header-title{
    margin-top: 0;
    font-size: 0.26rem;
    font-weight: bold;
    margin-bottom: -0.1rem;
  }
  #user-password .header-error{
    font-size: 15px;
    color: red;
    position: absolute;
  }

  #user-password .label{
    font-size: 15px;
    margin-bottom: 10px;
  }

  #user-password .el-button{
    margin-top: 0.3rem;
    font-size: 14px;
    padding-top: 8px;
    padding-bottom: 8px;
    width: 100%;
  }
</style>