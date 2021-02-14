# -*- coding: utf-8 -*-
import datetime
import scrapy
from scrapy.http import Request, HtmlResponse
from crawler.items import SinaItem, SinaLinkItem
from scrapy.selector import Selector
import json
import psycopg2
from crawler.settings import hostname, port, username, password, database
from crawler.utils import preprocess, setimage, setsource, settime, settitle

valid_prefix = (
    'https://news.sina.com.cn',
    'https://sports.sina.com.cn',
    'https://tech.sina.com.cn',
    'https://ent.sina.com.cn',
    'https://mil.news.sina.com.cn',
    'https://edu.sina.com.cn',
    'https://auto.sina.com.cn',
    'https://fashion.sina.com.cn',
    'https://eladies.sina.com.cn',
    'https://baby.sina.com.cn',
    'https://health.sina.com.cn',
    'https://cul.news.sina.com.cn',
    'https://games.sina.com.cn',
    'https://finance.sina.com.cn')

channels = (
    'society',
    'sports',
    'tech',
    'ent',
    'mil',
    'edu',
    'auto',
    'fashion',
    'women',
    'baby',
    'health',
    'cul',
    'game',
    'finance')

ids = [(3, 17),
       (4, 12),
       (13, 2503),
       (39, 561),
       (121, 1356),
       (153, 1655),
       (153, 2509),
       (153, 2510),
       (153, 2511),
       (153, 2512),
       (153, 2513),
       (153, 2514),
       (153, 2515),
       (153, 2516),
       (153, 2517),
       (153, 2518),
       (153, 2669),
       (153, 2968),
       (153, 2970),
       (153, 2972),
       (153, 2974),
       (372, 2431),
       (382, 2990),
       (384, 2519)]


def is_valid(url: str):
    return url.startswith(valid_prefix)


def get_channel(url: str):
    for i in range(len(valid_prefix)):
        if url.startswith(valid_prefix[i]):
            return channels[i]


def to_timestamp(date):
    return int(datetime.datetime(date.year, date.month, date.day, 0, 0, 0).timestamp())


class SinaDynamicLinkSpider(scrapy.Spider):
    name = 'sinadynamiclink'
    allowed_domains = ['sina.com.cn']
    handle_httpstatus_list = [301, 302, 404]

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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.SinaLinkPipeline': 1,
        },
    }

    url1 = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=%d&lid=%d&num=50'

    url2 = 'https://interface.sina.cn/games/gpapi/2016index/2020_interface_game_pc_home_newslist.shtml?callback=&fid=1_1&page=1&pageSize=200'

    url3 = 'https://interface.sina.cn/pc_api/public_news_data.d.json?cids=209211&type=std_news&pageSize=30&mod=nt_culture0&cTime=1483200000&up=0&action=1'

    def start_requests(self):
        for id_tuple in ids:
            yield Request(self.url1 % (id_tuple[0], id_tuple[1]), callback=self.parse_1)

        yield Request(self.url2, callback=self.parse_2)
        yield Request(self.url3, callback=self.parse_3)

    def parse_1(self, response):
        news_data = json.loads(response.text)
        item_list = news_data['result']['data']
        for item in item_list:
            news = SinaLinkItem()
            news['image'] = ''
            news['href'] = preprocess(item['url'])
            if is_valid(news['href']):
                yield news

    def parse_2(self, response):
        result = HtmlResponse(body=json.loads(response.text)['result']['data'], url='', encoding='utf-8')
        selector = Selector(response=result)
        result = selector.xpath('//h3/a/@href').getall()
        for res in result:
            news = SinaLinkItem()
            news['image'] = ''
            news['href'] = preprocess(res)
            if is_valid(news['href']):
                yield news

    def parse_3(self, response):
        news_data = json.loads(response.text)
        item_list = news_data['data']
        for item in item_list:
            news = SinaLinkItem()
            news['image'] = ''
            news['href'] = preprocess(item['url'])
            if is_valid(news['href']):
                yield news


class SinaStaticLink1Spider(scrapy.Spider):
    name = 'sinastaticlink1'
    allowed_domains = ['sina.com.cn']
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.SinaLinkPipeline': 1,
        },
    }

    template = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=%d&lid=%d&etime=%d&stime=%d&ctime=%d&k=&num=50&page=%d'

    def __init__(self, syear=2020, smonth=1, sday=1, eyear=2020, emonth=12, eday=1, *args, **kwargs):
        super(SinaStaticLink1Spider, self).__init__(*args, **kwargs)
        self.start_date = datetime.date(int(syear), int(smonth), int(sday))
        self.end_date = datetime.date(int(eyear), int(emonth), int(eday))

    def start_requests(self):
        date = self.start_date
        while date < self.end_date:
            print(date)
            for id_tuple in ids:
                for page in range(1, 51):
                    time1 = to_timestamp(date)
                    time2 = to_timestamp(date + datetime.timedelta(days=1))
                    url = self.template % (id_tuple[0], id_tuple[1], time1, time2, time2, page)
                    request = Request(url, callback=self.parse)
                    yield request
            date += datetime.timedelta(days=1)

    def parse(self, response):
        news_data = json.loads(response.text)
        item_list = news_data['result']['data']
        for item in item_list:
            news = SinaLinkItem()
            news['image'] = ''
            news['href'] = preprocess(item['url'])
            if is_valid(news['href']):
                yield news


