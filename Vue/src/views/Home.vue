<template>
  <div id="home" v-title data-title="Spect新闻——中文资讯平台">
    <el-container>
      <el-header height="fit-content" class="isFixed" style="padding: 0;">
        <SearchHeader name="注册" path="Register" v-on:login="dialogVisible = true"/>
        <el-row style="padding: 0 20px;">
          <el-col :xs="24" :sm="{span: 12, offset: 3}" :md="{span: 12, offset: 3}" :lg="{span: 12, offset: 2}">
            <el-tabs v-model="activeName" @tab-click="handleClick">
              <el-tab-pane v-for="(chinese, channel) in channelMap" :key="channel" :label="chinese" :name="channel"></el-tab-pane>
            </el-tabs>
          </el-col>
        </el-row>
        <div class="tabs-line"></div>
      </el-header>
      <el-main v-show="newsList.length > 0">
        <el-col :xs="24" :sm="{span: 12, offset: 3}" :md="{span: 12, offset: 3}" :lg="{span: 12, offset: 2}">
          <HomeNewsList :newsList="newsList" @loadmore="loadMore"/>
          <el-button
            :disabled=false
            v-show = "loading && !finish"
            class="footer-button">加载中...</el-button> 
        </el-col>
        <el-col :xs="0" :sm="{span: 7, offset: 1}" :md="{span: 6, offset: 1}" :lg="{span: 5, offset: 1}" v-show="todayNewsList.length + sinaNewsList.length > 0">
          <div class="right-bar">
            <div class="today-news-header">
              <img src="//mat1.gtimg.com/news/news2013/img/jrhtLogo.png" alt="今日话题" class="today-news-img">
            </div>
            <el-row v-for="news in todayNewsList" :key="news.id" class="today-news-item">
              <a :href="news.url" target="_blank">{{ news.title }}</a>
            </el-row>
            <el-row v-for="news in sinaNewsList" :key="news.id" class="today-news-item">
              <a :href="news.url" target="_blank">{{ news.title }}</a>
            </el-row>
          </div>
        </el-col>
      </el-main>
    </el-container>

    <LoginDialog 
        v-bind:dialogVisible="dialogVisible"
        v-bind:state="state"
        v-on:success="login_success"
        v-on:hide="dialogVisible=false">
      </LoginDialog>
  </div>
</template>

