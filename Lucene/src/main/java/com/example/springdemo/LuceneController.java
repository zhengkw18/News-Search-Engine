package com.example.springdemo;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.apache.lucene.search.highlight.InvalidTokenOffsetsException;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.sql.Timestamp;

/**
 * 测试控制器
 */
@RestController
public class LuceneController {
    private final QueryNews queryNews = new QueryNews();

    @GetMapping("/get")
    public JSONObject searhNews(String keyword, String start, String size, String approach,
                                Timestamp timestart, Timestamp timeend, String hrefcontains, String channel)
            throws InvalidTokenOffsetsException, IOException {
        return queryNews.searchNews(keyword,start,size,approach,timestart,timeend,hrefcontains,channel);
    }

    @GetMapping("/tags")
    public JSONObject searchTags(String tags, String start, String size, Timestamp timestart, Timestamp timeend) throws IOException {
        return queryNews.searchTags(tags,start,size,timestart,timeend);
    }
}