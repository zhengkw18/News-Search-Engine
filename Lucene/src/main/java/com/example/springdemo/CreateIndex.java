package com.example.springdemo;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.*;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.wltea.analyzer.lucene.IKAnalyzer;

import java.io.File;
import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class CreateIndex{
    //创建分词器
    Analyzer analyzer;
    // 指定索引库的地址
    Directory directory;
    // 创建IndexWriter
    private final IndexWriter writer;

    CreateIndex() throws IOException {
        analyzer = new IKAnalyzer();
        directory = FSDirectory.open(new File("indexsource"));
        IndexWriterConfig cfg = new IndexWriterConfig(Version.LUCENE_4_10_3, analyzer);
        cfg.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND);
        writer = new IndexWriter(directory,cfg);
    }

    void createAppend() throws IOException, SQLException {
        List<News> newsList = NewsSet.getNews();
        if(newsList.isEmpty()) return;

        long startTime = System.currentTimeMillis();
        List<Document> docList = new ArrayList<>();
        for(News news: newsList){
            Document document = new Document();

            // 设置Field域
            Field title = new TextField("title",news.getTitle(), Field.Store.YES);
            Field content = new TextField("content",news.getContent(), Field.Store.YES);
            Field source = new StringField("source",news.getSource(), Field.Store.YES);
            Field time = new LongField("time",news.getTime().getTime(),Field.Store.YES);
            Field id = new StringField("id",news.getId(),Field.Store.YES);
            Field href = new TextField("href",news.getHref(), Field.Store.YES);
            Field image = new StringField("image",news.getImage(),Field.Store.YES);
            Field channel = new StringField("channel",news.getChannel(),Field.Store.YES);
            Field tags = new TextField("tags",news.getTags(),Field.Store.YES);

            //将Field域放入document中
            document.add(title);
            document.add(content);
            document.add(source);
            document.add(time);
            document.add(id);
            document.add(href);
            document.add(image);
            document.add(channel);
            document.add(tags);

            docList.add(document);
        }

        // 通过IndexWriter对象将Document写入到索引库中
        for(Document doc: docList) {
            writer.addDocument(doc);
        }

        //提交
        writer.commit();

        long endTime = System.currentTimeMillis();
        Logger logger = LoggerFactory.getLogger("INFO");
        logger.info("建立索引所用时间：{} s",(endTime - startTime) / 1000.0);
    }
}
