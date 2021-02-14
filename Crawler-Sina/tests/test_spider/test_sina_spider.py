from crawler.spiders.sina import SinaDynamicLinkSpider, SinaStaticLink1Spider, SinaStaticLink2Spider, SinaDetailSpider
from crawler.items import SinaItem, SinaLinkItem
from scrapy.http import Request
from crawler.pipelines import SinaPipeline, SinaLinkPipeline


def test_sinadynamiclink(resource_get):
    spider = SinaDynamicLinkSpider()
    pipeline = SinaLinkPipeline()
    pipeline.open_spider(spider)
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
    }
    requests = spider.start_requests()
    for request in requests:
        assert isinstance(request, Request)
        selector1 = resource_get(request.url, headers=headers, request=request)
        if request.callback == spider.parse_1:
            result1 = spider.parse_1(selector1)
        elif request.callback == spider.parse_2:
            result1 = spider.parse_2(selector1)
        elif request.callback == spider.parse_3:
            result1 = spider.parse_3(selector1)
        item = result1.__next__()
        assert isinstance(item, SinaLinkItem)
        pipeline.process_item(item, spider)
    pipeline.close_spider(spider)


def test_sinastaticlink1(resource_get):
    spider = SinaStaticLink1Spider()
    pipeline = SinaLinkPipeline()
    pipeline.open_spider(spider)
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
    }
    requests = spider.start_requests()
    for i in range(25):
        request = requests.__next__()
        assert isinstance(request, Request)
        selector1 = resource_get(request.url, headers=headers, request=request)
        assert request.callback == spider.parse
        result1 = spider.parse(selector1)
        try:
            item = result1.__next__()
            assert isinstance(item, SinaLinkItem)
            pipeline.process_item(item, spider)
        except StopIteration:
            continue
    pipeline.close_spider(spider)


def test_sinastaticlink2(resource_get):
    spider = SinaStaticLink2Spider()
    pipeline = SinaLinkPipeline()
    pipeline.open_spider(spider)
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
    }

    requests = spider.start_requests()

    for request in requests:
        assert isinstance(request, Request)
        selector = resource_get(request.url, headers=headers, request=request, allow_redirects=False)
        if request.callback == spider.parse_1:
            result1 = spider.parse_1(selector)
        elif request.callback == spider.parse_2:
            result1 = spider.parse_2(selector)
        try:
            item = result1.__next__()
        except StopIteration:
            continue
        assert isinstance(item, SinaLinkItem)
        pipeline.process_item(item, spider)
    pipeline.close_spider(spider)


def test_sinadetail(resource_get):
    spider = SinaDetailSpider()
    pipeline = SinaPipeline()
    pipeline.open_spider(spider)
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
    }

    requests = spider.start_requests()
    for i in range(100):
        request = requests.__next__()
        assert isinstance(request, Request)
        selector = resource_get(request.url, headers=headers, request=request)
        result = spider.parse_detail(selector)
        item = result.__next__()
        assert isinstance(item, SinaItem)
        pipeline.process_item(item, spider)
    pipeline.close_spider(spider)
