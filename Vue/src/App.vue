<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style>
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    padding: 0;
    margin: 0;
  }  
  body { margin: 0; }
  html { font-size:100px; }
  @media(max-width:540px){ html { font-size:90px; } }   /*Android常用宽度*/
  @media(max-width:480px){ html { font-size:80px; } }		    /*Android常用宽度*/
  /*@media(max-width:414px){ html { font-size:64.69px; } }    /*i6Plus,i7Plus宽度*/  
  /*@media(max-width:375px){ html { font-size:58.59px; } }	  /*i6,i7宽度*/
  /*@media(max-width:360px){ html { font-size:56.25px; } }	  /*Android常用宽度*/
  /*@media(max-width:320px){ html { font-size:50px; } }		    /*i5宽度*/
</style>
