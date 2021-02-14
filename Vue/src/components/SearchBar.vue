<template>
  <div id="search-bar">
    <el-row>
        <el-col :xs="20" :sm="20" :md="20" :lg="21">
          <div style="position: relative;">
            <el-input
              ref="search_input"
              v-model="searchInput"
              @focus="input_focus"
              @blur="isFocus = false"
              @keyup.enter.native="searchHandler">
            </el-input>
            <div v-show="isSearchBox" class="box-line"></div>
            <el-card shadow="never"
              v-show="isSearchBox"
              class="search-box">
              <div v-show="isHistorySearch">
                <el-row v-for="(keyword, index) in historySearchList.slice(0, 9)"
                  v-bind:key="index">
                  <el-col :span="20">
                    <p class="history-item" @mousedown="$event.preventDefault()" @click="searchItem(index)">{{ keyword }}</p>
                  </el-col>
                  <el-col :span="2" :offset="2">
                    <p class="remove-history" @mousedown="$event.preventDefault()" @click="deleteItem(index)">
                      <i class="el-icon-close"></i>
                    </p>
                  </el-col>
                </el-row>
                <el-row>
                  <p class="remove-history" @mousedown="$event.preventDefault()" @click="removeAllHistory">
                    <i class="el-icon-delete"></i> 清空历史记录
                  </p>
                </el-row>
              </div>
              <div v-show="isRelatedSearch">
                <el-row v-for="keyword in relatedSearchList"
                  v-bind:key="keyword.id">
                  <p class="history-item" @mousedown="$event.preventDefault()" @click="searchRelated(keyword)">{{ keyword }}</p>
                </el-row>
              </div>
            </el-card>
          </div>
        </el-col>
        <el-col :xs="4" :sm="4" :md="4" :lg="3">
          <el-button icon="el-icon-search" id="search-button" type="primary" @click="searchHandler">搜索</el-button>
        </el-col>
    </el-row>
  </div>
</template>

<script>
import store from "@/utils/localStore"
import openCommunication from "@/utils/openCommunication"
var debounce = require("lodash/debounce")
var throttle = require("lodash/throttle")
export default {
  name: "SearchBar",
  props: {
    keyword: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      searchInput: this.keyword,
      isFocus: false, //是否聚焦
      historySearchList: [], //历史搜索数据
      relatedSearchList: []
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.respond()
    })
  },
  methods: {
    input_focus() {
      this.isFocus = true;
      let loadHistory = store.loadHistory();
      this.historySearchList = loadHistory == null ? [] : loadHistory;
    },
    respond: throttle(function(){
      let el = this.$el.getElementsByClassName("el-input__inner")[0]
      if (this.isSearchBox){
        el.style["borderWidth"] = "0.02rem 0.02rem 0 0.02rem"
        el.style["borderRadius"] = "0.12rem 0 0 0"
      }
      else{
        el.style["borderWidth"] = "0.02rem 0 0.02rem 0.02rem"
        el.style["borderRadius"] = "0.12rem 0 0 0.12rem"
      }
    }, 100),
    getKeyword(){
      return this.searchInput.replace(/([\s\n\t]+)/g, " ").replace(/(^\s|\s$)/g, "");
    },
    searchHandler() {
      this.$refs.search_input.blur()
      let keyword = this.getKeyword()
      if (keyword == ""){
        this.$router.push({name:'Home'})
      }
      else{
        let index =this.historySearchList.indexOf(keyword)
        if (index >= 0) {
          this.historySearchList.splice(index, 1);
        }
        this.historySearchList.splice(0, 0, keyword);
        store.saveHistory(this.historySearchList);
        this.$router.push({    
          name: 'Search',  
          query: {   
            "kd": this.searchInput,
            "pn": 1
          }   
        }) 
      }
    },
    searchItem(index) {
      this.$refs.search_input.blur()
      let item = this.historySearchList[index];
      this.historySearchList.splice(index, 1);
      if (item == ""){
        store.saveHistory(this.historySearchList);
        this.$router.push({name:'Home'})
      }
      else{
        this.historySearchList.splice(0, 0, item);
        store.saveHistory(this.historySearchList);
        this.searchInput = item;
        this.$router.push({    
          name: 'Search',  
          query: {   
            "kd": item,
            "pn": 1
          }   
        }) 
      }
    },
    deleteItem(index) {
      this.historySearchList.splice(index, 1);
      store.saveHistory(this.historySearchList);
    },
    removeAllHistory() {
      this.historySearchList=[]
      store.removeAllHistory();
    },

    searchRelated(item){
      this.searchInput = item;
      this.searchHandler() 
    },
    sendSearch: debounce(function(){
      if (this.searchInput == ""){
        return
      }
      openCommunication.search_related({
        "wd": this.searchInput,
        "prod": "news"
      }, this.callback)
    }, 500),
    callback(data){
      this.relatedSearchList = data["data"].slice(0, 10)
    }
  },
  computed: {
    isHistorySearch() {
      return this.isFocus && this.searchInput == "" && this.historySearchList.length > 0;
    },
    isRelatedSearch() {
      return this.isFocus && this.searchInput != "" && this.relatedSearchList.length > 0;
    },
    isSearchBox() {
      return this.isHistorySearch || this.isRelatedSearch
    },
  },
  watch: {
    isSearchBox: "respond",
    searchInput: "sendSearch"
  }
};
</script>

<style>
  #search-bar{
    font-size: 0.16rem;
  }
  #search-bar input.el-input__inner { 
    font-size: 0.16rem;
    height: 0.43rem;
    line-height: 0.43rem;
    padding: 0.15rem;
  }
  #search-button {
    border-radius: 0 0.12rem 0.12rem 0;
    font-size: 0.17rem;
    min-width: 100%;
    height: 0.43rem;
    padding: 0.13rem 1vw;
  }

  #search-bar .box-line{
    position: absolute;
    left: 0.15rem;
    right: 0.15rem;
    height: 2px;
    background-color: #E4E7ED;
    z-index: 30;
    margin-top: -2px;
  }
  #search-bar .search-box {
    height: fit-content;
    position: absolute;
    left: 0;
    right: 0;
    z-index: 15;
    font-size: 0.16rem;
    border-width: 0 0.02rem 0.02rem 0.02rem;
    border-radius: 0 0 0.12rem 0.12rem;
    border-color: #409EFF;
    text-align: left;
  }
  #search-bar .el-card__body{
    padding: 0.1rem 0.15rem 0.05rem 0.15rem;
  }
  #search-bar .search-box p:hover{
    color: #2d6df8;
  }
  #search-bar .search-box p{
    color: #b8b8b8;
  }

  #search-bar .history-item {
    cursor: pointer; 
    margin-top: 0;
    margin-bottom: 0.1rem;
    display: -webkit-box; 
    -webkit-box-orient: vertical; 
    -webkit-line-clamp: 1; 
    overflow: hidden;
  }
  #search-bar .remove-history {
    float: right;
    margin-top: 0;
    margin-bottom: 0.1rem;
    cursor: pointer;
  }
</style>