<template>
  <div id="search-page">
    <el-container>
      <el-header height="fit-content" class="isFixed" style="padding: 0;">
        <SearchHeader :keyword="keyword" v-on:login="dialogVisible = true"/>
      </el-header>
      <el-main>
        <el-col :xs="24" :sm="{span: 12, offset: 3}" :md="{span: 12, offset: 3}" :lg="{span: 12, offset: 2}" class="news-main">
          <div class="hidden-xs-only">
            <transition name="fade" mode="out-in">
              <el-row class="news-top" v-if="curTop == 0" :key="0">
                <el-col :span="18">
                  <p class="news-num">为您找到相关资讯{{ getNewsNum() }}篇</p>
                </el-col>
                <el-col :span="6">
                  <span class="search-tool" @click="curTop=1">
                    <i class="el-icon-s-tools el-icon--left"></i>搜索工具
                  </span>
                </el-col>
              </el-row>
              <el-row class="news-top__approach" v-if="curTop == 1" :key="1">
                <el-col :span="19">
                  <el-select class="dropdown-menues select-approach"
                    v-model="activeValue_0"
                    @change="sendSearch()">
                    <el-option
                      v-for="(approachName, index) in approachNames[0]" 
                      v-bind:key="index"
                      :label="approachName"
                      :value="approaches[0][index]">
                    </el-option>
                  </el-select>
                  <el-select class="dropdown-menues select-site"
                    v-model="activeValue_1"
                    multiple
                    collapse-tags
                    placeholder="全部资讯"
                    @change="sendSearch()">
                    <el-option
                      v-for="(approachName, index) in approachNames[1]" 
                      v-bind:key="index"
                      :label="approachName"
                      :value="approaches[1][index]">
                    </el-option>
                  </el-select>
                  <el-dropdown class="dropdown-menues" @command="handleCommand" trigger="click" ref="dropdown_3">
                    <span style="cursor: pointer;">
                      {{ activeName_2() }}<i class="el-icon-arrow-down el-icon--right"></i>
                    </span>
                    <el-dropdown-menu slot="dropdown" class="search-dropdown-menu">
                      <el-dropdown-item class="search-dropdown-item" v-for="(approachName, index) in approachNames[2]" v-bind:key="index" :command="index">{{ approachName }}</el-dropdown-item>
                      <el-divider></el-divider>
                      <el-row class="dropdown-notitem">
                        <p style="margin-top: 0.1rem;">自定义</p>
                      </el-row>
                      <el-row class="dropdown-notitem">
                        <el-col :span="4">
                          <p style="margin-top: 0.04rem;">从</p>
                        </el-col>
                        <el-col :span="20">
                          <el-date-picker
                            v-model="startValue"
                            type="date"
                            :clearable="false"
                            @change="handleDateChange"
                            :picker-options="{ 'disabledDate': disabledStartValue }">
                          </el-date-picker>
                        </el-col>
                      </el-row>
                      <el-row class="dropdown-notitem">
                        <el-col :span="4">
                          <p style="margin-top: 0.04rem;">至</p>
                        </el-col>
                        <el-col :span="20">
                          <el-date-picker
                            v-model="endValue"
                            type="date"
                            :clearable="false"
                            @change="handleDateChange"
                            :picker-options="{ 'disabledDate': disabledEndValue }">
                          </el-date-picker>
                        </el-col>
                      </el-row>
                      <el-row class="dropdown-notitem">
                        <el-button @click="handleDateConfirm">确定</el-button>
                      </el-row>
                    </el-dropdown-menu>
                  </el-dropdown>
                </el-col>
                <el-col :span="5">
                  <span class="search-tool" @click="removeApproach">
                    <i class="el-icon-arrow-up el-icon--left"></i>收起工具
                  </span>
                </el-col>
              </el-row>
            </transition>
          </div>
          <SearchNewsList :newsList="newsList"/>
        </el-col>
      </el-main>
      <el-footer height="fit-content" style="padding-bottom: 8px;">
        <el-col :xs="24" :sm="{span: 12, offset: 3}" :md="{span: 12, offset: 3}" :lg="{span: 12, offset: 2}">
          <el-pagination
            background
            hide-on-single-page
            layout="pager"
            :total="newsNum"
            :page-size="pageSize"
            :pager-count="pagerCount"
            :current-page="pageNum"
            @current-change="handleCurrentChange">
          </el-pagination>
        </el-col>
      </el-footer>
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
import SearchNewsList from "@/components/SearchNewsList"
import communication from "@/utils/communication"
import cookie from "@/utils/cookie"
import LoginDialog from "@/components/LoginDialog"
import 'element-ui/lib/theme-chalk/display.css';
var throttle = require("lodash/throttle")
var debounce = require("lodash/debounce")
export default {
  name: 'Search',
  components: {
    SearchHeader,
    LoginDialog,
    SearchNewsList
  },
  data() {
    return {
      keyword: "",

      curTop: 0,
      approaches: [["relativity", "time"], ["tencent", "sina"], [[], [], [], [], [], []]],
      approachNames: [["按相关度排序", "按时间排序"], ["腾讯", "新浪"], ["时间不限", "一天内", "一周内", "一月内", "一年内"]],
      activeValue_0: "relativity",
      activeValue_1: [],
      activeIndex_2: 0,
      approachName_2: "",
      startValue: new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate()),
      endValue: new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate()),
      startTime: new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate()),
      endTime: new Date(),

      error_info: "",
      newsNum: 0,
      newsList: [],

      pageNum: 1,
      pageSize: 10,
      pagerCount: this.getPagerCount(),
      
      dialogVisible: false,
      state:{
        username:"",
        password:""
      }
    }
  },
  created() {
    this.getParams()
  },
  mounted() {
    this.$nextTick(() => {
      this.respondInner()
    })
    window.addEventListener('resize', this.respond)
    window.addEventListener('scroll', this.handleScroll)
  },
  updated(){
    this.$nextTick(() => {
      this.adaptPagination()
    })
  },
  beforeDestroy () {
    window.removeEventListener('resize', this.respond)
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods:{
    respond: debounce(function(){
        this.respondInner()
      }, 100),
    respondInner(){
      let height = document.getElementsByClassName("el-header")[0].clientHeight;
      document.getElementsByClassName("el-main")[0].style["marginTop"] = height + "px";
      this.pagerCount = this.getPagerCount()
    },
    getPagerCount(){
      if (document.documentElement.clientWidth <= 375){
        return 5;
      }
      else{
        return 7;
      }
    },
    getParams(){
      if (Object.prototype.hasOwnProperty.call(this.$route.query, "kd")){
        this.keyword = this.$route.query.kd
        this.pageNum=parseInt(this.$route.query.pn)
        this.sendSearch()
      }
      else{
        this.$router.push({name:'Home'})
      }
    },
    sendSearch: throttle(function(){
      if (this.keyword == ""){
        this.$router.push({name:'Home'})
      }
      else{
        let params = {
          "start": (this.pageNum-1) * this.pageSize,
          "keyword": this.keyword,
          "size": this.pageSize,
          "approach": this.activeValue_0
        }
        if (this.activeValue_1.length > 0){
          params.site = this.activeValue_1.join(" ")
        }
        if (this.activeIndex_2 != 0){
          params.timestart = this.approaches[2][this.activeIndex_2][0]
          params.timeend = this.approaches[2][this.activeIndex_2][1]
        }
        communication.send_search(params, this.callback)
      }
    }, 1000),
    callback(success, data){
      if (success){
        this.error_info=""
        this.newsNum=data["newsnum"]
        this.newsList=data["data"].slice(0, this.pageSize)
        if (!Object.prototype.hasOwnProperty.call(data, "username")){
          cookie.delete_cookie("username")
          cookie.delete_cookie("password")
        }
      }
      else{
        this.error_info = data
      }
    },

    handleScroll: debounce(function(){
        // 兼容Edge, Chrome浏览器
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop
        if (scrollTop > 0){
          document.getElementsByClassName("el-header")[0].style["box-shadow"]= "0 2px 10px 0 rgba(0,0,0,.1)";
        }
        else{
          document.getElementsByClassName("el-header")[0].style["box-shadow"] = ""
        }
      }, 500),

    getNewsNum(){
      var newsNumStr = this.newsNum.toString();
      var zeros = parseInt((newsNumStr.length - 1) / 3);
      if (zeros <= 0){
        return this.newsNum;
      }
      return "约" + newsNumStr.slice(0, newsNumStr.length - zeros * 3) + new Array(zeros).fill(",000").join("");
    },
    handleCommand(index) {
      let oldName_2 = this.activeName_2()
      if (index >= 0 && index < 5){
        let now = new Date()
        if (index == 1){
          this.approaches[2][1] = [now.getTime() - 24 * 60 * 60 * 1000, now.getTime()]
        }
        else if (index == 2){
          this.approaches[2][2] = [now.getTime() - 7 * 24 * 60 * 60 * 1000, now.getTime()]
        }
        else if (index == 3){
          this.approaches[2][3] = [new Date(now.getFullYear(), now.getMonth() - 1, now.getDate()).getTime(), now.getTime()]
        }
        else if (index == 4){
          this.approaches[2][4] = [new Date(now.getFullYear() - 1, now.getMonth(), now.getDate()).getTime(), now.getTime()]
        }
      }
      else{
        this.approaches[2][5] = [this.startTime.getTime(), this.endTime.getTime()]
        this.approachName_2 = this.startTime.getFullYear() + "-" + (this.startTime.getMonth() + 1) + "-" + this.startTime.getDate() + "至" + this.endTime.getFullYear() + "-" + (this.endTime.getMonth() + 1) + "-" + this.endTime.getDate()
      }
      if (index != this.activeIndex_2){
        this.activeIndex_2 = index
      }
      if (this.activeName_2() != oldName_2){
        this.sendSearch()
      }
    },
    activeName_2(){
      if (this.activeIndex_2 >= 0 && this.activeIndex_2 < 5){
        return this.approachNames[2][this.activeIndex_2]
      }
      return this.approachName_2
    },
    handleDateChange(){
      this.$refs.dropdown_3.show()
    },
    handleDateConfirm(){
      this.handleCommand(5)
      this.$refs.dropdown_3.hide()
    },
    disabledEndValue(date){
      return date > new Date() || date < this.startValue;
    },
    disabledStartValue(date){
      return date > new Date() || date > this.endValue;
    },
    removeApproach(){
      this.curTop = 0
      this.activeValue_0 = "relativity"
      this.activeValue_1 = []
      this.activeIndex_2 = 0
      this.startValue = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate())
      this.endValue = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate())
      this.sendSearch()
    },

    adaptPagination(){
      if (this.newsNum > this.pageSize){
        if (document.getElementsByClassName("btn-quickprev").length > 0){
          document.getElementsByClassName("number")[0].style["display"] = "none";
        }
        else{
          document.getElementsByClassName("number")[0].style["display"] = "";
        }
        if (document.getElementsByClassName("btn-quicknext").length > 0){
          document.getElementsByClassName("number")[this.pagerCount - 1].style["display"] = "none";
        }
        else{
          document.getElementsByClassName("number")[this.pagerCount - 1].style["display"] = "";
        }
      }
    },
    handleCurrentChange(val) {
      this.$router.push({    
        name: 'Search',  
        query: {   
          "kd": this.keyword,
          "pn": val
        }   
      }) 
    },

    login_success(){
      this.dialogVisible=false
      location.reload()
    }
  },
  watch: {
    $route: 'getParams',
    keyword(k){
      document.title = "Spect资讯搜索_" + k
    },
    newsList(list){
      for (let i = 0; i < list.length; i++) {
        var content_index = list[i].content.indexOf('<span style="color:red;">')
        if (content_index > 30){
          this.newsList[i].content = list[i].content.slice(content_index - 30)
        } 
      }
    },
    startValue(v){
      this.startTime.setTime(v.getTime())
    },
    endValue(v){
      this.endTime.setTime(v.getTime() + 24 * 60 * 60 * 1000 - 1)
    }
  }
};
</script>

