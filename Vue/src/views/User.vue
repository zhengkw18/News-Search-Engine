<template>
  <div v-title data-title="Spect个人中心" id="user-page">
    <el-container>
      <el-header height="fit-content" class="isFixed" style="padding: 0; background-color: white;">
        <UserHeader/>
        <div class="header-line"></div>
      </el-header>
      <el-main style="padding: 0;">
        <el-col :xs="24" :sm="8" :md="7" :lg="5" style="position: relative;">
          <div style="padding-top: 0.3rem;" class="hidden-xs-only">
            <div class="user-avatar">
              <img v-lazy="default_user_src" class="user-img">
            </div>
            <p class="user-name">{{ username().slice(0, 10) }}</p>
          </div>

          <el-col class="user-function-item" v-for="(name, index) in functionNames" v-bind:key="index"
            :xs="8" :sm="24" :md="24" :lg="24" v-on:click.native="activeIndex=index" :style="activeColor(index)">
            <el-row class="user-function-item__inner">
              <el-col :xs="24" :sm="{span: 4, offset: 4}" :md="{span: 4, offset: 4}" :lg="{span: 4, offset: 4}">
                <i :class="functionIcons[index]" class="function-icon"></i>
              </el-col>
              <el-col :xs="24" :sm="8" :md="8" :lg="8">
                <p class="function-name">{{ name }}</p> 
              </el-col>
            </el-row>
            <div class="function-line hidden-xs-only" v-if="index < functionNames.length - 1"></div>
          </el-col>
        </el-col>

        <el-col :xs="24" :sm="16" :md="17" :lg="19" style="background-color: #f3f5fb;">
          <el-card class="user-function-block">
            <el-col :xs="24" :sm="20" :md="16" :lg="12">
              <component :is="functionComponents[activeIndex]" v-on:success="success(...arguments)"/>
            </el-col>
          </el-card>
        </el-col>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import UserHeader from "@/components/UserHeader"
import UserTags from "@/components/UserTags"
import UserInformation from "@/components/UserInformation"
import UserPassword from "@/components/UserPassword"
import cookie from "@/utils/cookie"
import 'element-ui/lib/theme-chalk/display.css';
var debounce = require("lodash/debounce")
export default {
  name: "User",
  components: {
    UserHeader,
    UserTags,
    UserInformation,
    UserPassword
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
  data(){
    return{
      default_user_src: require('../assets/default-user.jpg'),
      functionNames: ["用户标签", "注册信息", "修改密码"],
      functionIcons: ["el-icon-price-tag", "el-icon-edit-outline", "el-icon-unlock"],
      functionComponents: ["UserTags", "UserInformation", "UserPassword"],

      activeIndex: 0
    }
  },
  methods: {
    respond: debounce(function(){
        this.respondInner()
      }, 100),
    respondInner(){
      let headerHeight = document.getElementsByClassName("el-header")[0].clientHeight
      let height = document.documentElement.clientHeight
      document.getElementsByClassName("el-card")[0].style["minHeight"] = height - headerHeight + "px";

      document.getElementsByClassName("el-main")[0].style["marginTop"] = headerHeight + "px";
    },
    activeColor(index){
      if (index == this.activeIndex){
        return "color: #2d6df8;"
      }
      else{
        return "color: black;"
      }
    },
    username(){
      return cookie.get_cookie("username")
    },

    success(...args){
      this.$notify({
        showClose: true,
        title: args[0],
        type: 'success',
        duration: 2 * 1000,
        position: 'bottom-right'
      });
      this.activeIndex = 0;
    }
  }
}
</script>

<style>
  #user-page{
    font-size: 0.22rem;
  }
  #user-page .isFixed{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
  }
  #user-page .header-line{
    width: 100%;
    height: 2px;
    background-color: #E4E7ED;
  }
  #user-page .user-avatar{
    height: 0.75rem;
    width: 0.75rem;
    line-height: 0.75rem;
    border-radius: 50%;
    position: relative;
    margin: 0 auto;
  }
  #user-page .user-img{
    height: 100%;
    width: 100%;
    border-radius: 50%;
    object-fit: cover;
  }
  #user-page .user-name{
    font-size: 0.22rem;
    line-height: 0.22rem;
    margin-top: 0.1rem;
  }

  #user-page .user-function-item{
    background-color: white;
    cursor: pointer;
  }
  #user-page .user-function-item:hover{background-color: rgb(245, 247, 252);}
  #user-page .function-name{
    font-size: 0.18rem;
    margin: 0;
  }
  #user-page .user-function-item__inner{
    padding-top: 0.18rem;
    padding-bottom: 0.18rem;
  }
  #user-page .function-line{
    width: 100%;
    height: 1px;
    background-color: #E4E7ED;
  }

  #user-page .user-function-block{
    margin: 0.1rem; 
    border-radius: 10px;
  }
</style>