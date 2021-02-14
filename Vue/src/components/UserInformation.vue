<template>
  <div style="text-align: left;" id="user-information">
    <p class="header-title">用户注册信息</p>
    <p class="label">用户名</p>
    <el-input type="text" :placeholder="username()" :disabled=true></el-input>
    <p class="label">邮箱</p>
    <el-input type="text" :placeholder="email" :disabled=true></el-input>
  </div>
</template>

<script>
import cookie from "@/utils/cookie"
import communication from "@/utils/communication"
export default {
  name: "UserInformation",
  data(){
    return{
      email: ""
    }
  },
  mounted(){
    this.loadEmail()
  },
  methods: {
    username(){
      let username = cookie.get_cookie("username")
      if (username == ""){
        this.$router.push({name: "Home"})
      }
      return username
    },
    loadEmail(){
      communication.get_info(this.getEmail);  
    },
    getEmail(success, data){
      if (success){
        this.email = data.email      
      }
    }
  }
}
</script>

<style>
  #user-information{
    font-size: 0.26rem;
    padding: 0.1rem;
  }
  #user-information .header-title{
    margin-top: 0;
    font-size: 0.26rem;
    font-weight: bold;
    margin-bottom: 0.6rem;
  }

  #user-information .label{
    font-size: 15px;
    margin-bottom: 10px;
  }
</style>