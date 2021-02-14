import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'
import API from "@/utils/API";
import cookie from "@/utils/cookie";
import newsList from "./news"

let mock = new MockAdapter(axios)

mock.onPost(API.LOGIN.path).reply((config) => {
  // 解析axios传过来的数据
  let content = config.data.split("&")
  let username = content[0].split("=")[1]
  let password = content[1].split("=")[1]
  return new Promise((resolve) => {
    if (username == "admin" && password == "admin"){
      resolve([200, {data: ""}])
    }
    else{
      resolve([400, {data: "输入不能为空"}])
    }
  })
});

mock.onPost(API.REGISTER.path).reply((config) => {
  // 解析axios传过来的数据
  let content = config.data.split("&")
  let username = content[0].split("=")[1]
  return new Promise((resolve) => {
    if (username != "admin"){
      resolve([200, {data: ""}])
    }
    else{
      resolve([400, {data: "用户名已存在"}])
    }
  })
});

mock.onPost(API.USER_UPDATE.path).reply((content) => {
  let password = content.data.split("=")[1]
  return new Promise((resolve) => {
    if (password != "666666"){
      resolve([200, {data: ""}])
    }
    else{
      resolve([400, {data: "密码格式错误"}])
    }
  })
});

mock.onPost(API.SEND_EMAIL.path).reply((content) => {
  let email = content.data.split("=")[1]
  return new Promise((resolve) => {
    if (email == "12345678%40qq.com"){
      resolve([200, {data: ""}])
    }
    else{
      resolve([400, {data: "Undefined Interface"}])
    }
  })
});

mock.onGet(API.SEARCH.path).reply(() => {
  return new Promise((resolve) => {
    let data = {
      newsnum: 20,
      data: newsList
    }
    if (cookie.get_cookie("username") == "admin" && cookie.get_cookie("password") == "admin"){
      data.username = "admin"
    }
    resolve([200, data])
  })
});
 
mock.onGet(API.HOME.path).reply(() => {
  return new Promise((resolve) => {
    let data = {
      newsnum: 20,
      data: newsList
    }
    if (cookie.get_cookie("username") == "admin" && cookie.get_cookie("password") == "admin"){
      data.username = "admin"
    }
    resolve([200, data])
  })
});

let tags = {"data":[{
  "tag": "你好",
  "num": 100,
  "lasttime": new Date().getTime()
},
{
  "tag": "你不好",
  "num": 10,
  "lasttime": new Date().getTime()
},
{
  "tag": "你很好",
  "num": 1,
  "lasttime": new Date().getTime()
}]}

mock.onGet(API.GET_INFO.path).reply(() => {
  let tagstr = ""
  for(let i = 0; i < tags["data"].length; i ++){
    let tag = tags["data"][i]
    tagstr += tag['tag'] + "," + tag['num'] + "," + tag['lasttime'] + ";"
  }
  return new Promise((resolve) => {
    resolve([200, {
      email: "12345678@qq.com",
      tags: tagstr
    }])
  })
});

mock.onPost(API.SET_TAGS.path).reply((content) => {
  tags = content.data
  return new Promise((resolve) => {
    resolve([200, {data: ""}])
  })
});
 