<script>
import SearchHeader from "@/components/SearchHeader"
import HomeNewsList from "@/components/HomeNewsList"
import communication from "@/utils/communication"
import openCommunication from "@/utils/openCommunication"
import LoginDialog from "@/components/LoginDialog"
import cookie from "@/utils/cookie"
import newsLogic from "@/utils/newsLogic"
var debounce = require("lodash/debounce")
export default {
  name: 'Home',
  components: {
    SearchHeader,
    LoginDialog,
    HomeNewsList
  },
  data() {
    return {
      activeName: 'all',
      channelMap: {
        "all": "首页","astro": "星座", "weather": "天气", "houseliving": "家居", "agriculture": "农业", "ent": "娱乐", 
        "photography": "摄影", "digital": "数码", "edu": "教育", "game": "游戏", "religion": "宗教", 
        "comic": "漫画", "mil": "军事", "career": "职业", "cul": "文化", "": "其它", 
        "life": "生活", "women": "女性", "travel": "旅游", "emotion": "情感", "chuguo": "出国", 
        "inspiration": "启示", "health": "健康", "history": "历史", "society": "社会", "lifestyle": "生活方式", 
        "tech": "科技", "pet": "宠物", "finance": "财经", "science": "科学", "house": "住房", 
        "auto": "汽车", "lottery": "彩票", "baby": "育儿", "funny": "幽默", "sports": "运动", 
        "politics": "政治", "food": "饮食", "law": "法律"
      },
      newsList: [],
      error_info: "",

      loading: false,
      finish: false, // 是否加载完成
      loadStart: 0,
      loadSize: 10,

      todayNewsList: [],
      sinaNewsList: [],

      dialogVisible: false,
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
    this.load()
    this.getTodayNews()
    this.getSinaNews()
    window.addEventListener('resize', this.respond)
  },
  // 页面销毁，移除滚动监听
  beforeDestroy () {
    window.removeEventListener('resize', this.respond)
  },
  methods:{
    respond: debounce(function(){
        this.respondInner()
      }, 100),
    respondInner(){
      let height = document.getElementsByClassName("el-header")[0].clientHeight
      document.getElementsByClassName("el-main")[0].style["marginTop"] = height + "px";
    },
    load(){
      this.newsList = []
      this.loadStart = 0
      if (Object.prototype.hasOwnProperty.call(this.$route.query, "chnl")){
        this.activeName = this.$route.query.chnl
      }
      else{
        this.activeName = "all"
      }
      this.loadMore()
    },
    loadMore(){
      this.loading = true
      communication.send_home({
        "start": this.loadStart,
        "size": 2 * this.loadSize,
        "channel": this.activeName
      }, this.callback)
    },
    callback(success, data){
      this.loading = false
      if (success){
        this.error_info=""
        if (!Object.prototype.hasOwnProperty.call(data, "username")){
          cookie.delete_cookie("username")
          cookie.delete_cookie("password")
        }
        if (data["data"].length > 0){
          if (this.newsList.length == 0){
            this.newsList = data["data"].slice(0, this.loadSize)
            this.loadStart = this.newsList.length
          }
          else{
            let firstIndex = this.newsList.findIndex((el) => {
              return el.title == data["data"][0].title && el.time == data["data"][0].time
            })
            let lastIndex = data["data"].findIndex((el) => {
              return el.title == this.newsList[this.newsList.length - 1].title
            })
            if (lastIndex < 0 && firstIndex >= 0){
              this.loadStart += this.newsList.length - firstIndex
            }
            else{
              let addList = data["data"].slice(lastIndex + 1, lastIndex + 1 + this.loadSize)
              this.newsList = this.newsList.concat(addList)
              this.loadStart += addList.length + lastIndex + 1
            }
          }
        }
        this.finish = this.newsList.length > 150 || data["data"].length == 0
      }
      else{
        this.error_info = data
        this.finish = true
      }
    },
    handleClick(tab){
      this.$router.push({    
        name: 'Home',  
        query: {   
          "chnl": tab.name
        }   
      }) 
    },

    getTodayNews(){
      openCommunication.get_today_news({
        "pull_urls": "today_topic_2018"
      }, this.loadTodayNews)
    },
    loadTodayNews(data){
      this.todayNewsList = []
      for (let i = 0; i < data["data"].length; i += 2){
        this.todayNewsList.push(data["data"][i])
        if (this.todayNewsList.length >= 5){
          break;
        }
      }
    },
    getSinaNews(){
      openCommunication.get_sina_news({
        "top_type": "day",
        "top_cat": "www_www_all_suda_suda",
        "top_time": new Date().getFullYear().toString() + newsLogic.prefixInteger((new Date().getMonth() + 1), 2) + newsLogic.prefixInteger(new Date().getDate(), 2),
        "top_show_num": "5",
        "top_order": "DESC"
      }, this.loadSinaNews)
    },
    loadSinaNews(dataStr){
      var str = "function func(){" + dataStr + "return data['data'];}"
      let func = new Function(`return ${str}`)();
      this.sinaNewsList = func().slice(0, 5)
    },

    login_success(){
      this.dialogVisible=false
      location.reload()
    }
  },
  watch: {
    $route: 'load'
  }
};
</script>

<style>
  #home{
    font-size: 0.22rem; 
  }
  #home .el-header{
    background-color: white; 
    padding-top: 0.1rem;
  }
  #home .isFixed{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
  }

  #home .tabs-line{
    position: absolute;
    left: 0;
    right: 0;
    bottom: -1px;
    height: 2px;
    background-color: #E4E7ED;
    z-index: 1;
  }
  #home .el-tabs{
    font-size: 0.18rem; 
    margin-top: 0.2rem;
  }
  #home .el-tabs__header{
    margin-bottom: 0;
  }
  #home .el-tabs__item{
    font-size: 0.18rem;
    height: 0.4rem;
    line-height: 0.4rem;
  }
  #home .el-tabs__nav-prev{
    font-size: 0.18rem;
    line-height: 0.44rem;
  }
  #home .el-tabs__nav-next{
    font-size: 0.18rem;
    line-height: 0.44rem;
  }
  #home .el-tabs__nav-scroll{
    margin: 0 10px;
  }

  #home .right-bar{
    background-color: #f7f8f9;
    font-size: 0.24rem;
    padding: 0.2rem 0.1rem;
  }
  #home .right-bar a:link, #home .right-bar a:visited{color: black;} 
  #home .right-bar a:hover, #home .right-bar a:active{color: #2d6df8;} 
  #home .right-bar a{
    text-decoration: none; 
  }
  #home .today-news-header{
    font-size: 0.24rem;
    margin-bottom: 0.1rem;
    font-weight: bold;
  }
  #home .today-news-img{
    object-fit: contain;
    height: 0.3rem;
  }
  #home .today-news-item{
    background: url(//mat1.gtimg.com/pingjs/ext2020/test2017/build/static/images/news_dot.png) left 0.13rem no-repeat;
    line-height: 0.2rem;
    padding: 0.06rem 0 0.06rem 0.15rem;
    text-align: left;
    font-size: 0.15rem;
  }

  #home .footer-button{
      width: 100%;
      border-radius: 0.04rem;
      font-size: 0.14rem;
      background-color: #E4E7ED;
      color: black;
      padding-top: 0.08rem;
      padding-bottom: 0.08rem;
      border-width: 0;
    }
</style>