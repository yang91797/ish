from django.http import JsonResponse
from pyquery import PyQuery
from ish import settings
from wxapi.utils.tools import build_url, hs, saveFormId
from wxapi import models
import requests
import os
import threading
import datetime
import time


def jou(request):
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    openid = request.META.get("HTTP_IDMD5")
    all_cookie_dict = {}

    try:
        if request.method == "GET":
            user_obj = models.Customer.objects.filter(openid=openid).values("student_number").first()
            auth = request.GET.get("auth")
            if not user_obj.get("student_number") and auth == "auth":
                resp["code"] = 401
                return JsonResponse(resp)
            elif user_obj.get("student_number") and auth == "auth":
                return JsonResponse(resp)
            proxy = ip()
            index = requests.get(
                url="http://zfxk.hhit.edu.cn/(ltlvfe554be2ev45xntowi35)/default2.aspx",
                timeout=10,
                headers={
                    "Host": "zfxk.hhit.edu.cn",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
                },
                proxies=proxy
            )
            all_cookie_dict.update(index.cookies.get_dict())
            print(index.text)

            html = PyQuery(index.text)
            form1 = html('#form1 input').attr('value')
            print(form1)

            # 获得验证码
            CheckCode = requests.get(
                url="http://zfxk.hhit.edu.cn/(ltlvfe554be2ev45xntowi35)/CheckCode.aspx",
                timeout=10,
                headers={
                    "Host": "zfxk.hhit.edu.cn",
                    "Referer": "http://zfxk.hhit.edu.cn/(ltlvfe554be2ev45xntowi35)/default2.aspx",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
                },
                cookies=all_cookie_dict,
                proxies=proxy
            )
            path = os.path.join(settings.MEDIA_ROOT, "code", "%s.jpg" % openid)
            with open(path, 'wb') as f:
                f.write(CheckCode.content)
            url_path = build_url('code/%s.jpg' % openid)
            resp['data']['rsa'] = form1
            resp['data']["code"] = url_path
            return JsonResponse(resp)
        user = request.POST.get("user")
        password = request.POST.get("pwd")
        code = request.POST.get("code")
        form1 = request.POST.get("rsa")

        t1 = threading.Thread(target=saveFormId, args=(request,))
        t1.start()
        proxy = ip()
        login = requests.post(
            url="http://zfxk.hhit.edu.cn/(ltlvfe554be2ev45xntowi35)/default2.aspx",
            timeout=10,
            data={
                "__VIEWSTATE": form1,
                "txtUserName": user,
                "Textbox1": "",
                "TextBox2": password,
                "txtSecretCode": code,
                "RadioButtonList1": "(unable to decode value)",
                "Button1": "",
                "lbLanguage": "",
                "hidPdrs": "",
                "hidsc": "",
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Host": "zfxk.hhit.edu.cn",
                "Origin": "http://zfxk.hhit.edu.cn",
                "Referer": "http://zfxk.hhit.edu.cn/(ltlvfe554be2ev45xntowi35)/default2.aspx",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400"
            },
            allow_redirects=False,
            proxies=proxy
        )

        login_redirect = requests.get(
            url="http://zfxk.hhit.edu.cn/(ltlvfe554be2ev45xntowi35)/xs_main.aspx?xh=%s" % user,
            timeout=10,
            headers={
                "Host": "zfxk.hhit.edu.cn",
                "Referer": "http://zfxk.hhit.edu.cn/(ltlvfe554be2ev45xntowi35)/default2.aspx",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400"

            },
            proxies=proxy
        )
        print(login.text, "***")
        print(login_redirect.text)
        print(proxy)
        login_html = PyQuery(login_redirect.text)
        Label3 = login_html("#Label3").text()
        username = login_html("#xhxm").text()
        if Label3 == "欢迎您：":
            print("登录成功", resp)

            username = username.replace("同学", "")
            models.Customer.objects.filter(openid=openid).update(student_number=user, name=username)
            return JsonResponse(resp)
        else:
            resp['code'] = 400
            return JsonResponse(resp)
    except requests.exceptions.ReadTimeout as e:
        print(e)
        # getIp()
        return jou(request)
    except requests.exceptions.ConnectTimeout as e:
        print(e)
        # getIp()
        return jou(request)


def getIp():
    """
    获取ip
    :param count:
    :return:
    """
    url = "http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&groupid=0&qty=1&time=6&pro=&city=&port=1&format=json&ss=5&css=&ipport=1&et=1&pi=1&co=1&dt=1&specialTxt=3&specialJson=&usertype=2"

    try:
        res = requests.get(
            url="http://http.zhiliandaili.cn/Users-whiteIpAddNew.html?appid=3802&appkey=a2792cf6bf201ec00878b40de918cfcb&whiteip=47.105.44.64,47.100.57.249,49.94.143.215",
            timeout=5
        )
        response = requests.get(
            url=url,
            timeout=10,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6799.400 QQBrowser/10.3.2908.400',
                'Upgrade-Insecure-Requests': '1'
            }
        )
        ip_dict = response.json()
        print(ip_dict)

        return ip_dict.get('data')[0].get("IP")
    except Exception as e:

            getIp()


def ip():
    now_date = time.strftime('%Y-%m-%d', )
    ip_info = models.IpRecord.objects.filter(status=1).values("ip", "create_time")
    if ip_info:
        ip_first = ip_info.first()
        date = ip_first.get("create_time")
        date = str(date).split(maxsplit=1)[0]

        if date == now_date:
            ip = ip_first.get("ip")
        else:
            ip = getIp()
            ip_info.update(status=0)
            models.IpRecord.objects.create(ip=ip)
    else:
        ip = getIp()
        models.IpRecord.objects.create(ip=ip)

    return {
        'http': 'http://%s' % ip,
        'https': 'https://%s' % ip
    }


