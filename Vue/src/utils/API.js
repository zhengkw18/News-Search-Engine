const API={
    LOGIN:{
        path:"/api/login/",
        method: "post",
        contentType: 'application/x-www-form-urlencoded'
    },
    REGISTER:{
        path:"/api/register/",
        method: "post",
        contentType: 'application/x-www-form-urlencoded'
    },
    USER_UPDATE:{
        path:"/api/update/",
        method: "post",
        contentType: 'application/x-www-form-urlencoded'
    },
    SEARCH:{
        path:"/api/search/",
        method: "get"
    },
    HOME:{
        path:"/api/news/",
        method: "get"
    },
    GET_INFO:{
        path:"/api/getinfo/",
        method: "get"
    },
    SET_TAGS:{
        path:"/api/settags/",
        method: "post"
    },
    SEND_EMAIL:{
        path:"/api/email/",
        method: "post",
        contentType: 'application/x-www-form-urlencoded'
    },
    SEARCH_RELATED:{
        path:"/baidu/sug/",
        method: "get"
    },
    TODAY_NEWS:{
        path:"/tencent/trpc.qqnews_web.pc_base_srv.base_http_proxy/NinjaPageContentSync",
        method: "get"
    },
    SINA_NEWS:{
        path:"/sina/ws/GetTopDataList.php",
        method: "get"
    }
}

export default API