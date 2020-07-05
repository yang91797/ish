from django.test import TestCase
import requests
from ish import settings
from django.http import JsonResponse
import base64
import json
# Create your tests here.
from wxapi import models

def test(request):
    resp = {'code': 200, 'msg': '上传成功', 'data': {}}
    print(request.body)
    print(str(request.body, 'utf8'))
    return JsonResponse(resp)


def msgSecCheck(content):
    """
    内容校验
    :param content:
    :return:
    """
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
    print(content, "?", type(content))
    access_token = access_token.json().get("access_token")
    content = {"content": content}
    content = json.dumps(content, ensure_ascii=False, ).encode("utf-8")
    print(content)
    res = requests.post(
        url='https://api.weixin.qq.com/wxa/msg_sec_check',
        params={
            "access_token": access_token
        },
        data=content

    )
    print(res.text)


# msgSecCheck("完2347全dfji试3726测asad感3847知qwez到")

# res = requests.post(
#     url="https://ishdf.com/wxapi/userinfo/check-reg/",
#
# )
# models.Customer.objects.filter(nid=596).delete()

