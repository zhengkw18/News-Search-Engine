package com.example.springdemo;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.Term;
import org.apache.lucene.search.*;
import org.apache.lucene.search.highlight.*;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.wltea.analyzer.lucene.IKAnalyzer;

import java.io.File;
import java.io.IOException;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.*;

public class QueryNews {
    public JSONObject searchNews(String key, String start, String size,String approach,
                                 Timestamp timestart, Timestamp timeend, String hrefcontains, String channel)
            throws IOException, InvalidTokenOffsetsException {
        JSONArray newsarray = new JSONArray();
        JSONObject result = new JSONObject();

        //格式化时间表示，设置时区为上海
        TimeZone shanghai = TimeZone.getTimeZone("Asia/Shanghai");
        SimpleDateFormat timeFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        timeFormat.setTimeZone(shanghai);

        //打印日志
        Logger logger = LoggerFactory.getLogger("INFO");
        logger.info("request:GET,/get key={}",key);

        // 创建IndexSearcher
        // 指定索引库的地址
        int pageStart = Integer.parseInt(start);
        int pageSize = Integer.parseInt(size);
        Directory directory = FSDirectory.open(new File("indexsource"));
        IndexReader reader = DirectoryReader.open(directory);
        IndexSearcher searcher = new IndexSearcher(reader);

        String regex = "[ `~!@#$^&*()=|{}':;,\\\\[\\\\].<>/?！￥…（）—【】‘；：”“。，、？]+";
        String[] keyfrompun = key.split(regex);
        boolean flag = false;
        for(String i:keyfrompun) {
            if (i.length() > 8) {
                flag = true;
                break;
            }
        }

        // 搜索关键词分词和href，channel域区分空格间词
        IKAnalyzer ikAnalyzer = new IKAnalyzer();
        List<String> keywords = new ArrayList<>();
        TokenStream tk = ikAnalyzer.tokenStream("",key);
        tk.reset();
        CharTermAttribute term = tk.getAttribute(CharTermAttribute.class);
        while(tk.incrementToken()){
            if(flag && term.toString().length() < 2) continue;
            keywords.add(term.toString());
        }
        tk.close();

        //总query对象，表示所有搜索条件之间的关系
        BooleanQuery query = new BooleanQuery();
        for(String keyword: keywords){
            query.add(new TermQuery(new Term("title",keyword)), BooleanClause.Occur.SHOULD);
            query.add(new TermQuery(new Term("content",keyword)), BooleanClause.Occur.SHOULD);
        }

        BooleanQuery bfilter = new BooleanQuery();
        //时间过滤
        if(timestart != null && timeend != null) {
            Calendar cal = Calendar.getInstance();
            cal.setTime(timestart);
            cal.add(Calendar.HOUR_OF_DAY, -8);
            timestart = new Timestamp(cal.getTime().getTime());
            cal.setTime(timeend);
            cal.add(Calendar.HOUR_OF_DAY, -8);
            timeend = new Timestamp(cal.getTime().getTime());
            bfilter.add(NumericRangeQuery.newLongRange("time", timestart.getTime(), timeend.getTime(),
                    true, true), BooleanClause.Occur.MUST);
        }
        else{
            if(timestart != null) {
                Calendar cal = Calendar.getInstance();
                cal.setTime(timestart);
                cal.add(Calendar.HOUR_OF_DAY, -8);
                timestart = new Timestamp(cal.getTime().getTime());
                bfilter.add(NumericRangeQuery.newLongRange("time", timestart.getTime(), Long.MAX_VALUE,
                        true, true), BooleanClause.Occur.MUST);
            }
            if(timeend != null) {
                Calendar cal = Calendar.getInstance();
                cal.setTime(timeend);
                cal.add(Calendar.HOUR_OF_DAY, -8);
                timeend = new Timestamp(cal.getTime().getTime());
                bfilter.add(NumericRangeQuery.newLongRange("time", Long.MIN_VALUE, timeend.getTime(),
                        true, true), BooleanClause.Occur.MUST);
            }
        }
        // href过滤
        BooleanQuery hrefquery;
        if(hrefcontains != null){
            hrefquery = new BooleanQuery();
            String[] hrefkeys = hrefcontains.split(" ");
            for(String hrefkey: hrefkeys)
                hrefquery.add(new TermQuery(new Term("href",hrefkey)),BooleanClause.Occur.SHOULD);
            bfilter.add(hrefquery, BooleanClause.Occur.MUST);
        }
        // channel过滤
        BooleanQuery channelquery;
        if(channel != null) {
            channelquery = new BooleanQuery();
            String[] channelkeys = channel.split(" ");
            for(String channelkey:channelkeys)
                channelquery.add(new TermQuery(new Term("channel", channelkey)), BooleanClause.Occur.SHOULD);
            bfilter.add(channelquery, BooleanClause.Occur.MUST);
        }
        Filter filter = new QueryWrapperFilter(bfilter);

        
        int end = Math.min((pageStart +pageSize), 100000);
        // 通过searcher来搜索索引库
        // 第二个参数：指定需要显示的顶部记录的N条
        // 第三个参数：排序方式，默认按相关度
        long startTime = System.currentTimeMillis();
        TopDocs topDocs;
        if(channel != null || hrefcontains != null || timestart != null || timeend != null) {
            if (approach.equals("time"))
                topDocs = searcher.search(query, filter, end, new Sort(new SortField("time", SortField.Type.LONG, true)));
            else
                topDocs = searcher.search(query, filter, end);
        } else {
            if (approach.equals("time"))
                topDocs = searcher.search(query, end, new Sort(new SortField("time", SortField.Type.LONG, true)));
            else
                topDocs = searcher.search(query, end);
        }
        // 根据查询条件匹配出的记录总数
        int count = topDocs.totalHits;
        int newsnum = Math.min(count,100000);
        end = Math.min(end,count);

        // 根据查询条件匹配出的记录
        ScoreDoc[] scoreDocs = topDocs.scoreDocs;
        long endTime = System.currentTimeMillis();
        logger.info("搜索索引所用时间：{} s",(endTime - startTime) / 1000.0);

        Highlighter highlighter = new Highlighter(new SimpleHTMLFormatter
                ("<span style=\"color:red;\">", "</span>"),   //高亮格式
                new QueryScorer(query));
        highlighter.setTextFragmenter(new SimpleFragmenter(50000));//高亮后的段落范围

        startTime = System.currentTimeMillis();
        for (int i = pageStart; i<end; i++) {
            // 获取文档的ID
            int docId = scoreDocs[i].doc;
            // 通过ID获取文档
            Document doc = searcher.doc(docId);
            //将新闻存入list中
            JSONObject jsnews = new JSONObject();
            String title = (highlighter.getBestFragment(ikAnalyzer,"title",doc.get("title")) != null)
                    ? highlighter.getBestFragment(ikAnalyzer,"title",doc.get("title")) :
                    doc.get("title");
            String content = (highlighter.getBestFragment(ikAnalyzer,"content",doc.get("content")) != null)
                    ? highlighter.getBestFragment(ikAnalyzer,"content",doc.get("content")) :
                    doc.get("content");

            jsnews.put("title",title);
            jsnews.put("content",content);
            jsnews.put("image",doc.get("image"));
            jsnews.put("source",doc.get("source"));
            jsnews.put("href",doc.get("href"));
            jsnews.put("channel",doc.get("channel"));
            jsnews.put("tags",doc.get("tags"));

            Timestamp timestamp = new Timestamp(Long.parseLong(doc.get("time")));
            String time = timeFormat.format(timestamp);
            jsnews.put("time",time);

            jsnews.put("id",doc.get("id"));
            newsarray.add(jsnews);
        }
        endTime = System.currentTimeMillis();
        logger.info("获取数据所用时间：{} s",(endTime - startTime) / 1000.0);

        // 关闭资源
        reader.close();

        result.put("data",newsarray);
        result.put("newsnum",newsnum);
        return result;
    }