<style>
  #search-page{
    font-size: 0.18rem;
  }
  #search-page .el-header{
    background-color: white; 
    padding-top: 0.15rem;
    padding-bottom: 0.1rem;
  }
  #search-page .isFixed{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
  }

  #search-page .news-main{
    text-align: left; 
  }
  #search-page .news-top{
    margin-top: -0.2rem;
    font-size: 0.13rem; 
    margin-bottom: 0.06rem;
  }
  #search-page .news-top__approach{
    margin-top: -0.25rem;
    font-size: 0.13rem; 
    margin-bottom: 0.15rem;
  }
  #search-page .news-num{
    color: #b8b8b8; 
  }
  #search-page .search-tool{
    cursor: pointer; 
    float: right; 
    margin-top: 0.13rem;
  }
  .fade-enter-active, .fade-leave-active {
    transition: opacity .3s ease;
  }
  .fade-enter, .fade-leave-to{
    opacity: 0;
  }
  #search-page .dropdown-menues{
    margin-top: 0.13rem; 
    float: left; 
    margin-right: 0.24rem;
  }
  .select-approach .el-input{
    width: 1.08rem !important;
    font-size: 0.12rem !important;
  }
  .select-site .el-input{
    width: 1.3rem !important;
    font-size: 0.12rem !important;
  }
  .el-select__tags .el-tag{
    font-size: 0.12rem !important;
    padding: 0 0.04rem;
    height: 0.2rem !important;
    line-height: 0.2rem !important;
  }
  .el-select__tags .el-tag .el-tag__close{
    right: -2px !important;
  }
  #search-page .el-select .el-input__suffix{
    right: 0.02rem;
    height: 0.26rem;
  }
  .search-dropdown-menu .search-dropdown-item, .el-select-dropdown__item{
    padding: 0.1rem 0.13rem !important;
    font-size: 0.13rem !important;
    line-height: 0.13rem !important;
  }
  .search-dropdown-menu .dropdown-notitem{
    font-size: 0.13rem; 
    padding: 0 0.13rem; 
    line-height: 0.13rem;
  }
  .search-dropdown-menu .el-divider--horizontal{
    margin: 0;
  }
  .search-dropdown-menu .el-button{
    padding: 0.06rem 0.12rem;
    font-size: 0.13rem;
  }
  .el-date-editor.el-input{
    width: 0.8rem !important;
    margin-left: 0.05rem !important;
  }
  .el-input--prefix .el-input__inner, .el-select .el-input__inner{
    padding: 0 0.05rem !important;
    height: 0.26rem !important;
    line-height: 0.26rem !important;
    font-size: 0.12rem !important; 
  }
  .el-input--prefix .el-input__prefix{
    display: none;
  }

  #search-page .el-pagination li {
    font-size: 0.16rem !important;
    margin-left: 0.06rem !important;
    margin-right: 0.06rem !important;
    min-width: 0.4rem !important;
    min-height: 0.4rem !important;
    line-height: 0.4rem !important;
    border-radius: 0.08rem !important;
  }
</style>