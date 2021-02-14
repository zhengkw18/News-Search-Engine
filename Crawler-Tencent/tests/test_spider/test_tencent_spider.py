from crawler.spiders.tencent import TencentDynamicLink1Spider, TencentDynamicLink2Spider, TencentStaticLinkSpider, TencentDetailSpider
from crawler.items import TencentItem, TencentLinkItem
from scrapy.http import Request
from crawler.pipelines import TencentPipeline, TencentLinkPipeline


def test_tencentdynamiclink1(resource_get):
    spider = TencentDynamicLink1Spider()
    pipeline = TencentLinkPipeline()
    pipeline.open_spider(spider)
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
    }
    requests = spider.start_requests()
    for request in requests:
        assert isinstance(request, Request)
        selector1 = resource_get(request.url, headers=headers, request=request)
        assert request.callback == spider.parse_1
        result1 = spider.parse_1(selector1)
        request1 = result1.__next__()
        assert isinstance(request1, Request)
        assert request1.callback == spider.parse_detail
        selector2 = resource_get(request1.url, headers=headers, request=request1)
        result2 = spider.parse_detail(selector2)
        item = result2.__next__()
        assert isinstance(item, TencentLinkItem)
        pipeline.process_item(item, spider)
    pipeline.close_spider(spider)


def test_tencentdynamiclink2(resource_get):
    spider = TencentDynamicLink2Spider()
    pipeline = TencentLinkPipeline()
    pipeline.open_spider(spider)
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
    }
    requests = spider.start_requests()
    for request in requests:
        assert isinstance(request, Request)
        selector1 = resource_get(request.url, headers=headers, request=request)
        assert request.callback == spider.parse_2
        result1 = spider.parse_2(selector1)
        for request1 in result1:
            assert isinstance(request1, Request)
            if request1.callback == spider.parse_detail:
                selector2 = resource_get(request1.url, headers=headers, request=request1)
                result2 = spider.parse_detail(selector2)
                item = result2.__next__()
                assert isinstance(item, TencentLinkItem)
                pipeline.process_item(item, spider)
            else:
                break
    pipeline.close_spider(spider)


def test_tencentstaticlink(resource_get):
    spider = TencentStaticLinkSpider()
    pipeline = TencentLinkPipeline()
    pipeline.open_spider(spider)
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
    }

    requests = spider.start_requests()

    for request in requests:
        assert isinstance(request, Request)
        selector = resource_get(request.url, headers=headers, request=request, allow_redirects=False)
        result = spider.parse_detail(selector)
        try:
            result.__next__()
        except StopIteration:
            pass
        if selector.status == 200:
            break
    pipeline.close_spider(spider)


def test_tencentdetail(resource_get):
    spider = TencentDetailSpider()
    pipeline = TencentPipeline()
    pipeline.open_spider(spider)
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36"
    }

    requests = spider.start_requests()
    request = requests.__next__()
    assert isinstance(request, Request)
    selector = resource_get(request.url, headers=headers, request=request)
    result = spider.parse_detail(selector)
    item = result.__next__()
    assert isinstance(item, TencentItem)
    pipeline.process_item(item, spider)
    pipeline.close_spider(spider)