class SinaStaticLink2Spider(scrapy.Spider):
    name = 'sinastaticlink2'
    allowed_domains = ['sina.com.cn']
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.SinaLinkPipeline': 1,
        },
    }

    url1 = 'https://interface.sina.cn/games/gpapi/2016index/2020_interface_game_pc_home_newslist.shtml?callback=&fid=1_1&page=%d&pageSize=200'
    num1 = 10

    url2 = 'https://interface.sina.cn/pc_api/public_news_data.d.json?cids=209211&type=std_news&pageSize=30&mod=nt_culture0&cTime=1483200000&up=%d&action=1'
    num2 = 50

    def start_requests(self):
        for i in range(1, self.num1):
            yield Request(url=self.url1 % i, callback=self.parse_1)
        for i in range(0, self.num2):
            yield Request(url=self.url2 % i, callback=self.parse_2)

    def parse_1(self, response):
        try:
            result = HtmlResponse(body=json.loads(response.text)['result']['data'], url='', encoding='utf-8')
        except json.decoder.JSONDecodeError:
            print(response.url)
            return
        selector = Selector(response=result)
        result = selector.xpath('//h3/a/@href').getall()
        for res in result:
            news = SinaLinkItem()
            news['image'] = ''
            news['href'] = preprocess(res)
            if is_valid(news['href']):
                yield news

    def parse_2(self, response):
        try:
            news_data = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            print(response.url)
            return
        item_list = news_data['data']
        if item_list is not None:
            for item in item_list:
                news = SinaLinkItem()
                news['image'] = ''
                news['href'] = preprocess(item['url'])
                if is_valid(news['href']):
                    yield news


class SinaDetailSpider(scrapy.Spider):
    name = 'sinadetail'
    allowed_domains = ['sina.com.cn']
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        },
        'ITEM_PIPELINES': {
            'crawler.pipelines.SinaPipeline': 1,
        },
    }

    def start_requests(self):
        connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
        connection.autocommit = True
        cur = connection.cursor()
        cur.execute("select * from links where processed=false and position('sina.com.cn' in href)>0 limit 10000;")
        record = cur.fetchone()
        while record is not None:
            news = SinaItem()
            news['id'] = record[0]
            news['href'] = record[1]
            request = Request(news['href'], callback=self.parse_detail)
            request.meta['news'] = news
            yield request
            record = cur.fetchone()
        cur.close()
        connection.close()

    def parse_detail(self, response):
        news = response.meta['news']
        content = ""
        p_list1 = response.xpath("//div[@id='artibody']//p")
        p_list2 = response.xpath("//div[@id='article']//p")
        if len(p_list1) != 0:
            p_list = p_list1
        else:
            p_list = p_list2
        if len(p_list) == 0:
            news['valid'] = False
            yield news
        else:
            news['valid'] = True
            for p in p_list:
                p_str = p.xpath("string(.)").extract_first()  # 返回当前元素的所有节点文本内容
                if p_str:
                    content += p_str
            news['content'] = content
            image1 = response.xpath("//meta[@property='og:image']/@content").extract_first()
            image2 = response.xpath("//div[@class='img_wrapper']/img/@src").extract_first()
            news = setimage(news, image1, image2)
            title1 = response.xpath("//meta[@property='og:title']/@content").extract_first()
            title2 = response.xpath("//h1[@class='main-title']").xpath('string(.)').extract_first()
            title3 = response.xpath("//h1").xpath('string(.)').extract_first()
            news = settitle(news, title1, title2, title3)
            time1 = response.xpath("//meta[@name='weibo: article:create_at']/@content").extract_first()
            time2 = response.xpath("//meta[@property='article:published_time']/@content").extract_first()
            time3 = response.xpath("//span[@id='pub_date']").xpath('string(.)').extract_first()
            time4 = response.xpath("//span[@class='date']").xpath('string(.)').extract_first()
            news['time'] = None
            news = settime(news, time1, time2, time3, time4)
            if news['time'] is None:
                news['valid'] = False
            else:
                source1 = response.xpath("//meta[@name='mediaid']/@content").extract_first()
                source2 = response.xpath("//meta[@property='article:author']/@content").extract_first()
                news = setsource(news, source1, source2)
                news['tags'] = response.xpath("//meta[@name='keywords']/@content").extract_first().replace(news['title'] + ',', '').replace(news['title'], '')
                news['channel'] = get_channel(news['href'])
            yield news
