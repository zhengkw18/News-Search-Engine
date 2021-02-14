<template>
<el-dialog
  style="text-align: center;"
  :visible.sync="dialogVisible"
  :close-on-click-modal="false"
  width="3.5rem"
  id="auth-code"
  @close="close">
  <el-row>
    <el-col :span="10">
      <el-input placeholder="请输入验证码" v-model="check" autocomplete="off"></el-input>
    </el-col>
    <el-col :span="12" :offset="2">
      <div class="code" @click="refreshCode">
        <SIdentify :identifyCode="identifyCode"
          :contentWidth="125"
          :contentHeight="38"/>
      </div>
    </el-col>
    <div class="form-item__tip" v-show="isError">
      验证码错误
    </div>
  </el-row>
</el-dialog>
</template>

<script>
import SIdentify from '@/components/SIdentify'
export default {
  name: "AuthCode",
  components: {
    SIdentify
  },
  props: {
    dialogVisible: {
      type: Boolean,
      default: () => true
    }
  },
  data() {
    return {
      identifyCodes: '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ',
      identifyCode: "",
      check: "",
      isError: false
    };
  },
  mounted() {
    this.refreshCode()
  },
  methods: {
    randomNum(min, max) {
      return Math.floor(Math.random() * (max - min) + min);
    },
    refreshCode() {
      this.makeCode(4);
    },
    makeCode(len) {
      this.identifyCode = "";
      for (let i = 0; i < len; i++) {
        this.identifyCode += this.identifyCodes[
          this.randomNum(0, this.identifyCodes.length)
        ];
      }
    },
    close(){
      this.$emit('hide')
    },
    success(){
      this.$emit('success')
    }
  },
  watch: {
    check:{
      handler(){
        if (this.check.length >= this.identifyCode.length){
          if (this.check == this.identifyCode){
            this.isError = false
            this.success()
          }
          else{
            this.isError = true
            this.refreshCode()
          }
        }
      }
    },
    dialogVisible(visible){
      if (visible){
        this.refreshCode()
      }
    }
  }
};
</script>

<style>
  #auth-code{
    font-size: 15px; 
  }
  #auth-code .el-input{
    font-size: 15px !important;
  }
  #auth-code .el-input__inner{
    padding-left: 11px !important;
    padding-right: 11px !important;
  }
  #auth-code .form-item__tip{
    font-size: 13px;
    line-height: 1;
    padding-top: 4px;
    position: absolute;
    top: 100%;
    left: 0;
    color: red;
  }
  #auth-code .code {
    border: 1px solid;
    width: 125px;
    height: 38px;
    float: right;
  }
</style>