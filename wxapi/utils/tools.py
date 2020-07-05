from ish import settings
from urllib.parse import urljoin
import hashlib
from wxapi import models
from django.db.models import F, Q
import json
import requests
import time


def build_url(arg):
    if arg:
        url = urljoin(settings.URL + '/media/', arg+'/')
        return url


def hs(args):

    m = hashlib.md5()

    m.update(args.encode('utf8'))

    return m.hexdigest()


def saveFormId(request):
    """
    保存formId
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    openid = request.META.get("HTTP_IDMD5")
    expire = time.time() + 604800
    if request.method == "POST":
        formid = request.POST.get("formId")
    else:
        formid = request.GET.get("formId")

    print(formid, expire)
    models.Formid.objects.create(formid=formid, user_id=user_id, expire=expire)


def read_update(nid):
    """
    阅读数量的更新
    :return:
    """
    models.Article.objects.filter(status=1, nid=nid).update(read_count=F("read_count") + 1)


def SecCheck(request):
    """
    内容校验
    :param request:
    :return:
    """
    check = True
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        settings.MINA_APP.get('appid'), settings.MINA_APP.get('appkey'))
    access_token = requests.get(
        url=url,
        headers={
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://mp.weixin.qq.com/debug/cgi-bin/apiinfo?t=index&type=%E5%9F%BA%E7%A1%80%E6%94%AF%E6%8C%81&form=%E8%8E%B7%E5%8F%96access_token%E6%8E%A5%E5%8F%A3%20/token&token=&lang=zh_CN',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3676.400 QQBrowser/10.4.3505.400',

        },
    )

    access_token = access_token.json().get("access_token")
    img = request.FILES.get('images')         # 上传的图片
    content = request.POST.get('content')       # 上传的内容

    username = request.POST.get("username")         # 修改用户信息上传的内容
    sex = request.POST.get("sex")
    telephone = request.POST.get("telephone")
    qq = request.POST.get("qq")
    wechat = request.POST.get("wechat")
    email = request.POST.get("email")

    desc = request.POST.get("desc")         # 跑腿信息校验
    kg = request.POST.get("kg")
    price = request.POST.get("price")
    site = request.POST.get("site")
    outdate = request.POST.get("outdate")

    if content:
        res = msgSecCheck(access_token, content)
        if res.get("errcode") == 87014:
            check = False

    if img:
        res = imgSecCheck(access_token, img)
        if res.get("errcode") == 87014:
            check = False

    if username or sex or telephone or qq or wechat or email:
        userinfo = username + sex + telephone + qq + wechat + email
        res = msgSecCheck(access_token, userinfo)
        if res.get("errcode") == 87014:
            check = False

    if desc or kg or price or site or outdate:
        content = desc + kg + price + site + outdate
        res = msgSecCheck(access_token, content)
        if res.get("errcode") == 87014:
            check = False
    return check


def imgSecCheck(access_token, img):
    """
    图片鉴别
    :param content:
    :return:
    """
    content = b""
    for line in img:
        content += line
    res = requests.post(
        url="https://api.weixin.qq.com/wxa/img_sec_check?access_token=%s" % access_token,
        files={
            "media": content
        }
    )
    print(res.text)
    return res.json()


def msgSecCheck(access_token, content):
    """
    内容校验
    :param content:
    :return:
    """

    content = {"content": content}
    content = json.dumps(content, ensure_ascii=False, ).encode("utf-8")
    res = requests.post(
        url='https://api.weixin.qq.com/wxa/msg_sec_check?access_token=%s' % access_token,
        data=content
    )
    print(res.text)
    return res.json()

