<template>
  <div id="search-header">
    <el-row>
      <el-col :xs="12" :sm="3" :md="3" :lg="2">
        <img v-lazy="logo_src" alt="" class="search-img" v-on:click="home"/>
      </el-col>
      <el-col :xs="0" :sm="14" :md="14" :lg="14" class="hidden-xs-only">
        <SearchBar :keyword="keyword"/>
      </el-col>
      <el-col :xs="12" :sm="7" :md="7" :lg="8">
        <el-button type="primary"
          v-show='username() == ""'
          v-on:click="login"
          class="login-button">登录</el-button>
        <el-dropdown v-show='username() != ""' style="float: right;">
          <div>
            <p class="header-hover" style="margin-bottom: 0;">{{ username().slice(0, 5) }}</p>
            <div class="user-avatar">
              <img v-lazy="default_user_src" class="user-img">
            </div>
          </div>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item class="user-dropdown-item" @click.native="userPage">个人中心</el-dropdown-item>
            <el-dropdown-item class="user-dropdown-item" @click.native="logout">退出</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <p class="header-hover" style="margin-right: 2vw;" @click="jump">{{ name }}</p>
      </el-col> 
      <el-col class="hidden-sm-and-up">
        <SearchBar :keyword="keyword" style="margin-top: 0.1rem;"/>
      </el-col>     
    </el-row>
  </div>
</template>

<script>
import SearchBar from "@/components/SearchBar"
import cookie from "@/utils/cookie"
import 'element-ui/lib/theme-chalk/display.css';
export default {
  name: "SearchHeader",
  components: {
    SearchBar
  },
  props: {
    name: {
      type: String,
      default: () => "首页"
    },
    path: {
      type: String,
      default: () => "Home"
    },
    keyword: {
      type: String,
      default: () => ""
    }
  },
  data() {
    return {
      logo_src: require('../assets/logo.jpg'),
      default_user_src: require('../assets/default-user.jpg')
    }
  },
  methods: {
    jump(){
      if (this.path == "Register"){
        let routeUrl = this.$router.resolve({
          path: "/register"
        });
        window.open(routeUrl.href, '_blank');
      }
      else{
        this.$router.push({name:this.path})
      }
    },
    home(){
      this.$router.push({name: "Home"})
    },
    login(){
      this.$emit('login')
    },
    logout(){
      cookie.delete_cookie("username")
      cookie.delete_cookie("password")
      location.reload()
    },
    userPage(){
      let routeUrl = this.$router.resolve({
          path: "/user"
        });
      window.open(routeUrl.href, '_blank');
    },
    username(){
      return cookie.get_cookie("username")
    }
  }
}
</script>

<style>
  #search-header{
    font-size: 0.16rem;
    background-color: white;
    padding: 8px 20px;
  }
  #search-header .header-hover{
    float: right; 
    cursor: pointer; 
    font-size: 0.16rem;
    line-height: 0.16rem;
  }
  #search-header p.header-hover:hover{
    color: blue;
  }
  #search-header .search-img{
    height: 0.43rem; 
    max-width: 90%; 
    object-fit: contain;
    float: left;
    cursor: pointer;
  }

  #search-header .login-button{
    float: right;
    font-size: 0.16rem;
    padding: 0.05rem 0.12rem;
    border-radius: 6px;
    margin-top: 0.1rem;
  }

  #search-header .user-avatar{
    height: 0.35rem;
    width: 0.35rem;
    line-height: 0.35rem;
    border-radius: 50%;
    border: 0.01rem solid blue;
    float: right;
    margin-right: 1vw;
    margin-top: 0.05rem;
    padding: 0.02rem;
    cursor: pointer;
  }
  #search-header .user-img{
    height: 100%;
    width: 100%;
    border-radius: 50%;
    object-fit: cover;
  }
  .user-dropdown-item{
    padding: 0.1rem 0.14rem !important;
    font-size: 0.14rem !important;
    line-height: 0.14rem !important;
  }
</style>