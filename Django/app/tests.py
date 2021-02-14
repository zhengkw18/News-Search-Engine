"""
Unit test file for django backend
"""
import datetime
import pytest
from django.urls import reverse
from .models import Article, User, Token


@pytest.mark.django_db
def test_model_user():
    """
    Test model user
    """
    user = User(name="a", password="b", email="c", tags="")
    user.save()
    assert User.objects.all().count() > 0
    assert str(user) == "a"


@pytest.mark.django_db
def test_model_article():
    """
    Test model article
    """
    article = Article(title="a",
                      time=datetime.datetime.now(),
                      source="b",
                      content="c",
                      href="d",
                      image="e",
                      channel="f",
                      tags="g")
    article.save()
    assert Article.objects.all().count() > 0
    assert str(article) == "a"


@pytest.mark.django_db
def test_model_token():
    """
    Test model token
    """
    token = Token(token="a", code="b", expiretime=0)
    token.save()
    assert Token.objects.all().count() > 0
    assert str(token) == "a"


@pytest.mark.django_db
def test_view_news(client):
    """
    Test view news
    """
    url = reverse("news")
    data = {
        'start': -1
    }
    response = client.get(url, data=data)
    assert response.status_code == 400
    data = {
        'size': 120
    }
    response = client.get(url, data=data)
    assert response.status_code == 400
    data = {
        'channel': "all"
    }
    response = client.get(url, data=data)
    assert response.status_code == 200
    data = {
        'channel': "society"
    }
    response = client.get(url, data=data)
    assert response.status_code == 200
    data = {
        'channel': "ent"
    }
    response = client.get(url, data=data)
    assert response.status_code == 200
    client.cookies['username'] = 'admin'
    data = {
        'channel': "all"
    }
    response = client.get(url, data=data)
    assert response.status_code == 400
    user = User(name="admin", password="b", email="c", tags="a")
    user.save()
    response = client.get(url, data=data)
    assert response.status_code == 400
    user.tags = r'{"data": []}'
    user.save()
    response = client.get(url, data=data)
    assert response.status_code == 200
    user.tags = r'{"data":[{"tag":"合肥房价","num":1,"lasttime":1605623462951}]}'
    user.save()
    response = client.get(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_search(client):
    """
    Test view search
    """
    url = reverse("search")
    client.cookies['username'] = 'admin'
    data = {
        'start': 0,
        'keyword': "TES"
    }
    response = client.get(url, data=data)
    assert response.status_code == 200
    data = {
        'start': -10,
        'keyword': "TES"
    }
    response = client.get(url, data=data)
    assert response.status_code == 400
    data = {
        'size': 120,
        'keyword': "TES"
    }
    response = client.get(url, data=data)
    assert response.status_code == 400
    data = {
        'start': 0,
        'keyword': " "
    }
    response = client.get(url, data=data)
    assert response.status_code == 200
    data = {
        'start': 0,
        'timestart': 0,
        'timeend': 1,
        'site': "tencent sina",
        'keyword': "TES"
    }
    response = client.get(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_register(client):
    """
    Test view register
    """
    url = reverse("register")
    response = client.get(url)
    assert response.status_code == 400
    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 400
    data = {
        "username": "a",
        "password": "b",
        "authcode": "m",
        "email": "zhengkw@qq.com"
    }
    response = client.post(url, data=data)
    assert response.status_code == 400
    token = Token(token="m", code="n", expiretime=100000000000000000)
    token.save()
    client.cookies['token'] = 'm'
    data = {
        "username": "a",
        "password": "b",
        "authcode": "m",
        "email": "zhengkw@qq.com"
    }
    response = client.post(url, data=data)
    assert response.status_code == 400
    data = {
        "username": "a",
        "password": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "authcode": "n",
        "email": "zhengkw@qq.com"
    }
    response = client.post(url, data=data)
    assert response.status_code == 400
    data = {
        "username": "a",
        "password": "b",
        "authcode": "n",
        "email": "zhengkw@qq.com"
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    data = {
        "username": "a",
        "password": "b"
    }
    response = client.post(url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_view_login(client):
    """
    Test view login
    """
    url = reverse("login")
    response = client.get(url)
    assert response.status_code == 400
    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 400
    data = {
        "username": "a",
        "password": "b"
    }
    response = client.post(url, data=data)
    assert response.status_code == 400
    user = User(name="a", password="b")
    user.save()
    data = {
        "username": "a",
        "password": "b"
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    data = {
        "username": "a",
        "password": "c"
    }
    response = client.post(url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_view_update(client):
    """
    Test view update
    """
    url = reverse("update")
    response = client.get(url)
    assert response.status_code == 400
    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 400
    client.cookies['username'] = 'a'
    response = client.post(url, data=data)
    assert response.status_code == 400
    user = User(name="a", password="b", email="zhengkw@qq.com", tags=r'{"data": []}')
    user.save()
    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 400
    data = {'password': "b"}
    response = client.post(url, data=data)
    assert response.status_code == 200
    data = {
        "password": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    }
    response = client.post(url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_view_getinfo(client):
    """
    Test view getinfo
    """
    url = reverse("getinfo")
    response = client.get(url)
    assert response.status_code == 400
    client.cookies['username'] = 'a'
    response = client.get(url)
    assert response.status_code == 400
    user = User(name='a', password='b', email='zhengkw@qq.com', tags='.')
    user.save()
    response = client.get(url)
    assert response.status_code == 200
    user.tags = r'{"data":[{"tag":"合肥房价","num":1,"lasttime":1605623462951}]}'
    user.save()
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_settags(client):
    """
    Test view settags
    """
    url = reverse("settags")
    response = client.get(url)
    assert response.status_code == 400
    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 400
    client.cookies['username'] = 'a'
    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 400
    user = User(name='a', password='b', email='zhengkw@qq.com', tags=r'{"data": []}')
    user.save()
    data = {'data': []}
    response = client.post(url, data=data, content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_email(client):
    """
    Test view email
    """
    url = reverse("email")
    response = client.get(url)
    assert response.status_code == 400
    data = {'email': 'zhengkw@qq.com'}
    response = client.post(url, data=data)
    assert response.status_code == 200
