'''
Basic views
'''
import json
import datetime
import random
import requests
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from app.models import Article, User, Token

SITE_FILTERS = {
    'tencent': ['new.qq.com'],
    'sina': [
        'news.sina.com.cn',
        'sports.sina.com.cn',
        'tech.sina.com.cn',
        'ent.sina.com.cn',
        'mil.news.sina.com.cn',
        'edu.sina.com.cn',
        'auto.sina.com.cn',
        'fashion.sina.com.cn',
        'eladies.sina.com.cn',
        'baby.sina.com.cn',
        'health.sina.com.cn',
        'cul.news.sina.com.cn',
        'games.sina.com.cn',
        'finance.sina.com.cn'],
}

RANDOM_CANDIDATE = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    'z',
    'y',
    'x',
    'w',
    'v',
    'u',
    't',
    's',
    'r',
    'q',
    'p',
    'o',
    'n',
    'm',
    'l',
    'k',
    'j',
    'i',
    'h',
    'g',
    'f',
    'e',
    'd',
    'c',
    'b',
    'a']


def err_response(data: str):
    """
    Return an error with a message
    """
    return JsonResponse({
        'data': data
    }, status=400)


def timestamp2time(timestamp: str):
    """
    Transform a timestamp of length 13 to YYYY-mm-dd HH:MM:SS format str
    """
    timetamp = datetime.datetime.fromtimestamp(int(timestamp) / (10**3))
    return timetamp.strftime("%Y-%m-%d %H:%M:%S")


def random_str(length: int):
    """
    Generate random str of a specific length
    """
    return ''.join(random.sample(RANDOM_CANDIDATE, length))


