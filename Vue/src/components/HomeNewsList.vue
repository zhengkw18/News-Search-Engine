<template>
  <div id="home-news-list">
    <el-row v-for="(news, index) in newsList" :key="index" class="news-block">
      <el-col :span="9" v-if="news.image != ''"> 
        <div class="news-left">
          <img v-lazy="news.image" alt="" class="news-img" @click="enter_news(news.href, news.tags)" @click.middle="record(news.tags)" @click.right="record(news.tags)">
        </div>
      </el-col> 
      <el-col :span="15 + 9 * (news.image == '')">
        <a :href="news.href" target="_blank" class="news-title" @click="record(news.tags)" @click.middle="record(news.tags)" @click.right="record(news.tags)">{{ news.title }}</a>
        <div class="news-tags">
          <el-tag
            v-for="tag in getTags(news.tags)"
            :key="tag"
            type="info">
            {{ tag }}
          </el-tag>
        </div>
        <p class="news-source" v-html="getSource(news.source.slice(0, 8), news.href) + '&nbsp;&nbsp;&nbsp;&nbsp;' + getTime(news.time)"></p>
      </el-col> 
    </el-row>
    <el-backtop :visibility-height="clientHeight">
      <el-button class="backtop-button" icon="el-icon-top" circle></el-button>
    </el-backtop>
  </div>
</template>

<script>
import communication from "@/utils/communication"
import newsLogic from "@/utils/newsLogic"
var debounce = require("lodash/debounce")
export default {
  name: "SearchNewsList",
  props: {
    newsList: {
      type: Array,
      default: () => []
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
  },
  updated(){
    this.handleScroll()
  },
  /*
  activated(){
    this.handleScroll()
  },*/
  // 页面销毁，移除滚动监听
  beforeDestroy () {
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    enter_news(href, tags){
      this.$nextTick(this.record(tags))
      window.open(href, '_blank');
    },
    record(tags){
      communication.update_tags(newsLogic.dealTags, tags);
    },
    getTags(tags){
      let tagList = tags.trim().split(/[,;；\s]+/)
      let finalList = []
      for (let i = 0; i < tagList.length; i ++){
        if (tagList[i] == ""){
          continue;
        }
        finalList.push(tagList[i])
        if (finalList.length >= 3){
          break;
        }
      }
      return finalList;
    },
    getSource(source, href){
      if (href.indexOf("qq.com") >= 0){
        return "腾讯&nbsp;&nbsp;" + source;
      }
      if (href.indexOf("sina.com.cn") >= 0){
        return "新浪&nbsp;&nbsp;" + source;
      }
      return source;
    },
    getTime(time){
      return newsLogic.getTime(time)
    },
    handleScroll: debounce(function(){
        // 兼容Edge, Chrome浏览器
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
        // 内容距离底部多少距离 = 内容总高度 - 滚动高度 - 当前可视高度
        if (document.documentElement.scrollHeight - scrollTop - 2 * document.documentElement.clientHeight < 0 && !this.loading && !this.finish) {
          this.$emit("loadmore")
        }
      }, 500)
  },
  computed:{
    clientHeight(){
      return document.documentElement.clientHeight;
    }
  }
}
</script>

<style scoped>
  #home-news-list{
    background-color: #E4E7ED;
    font-size: 0.22rem; 
  }
  #home-news-list .news-block{
    text-align: left; 
    margin-bottom: 1px; 
    padding-top: 0.2rem; 
    height: 1.65rem;
    background-color: white;
  }
  #home-news-list .news-block:hover{background-color: rgb(245, 247, 252);}
  #home-news-list .news-block a:link, #home-news-list .news-block a:visited{color: black;} 
  #home-news-list .news-block a:hover, #home-news-list .news-block a:active{color: #2d6df8;} 

  #home-news-list .news-left{
    width: 90%; 
    height: 1.25rem;
    overflow: hidden;
  }
  #home-news-list .news-img{ 
    width: 100%;
    height: 100%;
    object-fit: cover;
    cursor: pointer; 
  }
  #home-news-list .news-img{
    transition: all .3s ease;
  }
  #home-news-list .news-img:hover{
    transform: scale(1.05);
  }

  #home-news-list .news-title{
    font-size: 0.22rem; 
    text-decoration: none; 
    display: -webkit-box; 
    -webkit-line-clamp: 2; 
    -webkit-box-orient: vertical; 
    overflow: hidden;
  }
  #home-news-list .news-tags{
    display: -webkit-box; 
    -webkit-line-clamp: 1; 
    -webkit-box-orient: vertical;  
    overflow: hidden;
  }
  #home-news-list .el-tag{
    font-size: 0.14rem; 
    height: 0.26rem;
    padding: 0 0.14rem;
    line-height: 0.26rem;
    border-width: 0;
    border-radius: 0.1rem;
    margin: 0.1rem 0.14rem 0 0;
  }
  #home-news-list .news-source{
    font-size: 0.14rem; 
    color: #808080; 
    position: absolute; 
    bottom: 0.1rem;
    display: -webkit-box; 
    -webkit-line-clamp: 1; 
    -webkit-box-orient: vertical;  
    overflow: hidden;
  }
  #home-news-list .el-backtop{
    width: 0.48rem;
    height: 0.48rem;
  }
  #home-news-list .backtop-button{
    width: 100%;
    height: 100%;
    padding: 0;
    font-size: 0.26rem;
  }
</style>