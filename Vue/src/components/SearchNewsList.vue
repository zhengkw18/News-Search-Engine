<template>
  <div id="search-news-list">
    <el-row v-for="news in newsList" :key="news.id" style="margin-bottom: 2vh;">
      <a :href="news.href" target="_blank" class="news-title" v-html="news.title" @click="record(news.tags)" @click.middle="record(news.tags)" @click.right="record(news.tags)"></a>
      <div>
        <el-col :span="6" v-if='news.image != ""'> 
          <img v-lazy="news.image" alt="" class="news-img" @click="enter_news(news.href, news.tags)" @click.middle="record(news.tags)" @click.right="record(news.tags)">
        </el-col> 
        <el-col :span="18 + 6 * (news.image == '')">
          <p class="news-source" v-html="news.source.slice(0, 8) + '&nbsp;&nbsp;&nbsp;&nbsp;' + getTime(news.time)"></p>
          <p class="news-content" v-html="news.content"></p>
        </el-col>  
      </div>
    </el-row>
  </div>
</template>

<script>
import communication from "@/utils/communication"
import newsLogic from "@/utils/newsLogic"
export default {
  name: "SearchNewsList",
  props: {
    newsList: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    enter_news(href, tags){
      this.$nextTick(this.record(tags))
      window.open(href, '_blank');
    },
    record(tags){
      communication.update_tags(newsLogic.dealTags, tags);
    },
    getTime(time){
      return newsLogic.getTime(time)
    }
  }
}
</script>

<style scoped>
  #search-news-list{
    font-size: 0.18rem;
  }
  #search-news-list .news-title {
    font-size: 0.18rem;
    display: -webkit-box; 
    -webkit-line-clamp: 1; 
    -webkit-box-orient: vertical;  
    overflow: hidden;
    text-decoration: none;
    margin-bottom: 0.08rem;
  }
  #search-news-list a.news-title:hover, a.news-title:active{
    color: #2d6df8;
    text-decoration: underline;
  }

  #search-news-list .news-img{
    width: 90%; 
    height: 0.85rem; 
    object-fit: cover;
    cursor: pointer; 
    vertical-align: top;
  }

  #search-news-list .news-source{
    font-size: 0.14rem; 
    color: #808080; 
    margin-bottom: -0.1rem;
    display: -webkit-box; 
    -webkit-line-clamp: 1; 
    -webkit-box-orient: vertical;  
    overflow: hidden;
    margin-top: 0;
  }
  #search-news-list .news-content {
    font-size: 0.14rem;
    display: -webkit-box; 
    -webkit-line-clamp: 3; 
    -webkit-box-orient: vertical; 
    overflow: hidden;
  }
</style>