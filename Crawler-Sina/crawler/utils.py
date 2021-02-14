def preprocess(url: str):
    if url.startswith('//'):
        return 'https:' + url
    if url.startswith('http:'):
        return 'https:' + url[5:]
    return url


def setimage(news, image1, image2):
    if image1 is not None:
        news['image'] = preprocess(image1)
    elif image2 is not None:
        news['image'] = preprocess(image2)
    else:
        news['image'] = ''
    return news


def settitle(news, title1, title2, title3):
    if title1 is not None:
        news['title'] = title1
    elif title2 is not None:
        news['title'] = title2
    elif title3 is not None:
        news['title'] = title3
    return news


def settime(news, time1, time2, time3, time4):
    if time1 is not None:
        news['time'] = time1
    elif time2 is not None:
        if '+' in time2:
            news['time'] = time2[0:10] + ' ' + time2[11:19]
        else:
            news['time'] = time2
    elif time3 is not None:
        news['time'] = time3.strip()
    elif time4 is not None:
        news['time'] = time4.replace('年', '-').replace('月', '-').replace('日', '') + ':00'
    return news


def setsource(news, source1, source2):
    if source1 is not None:
        news['source'] = source1
    elif source2 is not None:
        news['source'] = source2
    else:
        news['source'] = ''
    return news
