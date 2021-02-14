<template>
  <div id="user-header">
    <el-row>
      <el-col :xs="12" :sm="10" :md="8" :lg="6">
        <img v-lazy="logo_src" alt="" class="search-img" v-on:click="home"/>
        <div class="hidden-xs-only">
          <div class="seg-line"></div>
          <p class="header-hover" style="margin-left: 1vw; float: left;">个人中心</p>
        </div>
      </el-col>
      <el-col :xs="12" :sm="14" :md="16" :lg="18">
        <el-dropdown style="float: right;">
          <div class="user-avatar">
            <img v-lazy="default_user_src" class="user-img">
          </div>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item class="user-dropdown-item" @click.native="logout">退出</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <p class="header-hover" style="margin-right: 2vw; float: right;" @click="home">{{ name }}</p>
      </el-col>    
    </el-row>
  </div>
</template>

<script>
import cookie from "@/utils/cookie"
import 'element-ui/lib/theme-chalk/display.css';
export default {
  name: "UserHeader",
  data() {
    return {
      name: "首页",
      logo_src: require('../assets/logo.jpg'),
      default_user_src: require('../assets/default-user.jpg')
    }
  },
  created(){
    if (cookie.get_cookie("username") == ""){
      this.home()
    }
  },
  methods: {
    home(){
      this.$router.push({name: "Home"})
    },
    logout(){
      cookie.delete_cookie("username")
      cookie.delete_cookie("password")
      this.home()
    }
  }
}
</script>

<style>
  #user-header{
    font-size: 0.16rem;
    background-color: white;
    padding: 8px 20px;
  }
  #user-header .search-img{
    height: 0.43rem; 
    max-width: 90%; 
    object-fit: contain;
    float: left;
    cursor: pointer;
  }
  #user-header .seg-line{
    width: 2px;
    height: 0.16rem;
    margin-top: 0.16rem;
    margin-left: 1vw;
    background-color: #E4E7ED;
    float: left;
  }
  #user-header .header-hover{
    cursor: pointer; 
    font-size: 0.16rem;
    line-height: 0.16rem;
    font-weight: bold;
  }
  #user-header p.header-hover:hover{
    color: blue;
  }

  #user-header .el-dropdown .user-avatar{
    height: 0.4rem;
    width: 0.4rem;
    line-height: 0.4rem;
    border-radius: 50%;
    float: right;
    margin-top: 0.03rem;
    cursor: pointer;
  }
  #user-header .el-dropdown .user-img{
    height: 100%;
    width: 100%;
    border-radius: 50%;
    object-fit: cover;
  }
  #user-header .user-dropdown-item{
    padding: 0.1rem 0.14rem !important;
    font-size: 0.14rem !important;
    line-height: 0.14rem !important;
  }
</style>