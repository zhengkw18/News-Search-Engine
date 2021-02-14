<template>
  <div style="text-align: left;" id="user-tags">
    <el-tag
      v-for="(el, index) in tagList.slice(0, 20)"
      :key="index"
      closable
      :type="type(el.num)"
      @close="handleClose(el.tag)">
      {{ el.tag }}
    </el-tag>
    <el-popconfirm
      title="删除所有标签？"
      v-if="tagList.length > 0"
      @onConfirm="removeTags()"
    >
      <el-button slot="reference" class="button-remove-tags" type="info" plain icon="el-icon-delete">删除</el-button>
    </el-popconfirm>
  </div>
</template>

<script>
import cookie from "@/utils/cookie"
import communication from "@/utils/communication"
import newsLogic from "@/utils/newsLogic"
export default {
  name: "UserTags",
  created(){
    if (cookie.get_cookie("username") == ""){
      this.$router.push({name: "Home"})
    }
  },
  mounted(){
    this.loadTagList()
  },
  data(){
    return{
      tagList: []
    }
  },
  methods: {
    loadTagList(){
      communication.get_info(this.getTags);  
    },
    getTags(success, data){
      if (success){
        this.tagList = newsLogic.convertTags(data.tags) 
      }   
    },
    type(num){
      if (num >= 10 && num < 100){
        return "warning"
      }
      else if(num >= 100){
        return "danger"
      }
      else{
        return ""
      }
    },
    handleClose(tag){
      communication.update_tags(this.deleteTag, tag)
    },
    deleteTag(data, tag){
      this.tagList = newsLogic.convertTags(data.tags)
      let index = this.tagList.findIndex((el) => {
        return el.tag == tag
      })
      if (index >= 0){
        this.tagList.splice(index, 1)
        communication.set_tags(this.tagList)
      }
    },
    removeTags(){
      this.tagList = []
      communication.set_tags([])
    }
  }
}
</script>

<style>
  #user-tags .el-tag{
    font-size: 0.14rem !important;
    margin: 0.14rem 0.1rem;
  }
  #user-tags .button-remove-tags{
    margin: 0.14rem 0.1rem !important;
    height: 32px !important;
    line-height: 30px !important;
    padding: 0 10px !important;
    font-size: 0.14rem !important;
    border-width: 1px !important;
    border-radius: 4px !important;
    border-style: solid !important;
  }
</style>