def news(request):
    """
    Interface for newslist
    """
    start = int(request.GET.get('start', '0'))
    size = int(request.GET.get('size', '20'))
    if start < 0:
        return err_response("Start should be greater or equal to 0")
    if size <= 0 or size > 100:
        return err_response("Size should be in range (0,100]")
    responsejson = {}
    channel = request.GET.get('channel', 'all')
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        responsejson['username'] = username
    if 'username' in request.COOKIES and channel == 'all':
        users = User.objects.all().filter(name=username)
        if users:
            user = users[0]
        else:
            return err_response("Abnormal user status")
        try:
            tagjson = json.loads(user.tags)
        except ValueError:
            return err_response("Abnormal user status")
        taglist = tagjson['data']
        if taglist:
            taglist.sort(key=lambda tag: (-int(tag['num']), -int(tag['lasttime'])))
            taglist = taglist[:20]
            tagstr = ''
            for tag in taglist:
                tagstr += tag['tag']
                tagstr += ','
                tagstr += str(tag['num'])
                tagstr += ';'
            result = requests.get(url="https://lucene-specteam.app.secoder.net/tags", params={
                'tags': tagstr,
                'start': start * 2,
                'size': size * 2,
                'timestart': (datetime.datetime.now() - datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"),
            })
            if result.status_code == 200:
                response = result.json()
                responsejson['newsnum'] = response['newsnum']
                random_list = list(range(size * 2))
                random_list = random.sample(random_list, size)
                recommendation_list = []
                for i in random_list:
                    if i < len(response['data']):
                        newsitem = response['data'][i]
                        recommendation_list.append({
                            'title': newsitem['title'],
                            'source': newsitem['source'],
                            'time': newsitem['time'],
                            'content': newsitem['content'],
                            'href': newsitem['href'],
                            'image': newsitem['image'],
                            'channel': newsitem['channel'],
                            'tags': newsitem['tags'],
                        })
                responsejson['data'] = recommendation_list
                return JsonResponse(responsejson, status=200)
            return err_response("Query fail")
    articlelist = Article.objects
    if channel != 'all':
        if channel == 'society':
            articlelist = articlelist.filter(channel__in=['social', 'society'])
        else:
            articlelist = articlelist.filter(channel=channel)
    articlelist = articlelist.order_by('-time')
    articlelist = articlelist[start:start + size]
    responsejson['data'] = [{
        'title': newsitem.title,
        'source': newsitem.source,
        'time': newsitem.time.strftime("%Y-%m-%d %H:%M:%S"),
        'content': newsitem.content,
        'href': newsitem.href,
        'image': newsitem.image,
        'channel': newsitem.channel,
        'tags': newsitem.tags,
    } for newsitem in articlelist]

    return JsonResponse(responsejson, status=200)


def search(request):
    """
    Interface for news search
    """
    start = int(request.GET.get('start', '0'))
    size = int(request.GET.get('size', '20'))
    approach = request.GET.get('approach', 'relativity')
    keyword = request.GET.get('keyword', '')
    if start < 0:
        return err_response("Start should be greater or equal to 0")
    if size <= 0 or size > 100:
        return err_response("Size should be in range (0,100]")
    if keyword.strip() == '':
        responsejson = {
            'newsnum': 0,
            'data': []
        }
        if 'username' in request.COOKIES:
            responsejson['username'] = request.COOKIES['username']
        return JsonResponse(responsejson, status=200)
    requestjson = {
        "keyword": keyword,
        "start": start,
        "size": size,
        "approach": approach,
    }
    if 'timestart' in request.GET:
        requestjson['timestart'] = timestamp2time(request.GET['timestart'])
    if 'timeend' in request.GET:
        requestjson['timeend'] = timestamp2time(request.GET['timeend'])
    if 'site' in request.GET:
        sitestr = request.GET['site']
        sitelist = sitestr.split(' ')
        urllist = []
        for site in sitelist:
            urllist.extend(SITE_FILTERS[site])
        requestjson['hrefcontains'] = ' '.join(urllist)
    result = requests.get(url="https://lucene-specteam.app.secoder.net/get", params=requestjson)
    if result.status_code == 200:
        response = result.json()
        responsejson = {
            'newsnum': response['newsnum'],
            'data': [{
                'title': newsitem['title'],
                'source': newsitem['source'],
                'time': newsitem['time'],
                'content': newsitem['content'],
                'href': newsitem['href'],
                'image': newsitem['image'],
                'channel': newsitem['channel'],
                'tags': newsitem['tags'],
            } for newsitem in response['data']]
        }
        if 'username' in request.COOKIES:
            responsejson['username'] = request.COOKIES['username']
        return JsonResponse(responsejson, status=200)
    return err_response("Query fail")


def login(request):
    """
    Interface for user login
    """
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = "输入不能为空"
        if username and password:
            users = User.objects.all().filter(name=username)
            if users:
                user = users[0]
                if user.password == password:
                    return JsonResponse({}, status=200)
                message = "密码错误"
            else:
                message = "用户名不存在"
    else:
        message = "Undefined Interface"
    return err_response(message)


def register(request):
    """
    Interface for user register
    """
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        message = "输入不能为空"
        if username and password:
            users = User.objects.all().filter(name=username)
            if users:
                message = "用户名已存在"
            else:
                email = request.POST['email']
                authcode = request.POST['authcode']
                if 'token' in request.COOKIES:
                    token = request.COOKIES['token']
                    token = Token.objects.get(token=token)
                    if token.expiretime > datetime.datetime.now().timestamp() and authcode == token.code:
                        user = User(name=username, password=password, tags=r'{"data": []}', email=email)
                        try:
                            user.full_clean()
                            user.save()
                            return JsonResponse({}, status=200)
                        except ValidationError:
                            message = "请检查输入格式"
                    else:
                        message = "验证码错误或已过期"
                else:
                    message = "请验证邮箱"
    else:
        message = "Undefined Interface"
    return err_response(message)


def update(request):
    """
    Interface for user info update
    """
    if request.method == "POST":
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
            password = request.POST.get('password', None)
            message = "输入不能为空"
            users = User.objects.filter(name=username)
            if users and password:
                user = users[0]
                user.password = password
                try:
                    user.full_clean()
                    user.save()
                    return JsonResponse({}, status=200)
                except ValidationError:
                    message = "请检查输入格式"
            message = "用户不存在"
        message = "用户未登录"
    else:
        message = "Undefined Interface"
    return err_response(message)


def getinfo(request):
    """
    Interface for user info getting
    """
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
        users = User.objects.filter(name=username)
        if users:
            user = users[0]
            try:
                tagjson = json.loads(user.tags)
            except ValueError:
                tagjson = {"data": []}
            taglist = tagjson['data']
            tagstr = ''
            for tag in taglist:
                tagstr += tag['tag']
                tagstr += ','
                tagstr += str(tag['num'])
                tagstr += ','
                tagstr += str(tag['lasttime'])
                tagstr += ';'
            return JsonResponse({
                'tags': tagstr,
                'email': user.email,
            }, status=200)
        message = "用户不存在"
    message = "用户未登录"
    return err_response(message)


def settags(request):
    """
    Interface for user tags setting
    """
    if request.method == "POST":
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
            users = User.objects.filter(name=username)
            if users:
                user = users[0]
                user.tags = request.body.decode('utf-8')
                user.save()
                return JsonResponse({}, status=200)
            message = "用户不存在"
        message = "用户未登录"
    else:
        message = "Undefined Interface"
    return err_response(message)


def sendemail(request):
    """
    Interface for email
    """
    if request.method == "POST":
        email = request.POST['email']
        token = random_str(20)
        while Token.objects.filter(token=token).count() > 0:
            token = random_str(20)
        code = random_str(6)
        newtoken = Token(token=token,
                         code=code,
                         expiretime=int((datetime.datetime.now() + datetime.timedelta(minutes=30))
                                        .timestamp()))
        newtoken.save()
        response = JsonResponse({}, status=200)
        response.set_cookie('token', token)
        send_mail(subject='请查收您的Spect验证码',
                  message='您在Spect新闻注册的验证码为%s，请在30分钟内完成注册。' % code,
                  from_email='specteam@163.com',
                  recipient_list=[email],
                  fail_silently=False)
        return response
    message = "Undefined Interface"
    return err_response(message)
