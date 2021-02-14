# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy.http import Request
from crawler.items import TencentItem, TencentLinkItem
import json
import psycopg2
from crawler.settings import hostname, port, username, password, database


class TencentDynamicLink1Spider(scrapy.Spider):
    name = 'tencentdynamiclink1'
    allowed_domains = ['qq.com']
    handle_httpstatus_list = [301, 302, 404]
    mobile_url = 'https://xw.qq.com/cmsid/{}'
    recommend_url = 'https://pacaio.match.qq.com/xw/relate?num=30&id=0'  # 推荐新闻
    mobile_ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38' \
                ' (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'

    custom_settings = {
        'CONCURRENT_REQUESTS': 64,
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'RETRY_TIMES': 15,
        'DEFAULT_REQUEST_HEADERS': {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.TencentLinkPipeline': 1,
        },
    }

    url1 = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?sub_srv_id=%s&srv_id=pc&offset=0&limit=199&strategy=1&ext={"pool":["high","top"],"is_filter":10,"check_type":true}'
    candidate1 = ['24hours', 'antip', 'bj', 'ent', 'milite', 'world', 'tech', 'digi', 'finance', 'nstock', 'licai', 'auto', 'fashion', 'video', 'games',
                  'cul', 'house', 'comic', 'emotion', 'astro', 'health', 'baby', 'pet', 'history', 'football', 'newssh', 'rushidao', 'edu', 'sports', 'lifes', 'kepu']

    def start_requests(self):
        for ident in self.candidate1:
            yield Request(self.url1 % ident, callback=self.parse_1)

    def setCursor(self, cursor):
        self.cur = cursor

    def parse_1(self, response):
        news_data = json.loads(response.text)
        item_list = news_data['data']
        item_list = item_list['list']
        for item in item_list:
            news = TencentLinkItem()
            news['image'] = item['img']
            news['id'] = item['article_id']
            href1 = 'https://new.qq.com/omn/%s/%s00.html' % (news['id'][:8], news['id'])
            href2 = "https://new.qq.com/rain/a/" + news['id'] + "00"
            self.cur.execute("select * from links where href=%s or href=%s;", (href1, href2,))
            if len(self.cur.fetchall()) == 0:
                news['href'] = 'https://new.qq.com/omn/%s/%s00.html' % (news['id'][:8], news['id'])
                request = Request(url=news['href'], callback=self.parse_detail)
                request.meta['news'] = news
                yield request

    def parse_detail(self, response):
        news = response.meta['news']
        if response.status == 302:
            news['href'] = "https://new.qq.com/rain/a/" + news['id'] + "00"
            yield news
        if response.status == 200:
            yield news


class TencentDynamicLink2Spider(scrapy.Spider):
    name = 'tencentdynamiclink2'
    allowed_domains = ['qq.com']
    handle_httpstatus_list = [301, 302, 404]
    mobile_url = 'https://xw.qq.com/cmsid/{}'
    recommend_url = 'https://pacaio.match.qq.com/xw/relate?num=30&id=0'  # 推荐新闻
    mobile_ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38' \
                ' (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'

    custom_settings = {
        'CONCURRENT_REQUESTS': 64,
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'RETRY_TIMES': 15,
        'DEFAULT_REQUEST_HEADERS': {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.TencentLinkPipeline': 1,
        },
    }
    url2 = 'https://pacaio.match.qq.com/irs/rcd?cid=58&token=c232b098ee7611faeffc46409e836360&ext=%s&page=%d'
    candidate2 = ['all', 'antip', 'bj', 'msh', 'visit', 'milite', 'digi', 'fashion', 'games', 'health', 'cul', 'astro', 'comic',
                  'emotion', 'house', 'world', 'tech', 'finance', 'ent', 'sports', 'auto', 'baby', 'pet', 'history', 'edu', 'lifes', 'kepu']

    def start_requests(self):
        for ident in self.candidate2:
            request = Request(self.url2 % (ident, 0), callback=self.parse_2)
            request.meta['page'] = 0
            request.meta['ident'] = ident
            yield request

    def setCursor(self, cursor):
        self.cur = cursor

    def parse_2(self, response):
        news_data = json.loads(response.text)
        item_list = news_data['data']
        for item in item_list:
            news = TencentLinkItem()
            news['image'] = item['img']
            news['id'] = item['id']
            href1 = 'https://new.qq.com/omn/%s/%s00.html' % (news['id'][:8], news['id'])
            href2 = "https://new.qq.com/rain/a/" + news['id'] + "00"
            self.cur.execute("select * from links where href=%s or href=%s;", (href1, href2,))
            if len(self.cur.fetchall()) == 0:
                news['href'] = 'https://new.qq.com/omn/%s/%s00.html' % (news['id'][:8], news['id'])
                request = Request(url=news['href'], callback=self.parse_detail)
                request.meta['news'] = news
                yield request

        page = response.meta['page']
        ident = response.meta['ident']
        next_link = self.url2 % (ident, page + 1)
        request = Request(next_link, callback=self.parse_2)
        request.meta['page'] = page + 1
        request.meta['ident'] = ident
        yield request

    def parse_detail(self, response):
        news = response.meta['news']
        if response.status == 302:
            news['href'] = "https://new.qq.com/rain/a/" + news['id'] + "00"
            yield news
        if response.status == 200:
            yield news


class TencentStaticLinkSpider(scrapy.Spider):
    name = 'tencentstaticlink'
    allowed_domains = ['qq.com']
    handle_httpstatus_list = [301, 302, 404]
    custom_settings = {
        'CONCURRENT_REQUESTS': 32,
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'RETRY_TIMES': 15,
        'DEFAULT_REQUEST_HEADERS': {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.TencentLinkPipeline': 1,
        },
    }
    last_item_num = 1

    def __init__(self, syear=2020, smonth=1, sday=1, eyear=2020, emonth=1, eday=2, *args, **kwargs):
        super(TencentStaticLinkSpider, self).__init__(*args, **kwargs)
        self.start_date = datetime.date(int(syear), int(smonth), int(sday))
        self.end_date = datetime.date(int(eyear), int(emonth), int(eday))

    def setCursor(self, cursor):
        self.cur = cursor

    def start_requests(self):
        candidate = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        date = self.start_date
        while date < self.end_date:
            for i in range(0, len(candidate) ** 4):
                if i % 10000 == 0:
                    print(date, "%s/%s" % (i, len(candidate) ** 4), self.last_item_num)
                    if self.last_item_num == 0:
                        break
                    self.last_item_num = 0
                ident = ""
                index = i
                for j in range(0, 4):
                    ident = candidate[index % len(candidate)] + ident
                    index //= len(candidate)
                news = TencentLinkItem()
                news['id'] = date.strftime("%Y%m%d") + 'A0' + ident
                news['image'] = ""
                news['href'] = 'https://new.qq.com/omn/%s/%s00.html' % (news['id'][:8], news['id'])
                request = Request(news['href'], callback=self.parse_detail)
                request.meta['news'] = news
                yield request
            date += datetime.timedelta(days=1)
            self.last_item_num = 1

    def parse_detail(self, response):
        if response.status == 200:
            self.last_item_num += 1
            news = response.meta['news']
            href1 = 'https://new.qq.com/omn/%s/%s00.html' % (news['id'][:8], news['id'])
            href2 = "https://new.qq.com/rain/a/" + news['id'] + "00"
            self.cur.execute("select * from links where href=%s or href=%s;", (href1, href2,))
            if len(self.cur.fetchall()) == 0:
                yield news


class TencentDetailSpider(scrapy.Spider):
    name = 'tencentdetail'
    allowed_domains = ['qq.com']
    custom_settings = {
        'CONCURRENT_REQUESTS': 64,
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': False,
        'LOG_LEVEL': 'INFO',
        'RETRY_TIMES': 15,
        'DEFAULT_REQUEST_HEADERS': {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.TencentPipeline': 1,
        },
    }

    def start_requests(self):
        connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
        connection.autocommit = True
        cur = connection.cursor()
        cur.execute("select * from links where processed=false and position('new.qq.com' in href)>0 limit 10000;")
        record = cur.fetchone()
        while record is not None:
            news = TencentItem()
            news['id'] = record[0]
            news['href'] = record[1]
            news['image'] = record[2]
            request = Request(news['href'], callback=self.parse_detail)
            request.meta['news'] = news
            yield request
            record = cur.fetchone()
        cur.close()
        connection.close()

    def parse_detail(self, response):
        news = response.meta['news']
        content = ""
        first_img = ""
        p_list = response.xpath("//p[1]//parent::div/p")
        if len(p_list) == 0:
            news['valid'] = False
            yield news
        else:
            news['valid'] = True
            for p in p_list:
                p_str = p.xpath("string(.)").extract_first()  # 返回当前元素的所有节点文本内容
                if p_str:
                    content += p_str
                if p.xpath(".//img") and first_img == "":  # 有照片
                    first_img = 'https:' + p.xpath(".//img/@src").extract_first()
            news['content'] = content
            if news['image'] == '':
                news['image'] = first_img
            header = response.xpath('//script[contains(text(),"window.DATA")]')
            header = header[0].xpath("string(.)").extract_first().replace("window.DATA =", "")
            header = json.loads(header)
            news['title'] = header['title']
            news['time'] = header['pubtime']
            news['source'] = header['media']
            news['tags'] = header['tags']
            news['channel'] = ''
            if 'catalog1' in header.keys():
                news['channel'] = header['catalog1']
            yield news
