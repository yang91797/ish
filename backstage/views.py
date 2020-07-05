from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from wxapi import models as wxapi
from backstage import models
from rbac.service.init_permission import init_permission
from backstage.utils.geetest import GeetestLib
from django.contrib import auth
from django.http import JsonResponse
from backstage.utils import Myforms
import requests
from ish import settings
import datetime
# Create your views here.

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == "POST":
        response = {"user": None, "mag": None}
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE)
        validate = request.POST.get(gt.FN_VALIDATE)
        seccode = request.POST.get(gt.FN_SECCODE, "")
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id=user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            user_obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if user_obj:
                request.session['userInfo'] = {"id": user_obj.id, "name": user_obj.name}
                response['user'] = user_obj.username
                print("登录成功")
                # 权限信息初始化
                init_permission(user_obj, request)
                # return redirect('/stark/wxapi/article/list/')

            else:
                response['msg'] = "用户名或密码错误"
        return JsonResponse(response)

    return render(request, "login.html")

    # user = request.POST.get("user")
    # pwd = request.POST.get("pwd")
    # user_obj = models.User.objects.filter(username=user, password=pwd).first()
    # if not user_obj:
    #     return render(request, "login.html", {"msg": "用户名或密码错误"})
    # request.session['userInfo'] = {"id": user_obj.id, "name": user_obj.name}
    #
    # # 权限信息初始化
    # init_permission(user_obj, request)
    # return redirect("/stark/")


def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()

    return HttpResponse(response_str)


def register(request):
    """
    注册用户
    :param request:
    :return:
    """
    if request.is_ajax():
        form = Myforms.UserForm(request.POST)
        response = {"user": None, "msg": None}
        if form.is_valid():
            response["user"] = form.cleaned_data.get("user")

            # 生成用户
            user = form.cleaned_data.get("user")
            name = form.cleaned_data.get("name")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")

            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj
            models.UserInfo.objects.create(username=user, name=name, password=pwd, email=email, **extra)
        else:
            response["msg"] = form.errors

        return JsonResponse(response)
    form = Myforms.UserForm()
    return render(request, "register.html", {"form": form})


def logout(request):
    """
    注销登录
    :param request:
    :return:
    """
    if request.method == "GET":
        request.session.clear()
        return redirect("login/")


def datacube(request):
    """
    小程序数据统计
    :param request:
    :return:
    """
    for i in range(1, 31):

        dateTime = datetime.datetime.now() - datetime.timedelta(i)
        date = dateTime.strftime("%Y%m%d")
        print(date)
        access_token = request.session.get("access_token")
        if not access_token:
            get_access_token(request)
            access_token = request.session.get("access_token")

        response = requests.post(
            url="https://api.weixin.qq.com/datacube/getweanalysisappiddailyvisittrend?access_token=%s" % access_token,
            json={
                "begin_date": "20190317",
                "end_date": "20190317"
            }
        )
        dataText = response.json()
        print(
            dataText
        )
    return HttpResponse("hahha")


def get_access_token(request):
    """
    获取access_token
    :param request:
    :return:
    """
    # 19_4f8Ktlr96cVnUG9Ji5hDh_NYqW3jUZBxueSB5MXhTX3lTvdH9jq_dSpoVZftvnycqNor8LjHqvJETyiuQkAa8lh6tRezPOA_Xrj5vLxHDACDX1j8tAOJ2b_w3dIQZHfAEAJSA
    response = requests.get(
        url="https://api.weixin.qq.com/cgi-bin/token",
        params={
            "grant_type": "client_credential",
            "appid": settings.MINA_APP.get('appid'),
            "secret": settings.MINA_APP.get('appkey')
        }
    )
    text = response.json()
    print(text)
    request.session['access_token'] = text.get("access_token")
    request.session.setMaxInactiveInterval(7200)

def test(request):

    return render(request, "addInform.html")
