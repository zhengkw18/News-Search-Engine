import pathlib
import pytest
from scrapy.http import HtmlResponse

import betamax
from betamax.fixtures.pytest import _betamax_recorder

# betamax配置，设置betamax录像带的存储位置
cassette_dir = pathlib.Path(__file__).parent / 'fixture' / 'cassettes'
cassette_dir.mkdir(parents=True, exist_ok=True)
with betamax.Betamax.configure() as config:
    config.cassette_library_dir = cassette_dir.resolve()
    config.preserve_exact_body_bytes = True


@pytest.fixture
def betamax_recorder(request):
    """
    修改默认的betamax pytest fixtures
    让它默认可用接口pytest.mark.parametrize装饰器，并且生产不同的录像带.
    有些地方可能会用到
    """
    return _betamax_recorder(request, parametrized=True)


@pytest.fixture
def resource_get(betamax_session):
    """这是一个pytest fixture
    返回一个http请求方法，相当于:

    with Betamax(session) as vcr:
        vcr.use_use_cassette('这里是测试函数的qualname')
        resp = session.get(url, *args, **kwargs)
        # 将requests的Response，封装成scrapy的HtmlResponse
        return HtmlResponse(body=resp.content)
    """
    def get(url, *args, **kwargs):
        request = kwargs.pop('request', None)
        resp = betamax_session.get(url, *args, **kwargs)
        selector = HtmlResponse(body=resp.content, url=url, request=request, status=resp.status_code)
        return selector

    return get
