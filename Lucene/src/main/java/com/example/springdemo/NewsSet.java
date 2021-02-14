package com.example.springdemo;

import java.sql.*;
import java.util.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class NewsSet {
    static int maxId = 0;

    public static List<News> getNews() throws SQLException {

        //打印日志
        Logger logger = LoggerFactory.getLogger("INFO");

        //新闻列表
        List<News> list = new ArrayList<>();

        long  startTime = System.currentTimeMillis();    //获取开始时间

        //连接数据库
        Connection connection = DriverManager.getConnection(
                "jdbc:postgresql://49.233.9.194:32100/specteam", "specteam", "specteam");
        try {
            // 创建Statement对象
            Statement stmt = connection.createStatement();
            try {
                // SQL语句
                String sql = "select * from app_article where id > " + maxId + " order by id limit 1000;";
                // 获取结果集
                ResultSet resultSet = stmt.executeQuery(sql);
                try {
                    logger.info("++++++++++++++++++++++++++++++++++++++");
                    int count = 0;
                    // 结果集解析
                    while (resultSet.next()) {
                        count++;
                        News news = new News();
                        news.setTitle(resultSet.getString("title"));
                        news.setContent(resultSet.getString("content"));
                        news.setHref(resultSet.getString("href"));
                        String id = resultSet.getString("id");
                        news.setId(id);
                        int newid = Integer.parseInt(id);
                        maxId = (newid > maxId) ? newid : maxId;
                        news.setSource(resultSet.getString("source"));

                        //格式化时间
                        Timestamp timestamp = resultSet.getTimestamp("time");
                        news.setTime(timestamp);

                        news.setImage(resultSet.getString("image"));
                        news.setChannel(resultSet.getString("channel"));
                        news.setTags(resultSet.getString("tags"));
                        list.add(news);
                    }
                    logger.info("news count is {}", count);
                    logger.info("max_id is {}", maxId);
                } finally {
                    resultSet.close();
                }
            } finally {
                stmt.close();
            }
        } finally {
            connection.close();
        }
        long endTime = System.currentTimeMillis();
        logger.info("程序运行时间：{} s",(endTime - startTime) / 1000.0);

        return list;
    }
}