    public JSONObject searchTags(String tags, String start, String size, Timestamp timestart, Timestamp timeend)
            throws IOException{
        //格式化时间表示，设置时区为上海
        TimeZone shanghai = TimeZone.getTimeZone("Asia/Shanghai");
        SimpleDateFormat timeFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        timeFormat.setTimeZone(shanghai);

        //打印日志
        Logger logger = LoggerFactory.getLogger("INFO");
        logger.info("request:GET,/tags tags={}",tags);

        // 创建IndexSearcher
        // 指定索引库的地址
        int pageStart = Integer.parseInt(start);
        int pageSize = Integer.parseInt(size);
        Directory directory = FSDirectory.open(new File("indexsource"));
        IndexReader reader = DirectoryReader.open(directory);
        IndexSearcher searcher = new IndexSearcher(reader);

        // 搜索关键词分词和href，channel域区分空格间词
        IKAnalyzer ikAnalyzer = new IKAnalyzer();

        // 分析tags获取每个关键词和对应权值
        Map<String,Float> tagsmap = new HashMap<>();
        String[] tagsarray = tags.split(";");
        for(String tag: tagsarray){
            String[] nameweight = tag.split(",");

            List<String> keywords = new ArrayList<>();
            TokenStream tk = ikAnalyzer.tokenStream("",nameweight[0]);
            tk.reset();
            CharTermAttribute term = tk.getAttribute(CharTermAttribute.class);
            while(tk.incrementToken()){
                keywords.add(term.toString());
            }
            tk.close();

            for(String key: keywords){
                tagsmap.put(key,Float.parseFloat(nameweight[1]));
            }
        }

        //总query对象，表示所有搜索条件之间的关系
        BooleanQuery query = new BooleanQuery();
        for(Map.Entry<String,Float> key: tagsmap.entrySet()){
            TermQuery termQuery = new TermQuery(new Term("tags",key.getKey()));
            termQuery.setBoost(key.getValue());
            query.add(termQuery, BooleanClause.Occur.SHOULD);
        }

        BooleanQuery bfilter = new BooleanQuery();
        //时间过滤
        if(timestart != null && timeend != null) {
            Calendar cal = Calendar.getInstance();
            cal.setTime(timestart);
            cal.add(Calendar.HOUR_OF_DAY, -8);
            timestart = new Timestamp(cal.getTime().getTime());
            cal.setTime(timeend);
            cal.add(Calendar.HOUR_OF_DAY, -8);
            timeend = new Timestamp(cal.getTime().getTime());
            bfilter.add(NumericRangeQuery.newLongRange("time", timestart.getTime(), timeend.getTime(),
                    true, true), BooleanClause.Occur.MUST);
        }
        else{
            if(timestart != null) {
                Calendar cal = Calendar.getInstance();
                cal.setTime(timestart);
                cal.add(Calendar.HOUR_OF_DAY, -8);
                timestart = new Timestamp(cal.getTime().getTime());
                bfilter.add(NumericRangeQuery.newLongRange("time", timestart.getTime(), Long.MAX_VALUE,
                        true, true), BooleanClause.Occur.MUST);
            }
            if(timeend != null) {
                Calendar cal = Calendar.getInstance();
                cal.setTime(timeend);
                cal.add(Calendar.HOUR_OF_DAY, -8);
                timeend = new Timestamp(cal.getTime().getTime());
                bfilter.add(NumericRangeQuery.newLongRange("time", Long.MIN_VALUE, timeend.getTime(),
                        true, true), BooleanClause.Occur.MUST);
            }
        }
        Filter filter = new QueryWrapperFilter(bfilter);

        int end = Math.min((pageStart +pageSize), 10000);
        // 通过searcher来搜索索引库
        // 第二个参数：指定需要显示的顶部记录的N条
        // 第三个参数：排序方式，默认按相关度
        TopDocs topDocs;
        if(timestart != null || timeend != null)
            topDocs = searcher.search(query, filter, end);
        else
            topDocs = searcher.search(query,end);
        // 根据查询条件匹配出的记录总数
        int count = topDocs.totalHits;
        end = Math.min(end,count);

        // 根据查询条件匹配出的记录
        ScoreDoc[] scoreDocs = topDocs.scoreDocs;

        JSONArray newsarray = new JSONArray();
        for (int i = pageStart; i<end; i++) {
            // 获取文档的ID
            int docId = scoreDocs[i].doc;
            // 通过ID获取文档
            Document doc = searcher.doc(docId);

            //将新闻存入list中
            JSONObject jsnews = new JSONObject();

            jsnews.put("title",doc.get("title"));
            jsnews.put("content",doc.get("content"));
            jsnews.put("image",doc.get("image"));
            jsnews.put("source",doc.get("source"));
            jsnews.put("href",doc.get("href"));
            jsnews.put("channel",doc.get("channel"));

            Timestamp timestamp = new Timestamp(Long.parseLong(doc.get("time")));
            String time = timeFormat.format(timestamp);
            jsnews.put("time",time);

            jsnews.put("tags",doc.get("tags"));
            jsnews.put("id",doc.get("id"));
            newsarray.add(jsnews);
        }

        // 关闭资源
        reader.close();

        JSONObject result = new JSONObject();
        int newsnum = Math.min(10000,count);
        result.put("data",newsarray);
        result.put("newsnum",newsnum);
        return result;
    }
}