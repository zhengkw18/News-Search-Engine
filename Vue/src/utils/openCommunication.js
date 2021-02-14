import API from "@/utils/API";
import axios from 'axios';

const openCommunication = {
    search_related: function(message, callback){
        axios({
                url: API.SEARCH_RELATED.path,
                method: API.SEARCH_RELATED.method,
                params: message
            })
            .then(function (response) {
                callback(response.data);
            })
            .catch(function (error) {
                console.log(error)
        });
    },
    get_today_news: function(message, callback){
        axios({
                url: API.TODAY_NEWS.path,
                method: API.TODAY_NEWS.method,
                params: message
            })
            .then(function (response) {
                callback(response.data);
            })
            .catch(function (error) {
                console.log(error)
        });
    },
    get_sina_news: function(message, callback){
        axios({
                url: API.SINA_NEWS.path,
                method: API.SINA_NEWS.method,
                params: message
            })
            .then(function (response) {
                callback(response.data);
            })
            .catch(function (error) {
                console.log(error)
        });
    }
}
export default openCommunication