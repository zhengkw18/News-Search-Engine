# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
from crawler.settings import hostname, username, password, database, port


class SinaPipeline(object):
    def open_spider(self, spider):

        # 创建连接
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
        self.connection.autocommit = True
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        if item['valid']:
            self.cur.execute("insert into app_article(title,source,time,content,channel,tags,href,image) values(%s,%s,to_timestamp(%s,'YYYY-MM-DD HH24:MI:SS'),%s,%s,%s,%s,%s);",
                             (item['title'], item['source'], item['time'], item['content'], item['channel'], item['tags'], item['href'], item['image']))
            self.cur.execute("update links set processed=true, valid=true where id=%s;", (item['id'],))
        else:
            self.cur.execute("update links set processed=true, valid=false where id=%s;", (item['id'],))
        return item


class SinaLinkPipeline(object):
    def open_spider(self, spider):
        # 创建连接
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
        self.connection.autocommit = True
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("select * from links where href=%s;", (item['href'],))
        if len(self.cur.fetchall()) == 0:
            self.cur.execute("insert into links(href,image,processed,valid) values(%s,%s,false,false);", (item['href'], item['image'],))
        return item
