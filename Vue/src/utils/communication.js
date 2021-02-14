/**
 * 如果需要修改为正常上线模式，请注释下面mock的import代码
 * **/
//import "@/mock/index"
import API from "@/utils/API";
import axios from 'axios';
import qs from 'qs';

axios.defaults.withCredentials = true;

const communication = {
    send_login: function(message, callback){
        axios({
                url: API.LOGIN.path,
                method:API.LOGIN.method,
                data: qs.stringify(message),
                responseType:"text",
                contentType: API.LOGIN.contentType
            })
            .then(function () {
                callback(true, "");
            })
            .catch(function (error) {
                console.log(error)
                if (error.response){
                    callback(false, error.response.data.data);
                }
        });
    },
    send_register: function(message, callback){
        axios({
                url: API.REGISTER.path,
                method: API.REGISTER.method,
                data: qs.stringify(message),
                responseType:"text",
                contentType: API.REGISTER.contentType
            })
            .then(function () {
                callback(true, "");
            })
            .catch(function (error) {
                console.log(error)
                if (error.response){
                    callback(false, error.response.data.data);
                }
        });
    },
    send_user_update: function(message, callback){
        axios({
                url: API.USER_UPDATE.path,
                method: API.USER_UPDATE.method,
                data: qs.stringify(message),
                responseType:"text",
                contentType: API.USER_UPDATE.contentType
            })
            .then(function () {
                callback(true, "");
            })
            .catch(function (error) {
                console.log(error)
                if (error.response){
                    callback(false, error.response.data.data);
                }
        });
    },
    send_search: function(message, callback){
        axios({
                url: API.SEARCH.path,
                method:API.SEARCH.method,
                params: message,
                responseType:"text"
            })
            .then(function (response) {
                callback(true, response.data);
            })
            .catch(function (error) {
                console.log(error)
                if (error.response){
                    callback(false, error.response.data.data);
                }
        });
    },
    send_home: function(message, callback){
        axios({
                url: API.HOME.path,
                method:API.HOME.method,
                params: message,
                responseType:"text"
            })
            .then(function (response) {
                callback(true, response.data);
            })
            .catch(function (error) {
                console.log(error)
                if (error.response){
                    callback(false, error.response.data.data);
                }
        });
    },
    set_tags: function(message){
        axios({
                url: API.SET_TAGS.path,
                method: API.SET_TAGS.method,
                data: {
                    "data": message.slice(0, 200)
                },
                responseType:"text"
            })
            .catch(function (error) {
                console.log(error)
        });
    },
    get_info: function(callback){
        axios({
                url: API.GET_INFO.path,
                method:API.GET_INFO.method,
                responseType:"text"
            })
            .then(function (response) {
                callback(true, response.data);
            })
            .catch(function (error) {
                console.log(error)
                if (error.response){
                    callback(false, error.response.data.data);
                }
        });
    },
    update_tags: function(callback, tags){
        axios({
                url: API.GET_INFO.path,
                method:API.GET_INFO.method,
                responseType:"text"
            })
            .then(function (response) {
                callback(response.data, tags);
            })
            .catch(function (error) {
                console.log(error)
        });
    },
    send_email: function(message, callback){
        axios({
                url: API.SEND_EMAIL.path,
                method: API.SEND_EMAIL.method,
                data: qs.stringify(message),
                responseType:"text",
                contentType: API.SEND_EMAIL.contentType
            })
            .then(function () {
                callback(true, "");
            })
            .catch(function (error) {
                console.log(error)
                if (error.response){
                    callback(false, error.response.data.data);
                }
        });
    },
}
export default communication
