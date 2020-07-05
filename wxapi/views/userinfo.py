from django.http import JsonResponse
import requests
from ish import settings
from wxapi import models
from wxapi.utils.tools import build_url, hs, SecCheck
import os


def login(request):
    """
    验证权限
    :param request:
    :return:
    """
    resp = {"code": 200, 'msg': '操作成功', 'data': {}}

    if request.method == 'POST':
        code = request.POST.get('code')

        if not code or len(code) < 1:
            resp['code'] = -1
            resp['msg'] = '需要code'
            return JsonResponse(resp)

        # https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code

        openid = get_openid(code)
        userInfo = models.Customer.objects.filter(openid=openid).values("username", "avatar", "sex", "openid", "asset",
                                                                                  "province", "city", "email", "status").first()

        if userInfo:
            if userInfo.get("status"):
                resp['msg'] = '已经绑定'
                resp['data'] = {'nickname': userInfo}
                request.session['user'] = openid
                return JsonResponse(resp)
            else:
                resp["code"] = 401
                resp["msg"] = '该账号因违规封禁'
                return JsonResponse(resp)
        username = request.POST.get('nickName')
        province = request.POST.get('province')
        city = request.POST.get('city')
        sex = request.POST.get('gender')
        avatar = request.POST.get('avatarUrl')
        user = models.Customer.objects.create(username=username, openid=openid, province=province,
                                              city=city, sex=sex, avatar=avatar)

        userInfo = {"nid": user.pk, "username": username, "avatar": avatar, "sex": sex, "province": province,
                    "city": city, "email": user.email, "asset": user.asset, "openid": openid}

        resp['msg'] = '注册成功'
        resp['data'] = userInfo
        return JsonResponse(resp)
    return JsonResponse(resp)


def get_openid(code):
    """
    获取openid
    :param code:
    :return:
    """
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (
        settings.MINA_APP.get('appid'), settings.MINA_APP.get('appkey'), code)

    res = requests.get(url=url)
    text = res.json()
    openid = text.get('openid')
    return openid


def check_reg(request):
    """
    启动小程序即验证是否注册过
    :param request:
    :return:
    """
    # print(request.META)       # 请求头
    resp = {"code": 200, 'msg': '用户已绑定', 'data': {}}
    code = request.POST.get('code')
    openid = request.META.get("HTTP_IDMD5")
    if not openid or openid == "0":
        openid = get_openid(code)

    userinfo = models.Customer.objects.filter(openid=openid).values("nid", "openid", "username",
                                                                              "avatar", "sex",
                                                                              "province", "city",
                                                                              "email", "asset", "status").first()
    print(userinfo, openid, "&&&&&&&")
    if userinfo:
        if userinfo.get("status"):
            request.session['user'] = openid
            resp['data'] = userinfo
            return JsonResponse(resp)
        else:
            resp["code"] = 401
            resp["msg"] = '该账号因违规封禁'
            return JsonResponse(resp)

    resp = {"code": 403, 'msg': '用户未绑定', 'data': {}}
    return JsonResponse(resp)


def change_user(request):
    """
    更改用户资料
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    openid = request.META.get("HTTP_IDMD5")
    oid = request.GET.get("oid")

    if request.method == "GET":
        if oid:
            user = models.Customer.objects.filter(openid=oid).values("username", "avatar", "sex",
                                                                                 "telephone", "email", "qq",
                                                                                 'wechat').first()
        else:
            user = models.Customer.objects.filter(nid=user_id, openid=openid).values("username", "avatar", "sex",
                                                                                 "telephone", "email", "qq",
                                                                                 'wechat').first()

        resp["data"] = user
        return JsonResponse(resp)
    # return JsonResponse(resp)
    username = request.POST.get("username")
    sex = request.POST.get("sex")

    telephone = request.POST.get("telephone")
    qq = request.POST.get("qq")
    wechat = request.POST.get("wechat")
    email = request.POST.get("email")
    img = request.FILES.get('avatar')
    check = SecCheck(request)
    if not check:
        resp["code"] = 405
        resp['msg'] = "内容具有敏感信息"

        userinfo = models.Customer.objects.filter(openid=openid, status=1).values("nid", "openid", "username",
                                                                                  "avatar", "sex",
                                                                                  "province", "city",
                                                                                  "email", "asset").first()
        return JsonResponse(resp)
    if img:
        path = os.path.join(settings.MEDIA_ROOT, "avatars", img.name)
        with open(path, 'wb') as f:
            for line in img:
                f.write(line)

        image = "avatars/" + img.name
        avatar = build_url(image)
        models.Customer.objects.filter(nid=user_id, openid=openid).update(avatar=avatar, username=username, sex=sex,
                                                                          telephone=telephone, qq=qq, wechat=wechat,
                                                                          email=email)

    else:
        models.Customer.objects.filter(nid=user_id, openid=openid).update(username=username, sex=sex,
                                                                          telephone=telephone, qq=qq, wechat=wechat,
                                                                          email=email)

    userinfo = models.Customer.objects.filter(openid=openid, status=1).values("nid", "openid", "username",
                                                                              "avatar", "sex",
                                                                              "province", "city",
                                                                              "email", "asset").first()
    resp['data'] = userinfo
    return JsonResponse(resp)