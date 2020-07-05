from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import requests
from ish import settings
from wxapi import models
from wxapi.utils.tools import build_url, hs
from django.db import transaction
from django.db.models import F, Q
from django.db.models import Count
import datetime
import os
import jieba
import threading
import time


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
        userinfo = models.Customer.objects.filter(openid=openid, status=1).values("username", "avatar", "sex", "openid",
                                                                                  "province", "city", "email").first()

        if userinfo:
            resp['msg'] = '已经绑定'
            resp['data'] = {'nickname': userinfo}
            request.session['user'] = openid

            return JsonResponse(resp)
        username = request.POST.get('nickName')
        province = request.POST.get('province')
        city = request.POST.get('city')
        sex = request.POST.get('gender')
        avatar = request.POST.get('avatarUrl')
        user = models.Customer.objects.create(username=username, openid=openid, province=province,
                                              city=city, sex=sex, avatar=avatar)

        userinfo = {"nid": user.pk, "username": username, "avatar": avatar, "sex": sex, "province": province,
                    "city": city, "email": user.email, "asset": user.asset}

        resp['msg'] = '注册成功'
        resp['data'] = userinfo
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

    openid = get_openid(request.POST.get('code'))
    userinfo = models.Customer.objects.filter(openid=openid, status=1).values("nid", "openid", "username",
                                                                              "avatar", "sex",
                                                                              "province", "city",
                                                                              "email", "asset").first()

    if userinfo:
        resp = {"code": 200, 'msg': '用户已绑定', 'data': userinfo}
        request.session['user'] = openid
        # login(request, openid)
        return JsonResponse(resp)
    request.session['user'] = 'ouuau'
    resp = {"code": 403, 'msg': '用户未绑定', 'data': {}}
    return JsonResponse(resp)


def index(request):
    """
    首页
    :param request:
    :return:
    """
    info_list = []
    article_list = []
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    page_size = 20

    if request.method == 'POST':
        category_id = request.POST.get('cat_id')
        p = int(request.POST.get('p'))

        if not category_id or category_id == '1':
            article_info = models.Article.objects.filter(status=1).values('nid', 'title', 'desc', 'create_time',
                                                                          'comm_count', 'up_count',
                                                                          'category__title', 'user__avatar',
                                                                          'user__username').order_by("-weight",
                                                                                                     "-create_time")[
                           page_size * (p + 1):page_size * (p + 1) + page_size]
        else:
            article_info = models.Article.objects.filter(status=1, category=category_id).values('nid', 'title', 'desc',
                                                                                                'create_time',
                                                                                                'comm_count',
                                                                                                'up_count',
                                                                                                'category__title',
                                                                                                'user__avatar',
                                                                                                'user__username').order_by(
                "-weight", "-nid")[page_size * (p + 1):page_size * (p + 1) + page_size]

        # p=0 n=2 [2,4]         p=1   [4, 6]
        # p=0  n=5 [5, 10]    p=1   [10:15]
        # 总结规律：每页取n个，取第p页则，    [n*(p+1), n*(p+1)+n]
        for item in article_info:
            date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
            item["create_time"] = date
            image = models.Article.objects.filter(nid=item.get("nid")).values("img__image").first()
            if image.get("img__image") and image.get("img__image") != "undefined":
                item["img__image"] = build_url('images/' + image.get("img__image"))

        resp['data']['article'] = list(article_info)
        resp['data']['has_more'] = 0 if len(article_list) < page_size else 1

        return JsonResponse(resp)

    category_id = request.GET.get('cat_id')
    if not category_id or category_id == '1':
        ad_info = models.Advertise.objects.filter(status=1, place='0').all().values('nid', 'title', 'images', 'url',
                                                                                    'content')
        article_info = models.Article.objects.filter(status=1).values('nid', 'title', 'desc', 'create_time',
                                                                      'comm_count', 'up_count', 'category__title',
                                                                      'user__avatar',
                                                                      'user__username').order_by("-weight",
                                                                                                 "-nid")[
                       0: page_size]

        for item in ad_info:
            item["pic_url"] = build_url('advertise/' + item.get('images'))

        resp['data']['advertise'] = list(ad_info)
        category_list = list(models.Category.objects.all().values('nid', 'title'))
        resp['data']['category'] = category_list

    else:
        t1 = threading.Thread(target=saveFormId, args=(request,))
        t1.start()
        article_info = models.Article.objects.filter(status=1, category=category_id).values('nid', 'title', 'desc',
                                                                                            'create_time',
                                                                                            'comm_count', 'up_count',
                                                                                            'category__title',
                                                                                            'user__avatar',
                                                                                            'user__username').order_by(
            "-weight", "-create_time")[0: page_size]

    for item in article_info:
        date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
        item["create_time"] = date
        image = models.Article.objects.filter(nid=item.get("nid")).values("img__image").first()
        if image.get("img__image") and image.get("img__image") != "undefined":
            item["img__image"] = build_url('images/' + image.get("img__image"))

    resp['data']['article'] = list(article_info)

    return JsonResponse(resp)


def category(request):
    """
    查看文章分类
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}

    category_list = list(models.Category.objects.all().values('nid', 'title'))
    resp['data'] = category_list

    return JsonResponse(resp)


def details(request):
    """
    查看文章详情
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "POST":  # 查看回复评论
        comment_list = []
        cid = request.POST.get("cid")
        comment_queryset = models.Comment.objects.filter(status=1, ancestor=cid).values('nid', 'user_id', "user__openid",
                                                                                        'user__username',
                                                                                        'user__avatar', 'content',
                                                                                        'create_time', 'parent_comment',
                                                                                        'like_count', 'reply_count',
                                                                                        'ancestor', 'parent_comment__user__openid',
                                                                                        'parent_comment__user__username',
                                                                                        'parent_comment__user__avatar')

        for item in comment_queryset:
            item["create_time"] = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
            comment_list.append(item)
        resp['data'] = comment_list

        return JsonResponse(resp)

    article_id = request.GET.get('article_id')
    user_id = request.META.get('HTTP_AUTHORIZATION')

    t = threading.Thread(target=read_update, args=(article_id,))
    t.start()
    article = models.Article.objects.filter(status=1, nid=article_id).values('nid', 'title', 'content', 'create_time',
                                                                             'img__image', 'comm_count', 'up_count',
                                                                             'read_count', 'user__username', 'user__openid',
                                                                             'user__avatar', 'category__title',
                                                                             'category_id', 'type', 'study_url__gold')
    study_Link = models.Buy.objects.filter(user_id=user_id, study=article_id).values(
        'study__study_url__study_url').first()

    likeUp = models.ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).values("is_up").first()
    likeUp = False if not likeUp or not likeUp.get("is_up") else True

    resp['data']['likeUp'] = likeUp
    if study_Link:
        resp['data']['study_url'] = study_Link.get("study__study_url__study_url")
    else:
        resp['data']['study_url'] = None
    collect = models.Trove.objects.filter(user_id=user_id, article_id=article_id).values("pk").first()
    resp['data']['collect'] = collect

    comment = models.Comment.objects.filter(article_id=article_id, status=1, parent_comment_id__isnull=True).order_by(
        "-pk").values('nid', 'user_id', 'user__openid', 'user__username', 'user__avatar', 'parent_comment', 'reply_count', "ancestor",
                      'content', 'create_time')

    commentId = [i.get("nid") for i in comment]
    commentImage = models.CommentImage.objects.filter(commentId__in=commentId).values("commentId", "image__image")

    commentImage_dic = {}
    for item in commentImage:
        url = build_url('images/' + item.get('image__image') + '/')
        if item.get("commentId") in commentImage_dic:
            commentImage_dic[item.get("commentId")].append(url)
        else:
            commentImage_dic[item.get("commentId")] = [url]

    comment_list = []
    for item in comment:
        item['commentImage'] = commentImage_dic.get(item.get("nid"))
        item['create_time'] = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
        comment_list.append(item)

    images = ['images/' + i['img__image'] + '/' for i in article if i['img__image']]
    images = list(map(build_url, images))
    article = article.first()
    date = datetime.datetime.strftime(article.get('create_time'), "%Y-%m-%d %H:%M")

    resp['data']['article'] = article
    resp['data']['article']['create_time'] = date
    resp['data']['article']['img'] = images

    resp['data']['comment'] = comment_list
    return JsonResponse(resp)


def read_update(nid):
    """
    阅读数量的更新
    :return:
    """
    models.Article.objects.filter(status=1, nid=nid).update(read_count=F("read_count") + 1)


def search(request):
    """
    搜索信息
    :param request:
    :return:
    """
    # django.contrib.sessions.middleware.SessionMiddleware
    # from django.contrib.sessions.middleware import SessionMiddleware
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    searchTitle = request.POST.get("searchTitle")
    formId = request.POST.get("formId")
    expire = request.POST.get("expire")
    print(formId, expire)
    content = jieba.lcut(searchTitle)
    print(content)
    result = []
    for keyword in content:
        if len(keyword) > 1:
            title_result = models.Article.objects.filter(status=1, title__icontains=keyword).values('nid', 'title',
                                                                                                    'desc',
                                                                                                    'create_time',
                                                                                                    'comm_count',
                                                                                                    'up_count',
                                                                                                    'category__title',
                                                                                                    'user__avatar',
                                                                                                    'user__username',
                                                                                                    'user__openid').order_by(
                "-create_time")
            content_result = models.Article.objects.filter(status=1, content__icontains=keyword).values('nid', 'title',
                                                                                                        'desc',
                                                                                                        'create_time',
                                                                                                        'comm_count',
                                                                                                        'up_count',
                                                                                                        'category__title',
                                                                                                        'user__avatar',
                                                                                                        'user__username').order_by(
                "-create_time")

            for item in title_result:
                date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
                item['create_time'] = date
                if item not in result:
                    result.append(item)
            for item in content_result:
                date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
                item['create_time'] = date
                if item not in result:
                    result.append(item)

    print(result, "")
    resp['data'] = result

    return JsonResponse(resp)


def advertise(request):
    """
    宣传位
    :param request: 
    :return: 
    """
    resp = {}
    return JsonResponse(resp)


def create(request):
    """
    添加文章
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}

    user_id = request.META.get('HTTP_AUTHORIZATION')
    title = request.POST.get('title')
    content = request.POST.get('content')
    img_url = request.POST.get('images')
    types = request.POST.get('type')
    category_id = request.POST.get('category')
    study_url = request.POST.get('study_url')
    gold = request.POST.get('gold')

    t1 = threading.Thread(target=saveFormId, args=(request, ))
    t1.start()
    desc = content[0:30] + '......' if len(content) > 30 else content

    with transaction.atomic():
        if study_url != "undefined":
            link = models.StudyLink.objects.create(study_url=study_url, gold=gold)
            obj = models.Article.objects.create(title=title, desc=desc, content=content, type=types,
                                                user_id=user_id, category_id=category_id, study_url_id=link.pk)
        else:
            obj = models.Article.objects.create(title=title, desc=desc, content=content, type=types,
                                                user_id=user_id, category_id=category_id)

        if img_url:
            img_list = img_url.split(',')
            for img in img_list:
                res = models.Image.objects.create(image=img)

                obj.img.add(res.nid)
    # else:
    #     models.Article.objects.create(title=title, desc=desc, content=content, type=types, user_id=user_id,
    #                                   category_id=category_id)

    return JsonResponse(resp)


def upload(request):
    """
    接收上传的图片
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}

    img = request.FILES.get('file')
    path = os.path.join(settings.MEDIA_ROOT, "images", img.name)
    with open(path, 'wb') as f:
        for line in img:
            f.write(line)
    resp['data'] = img.name
    return JsonResponse(resp)


def comment(request):
    """
    添加评论
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    openid = request.META.get("HTTP_IDMD5")
    article_id = request.POST.get('article_id')
    comment = request.POST.get('content')
    commentUserId = request.POST.get("commentUserId")
    # formId = request.POST.get("formId")
    types = request.POST.get('type')
    images = request.POST.get("images")

    t1 = threading.Thread(target=saveFormId, args=(request,))
    t1.start()

    articleUser = models.Article.objects.filter(nid=article_id).values("user_id", "user__openid").first()
    if types:  # 回复评论
        comment_id = request.POST.get('comment_id')
        ancestor = request.POST.get('ancestor')
        comment_user = models.Customer.objects.filter(nid=commentUserId).values("openid", "username").first()
        with transaction.atomic():
            obj = models.Comment.objects.create(article_id=article_id, user_id=user_id, content=comment,
                                                parent_comment_id=comment_id, ancestor_id=ancestor)
            models.Article.objects.filter(pk=article_id).update(comm_count=F("comm_count") + 1)
            models.Comment.objects.filter(pk=comment_id).update(reply_count=F("reply_count") + 1)

            if comment_id != ancestor:      # 回复
                models.Comment.objects.filter(pk=ancestor).update(reply_count=F("reply_count") + 1)

            if user_id != commentUserId:

                models.Msg.objects.create(user_id=user_id, article_id=article_id, commentUserId_id=commentUserId,
                                          commentId=obj, describe=comment)
                # t1 = threading.Thread(target=send_serve,
                #                       args=(request, comment_user.get("openid"),
                #                             article_id,
                #                             "您评论的内容",
                #                             comment,
                #                             time.strftime('%Y-%m-%d %H:%M')
                #                             ))
                # t1.start()

        return JsonResponse(resp)

    articleUserId = articleUser.get("user_id")

    with transaction.atomic():

        if images:
            img_list = images.split(',')
            obj = models.Comment.objects.create(article_id=article_id, user_id=user_id, content=comment)
            models.Article.objects.filter(pk=article_id).update(comm_count=F("comm_count") + 1)
            des = ""
            for img in img_list:
                res = models.Image.objects.create(image=img)
                models.CommentImage.objects.create(commentId=obj, image=res)
                des = des + "[[图片]]"

            if int(user_id) != articleUserId and comment == "null":
                models.Msg.objects.create(user_id=user_id, article_id=article_id,
                                          commentUserId_id=articleUserId, commentId=obj,
                                          describe=des)
                # t = threading.Thread(target=send_serve,
                #                      args=(request, articleUser.get("user__openid"),
                #                            article_id,
                #                            "您发布的内容",
                #                            des,
                #                            time.strftime('%Y-%m-%d %H:%M')
                #                            ))
                # t.start()
        else:
            obj = models.Comment.objects.create(article_id=article_id, user_id=user_id, content=comment)
            models.Article.objects.filter(pk=article_id).update(comm_count=F("comm_count") + 1)

            if int(user_id) != articleUserId:
                models.Msg.objects.create(user_id=user_id, article_id=article_id, commentUserId_id=articleUserId,
                                          commentId=obj, describe=comment)

                print(articleUser.get("user__openid"), article_id, comment, str(time.strftime('%Y-%m-%d')))
                # t = threading.Thread(target=send_serve,
                #                      args=(request, articleUser.get("user__openid"),
                #                            article_id,
                #                            "您发布的内容",
                #                            comment,
                #                            time.strftime('%Y-%m-%d %H:%M'),
                #                            ))
                # t.start()

    return JsonResponse(resp)


def send_teleplate(request, openid, article, keyword2, keyword3, keyword4):
    """
    发送模板消息
    :return:
    """
    user_id = request.META.get('HTTP_AUTHORIZATION')
    user_openid = request.META.get("HTTP_IDMD5")
    expire_list = models.Formid.objects.filter(user_id=user_id).values("id", "expire")
    now_date = time.time()
    username = models.Customer.objects.filter(nid=user_id, openid=openid).values("username").first()
    keyword1 = username.get("username")
    for item in expire_list:
        if float(item.get("expire")) < float(now_date):
            models.Formid.objects.filter(id=item.get("id")).delete()
    formId = models.Customer.objects.filter(openid=openid).values("formid__formid").first().get("formid__formid")

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
    response = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=%s" % access_token,
        json={
            "touser": openid,
            "template_id": "DN8O2wAjWDh_VxuGMntC7xk_3lNBUj31k5IBP8eqAdQ",
            "page": "pages/detail/detail?id=%s" % article,
            "form_id": formId,
            "data": {
                "keyword1": {
                    "value": keyword1
                },
                "keyword2": {
                    "value": keyword2
                },
                "keyword3": {
                    "value": keyword3
                },
                "keyword4": {
                    "value": keyword4
                }
            }
        }
    )

    models.Formid.objects.filter(formid=formId).delete()
    print(response.json())


def send_serve(request, openid, article, keyword2, keyword3, keyword4):
    """
    发送服务消息
    :param request:
    :return:
    """
    user_id = request.META.get('HTTP_AUTHORIZATION')
    user_openid = request.META.get("HTTP_IDMD5")
    expire_list = models.Formid.objects.filter(user_id=user_id).values("id", "expire")
    now_date = time.time()
    username = models.Customer.objects.filter(nid=user_id, openid=user_openid).values("username").first()
    keyword1 = username.get("username")
    for item in expire_list:
        if float(item.get("expire")) < float(now_date):
            models.Formid.objects.filter(id=item.get("id")).delete()
    formId = models.Customer.objects.filter(openid=openid).values("formid__formid").first().get("formid__formid")

    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
        settings.MINA_APP.get('appid'), settings.MINA_APP.get('appkey'))
    access_token = requests.get(
        url=url
    )

    access_token = access_token.json().get("access_token")
    response = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/wxopen/template/uniform_send?access_token=%s" % access_token,
        json={
            "touser": openid,
            "weapp_template_msg": {
                "template_id": "DN8O2wAjWDh_VxuGMntC7xk_3lNBUj31k5IBP8eqAdQ",
                "page": "pages/detail/detail?id=%s" % article,
                "form_id": formId,
                "data": {
                    "keyword1": {
                        "value": keyword1
                    },
                    "keyword2": {
                        "value": keyword2
                    },
                    "keyword3": {
                        "value": keyword3
                    },
                    "keyword4": {
                        "value": keyword4
                    }
                },

            },
        }
    )
    models.Formid.objects.filter(formid=formId).delete()
    print(response.json())


def like(request):
    """
    点赞
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    article_id = request.GET.get('nid')
    user_id = request.META.get('HTTP_AUTHORIZATION')
    likeUp = models.ArticleUpDown.objects.filter(article_id=article_id, user_id=user_id).values("is_up").first()

    with transaction.atomic():
        if not likeUp:
            models.ArticleUpDown.objects.create(user_id=user_id, article_id=article_id)
            models.Article.objects.filter(nid=article_id, status=1).update(up_count=F("up_count") + 1)
        elif likeUp.get("is_up"):
            models.ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).update(is_up=False)
            models.Article.objects.filter(nid=article_id).update(up_count=F("up_count") - 1)
        else:
            models.ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).update(is_up=True)
            models.Article.objects.filter(nid=article_id, status=1).update(up_count=F("up_count") + 1)

    return JsonResponse(resp)


def study_link(request):
    """
    学习资料链接
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    article_id = request.GET.get('article_id')
    user_buy_id = request.META.get('HTTP_AUTHORIZATION')
    study_url = models.Article.objects.filter(status=1, nid=article_id).values('study_url__study_url', 'user',
                                                                               'study_url__gold').first()
    asset = models.Customer.objects.filter(pk=user_buy_id).values('asset').first().get('asset')

    with transaction.atomic():
        surplus = asset - study_url.get('study_url__gold')
        if surplus < 0:
            resp['code'] = 403
            resp['msg'] = '金币不足'
            return JsonResponse(resp)
        user_buy = models.Customer.objects.filter(pk=user_buy_id).update(asset=surplus)
        models.Customer.objects.filter(pk=study_url.get('user')).update(
            asset=F("asset") + study_url.get('study_url__gold'))
        models.Buy.objects.create(user_id=user_buy_id, study_id=article_id)
        if int(user_buy_id) != study_url.get('user'):
            models.Msg.objects.create(user_id=user_buy_id, commentUserId_id=study_url.get('user'),
                                      article_id=article_id,
                                      describe="有人打赏了分享的资料，金币 +%s" % study_url.get('study_url__gold'))
        resp['data'] = study_url.get('study_url__study_url')
    return JsonResponse(resp)


def sign(request):
    """
    签到
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    date = str(datetime.datetime.now()).split(' ')[0]
    user_id = request.META.get('HTTP_AUTHORIZATION')
    user = list(models.Sign.objects.filter(user_id=user_id).order_by("-pk").values("create_time")[:7])
    t1 = threading.Thread(target=saveFormId, args=(request,))
    t1.start()

    if user:
        date_record = datetime.datetime.strftime(user[0].get("create_time"), '%Y-%m-%d')

        if date != date_record:
            with transaction.atomic():
                models.Sign.objects.create(user_id=user_id)
                models.Customer.objects.filter(nid=user_id).update(asset=F("asset") + 5)
                models.Msg.objects.create(user_id=user_id, commentUserId_id=user_id, describe="签到成功！金币 +5")
                return JsonResponse(resp)

    else:
        with transaction.atomic():
            models.Sign.objects.create(user_id=user_id)
            models.Customer.objects.filter(nid=user_id).update(asset=F("asset") + 5)
            models.Msg.objects.create(user_id=user_id, commentUserId_id=user_id, describe="签到成功！金币 +5")
            return JsonResponse(resp)
    resp['code'] = 403
    return JsonResponse(resp)


def collect(request):
    """
    收藏
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    if request.method == "POST":
        article_id = request.POST.get("articleId")
        collectIf = models.Trove.objects.filter(user_id=user_id, article_id=article_id).first()
        if collectIf:
            collectIf.delete()
        else:
            models.Trove.objects.create(user_id=user_id, article_id=article_id)
        return JsonResponse(resp)
    userCollect = models.Trove.objects.filter(user_id=user_id).values("article")
    collectList = [i.get("article") for i in userCollect]
    articleQuery = models.Article.objects.filter(status=1, pk__in=collectList).values('nid', 'title', 'desc',
                                                                                      'create_time',
                                                                                      'comm_count',
                                                                                      'up_count',
                                                                                      'category__title',
                                                                                      'user__avatar',
                                                                                      'user__username').order_by(
        "-create_time")

    article_list = []
    for item in articleQuery:
        date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
        article = {
            'id': item.get('nid'),
            'title': item.get('title'),
            'desc': item.get('desc'),
            'create_time': date,
            'comm_count': item.get('comm_count'),
            'up_count': item.get('up_count'),
            'category': item.get('category__title'),
            'view': 0,
            'username': item.get('user__username'),
            'avatar': item.get('user__avatar')
        }
        article_list.append(article)
    resp['data'] = article_list
    return JsonResponse(resp)


def reply(request):
    """
    查看个人回复
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')

    replyQuerySet = models.Comment.objects.filter(user_id=user_id, status=1).values("nid", "content", "create_time",
                                                                                    "article__nid",
                                                                                    "article__title", "article__desc",
                                                                                    "article__comm_count",
                                                                                    "article__up_count").order_by(
        "-create_time")
    replyList = []
    for item in replyQuerySet:
        t = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
        item['create_time'] = t
        replyList.append(item)

    resp['data'] = replyList

    return JsonResponse(resp)


def publish(request):
    """
    查看个人发布
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    page_size = 20
    p = request.GET.get('p')
    if not p:
        p = -1

    article = models.Article.objects.filter(user_id=user_id, status=1).values('nid', 'title', 'desc',
                                                                              'create_time',
                                                                              'comm_count',
                                                                              'up_count',
                                                                              'category__title',
                                                                              'user__avatar',
                                                                              'user__username').order_by(
        "-create_time")[page_size * (p + 1):page_size * (p + 1) + page_size]
    for item in article:
        date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
        item['create_time'] = date
    resp['data'] = list(article)
    return JsonResponse(resp)


def storage(request):
    """
    查看是否需要更新小程序数据
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {"event1": None, "event2": None}}
    data_type1 = request.GET.get("event1")
    data_type2 = request.GET.get("event2")
    if data_type1:
        event1 = get_last(data_type1)
        resp['data']['event1'] = event1
    if data_type2:
        event2 = get_last(data_type2)
        resp["data"]['event2'] = event2
    return JsonResponse(resp)


def get_last(meter):
    """
    查询表的最后一个id
    :param meter:
    :return:
    """
    pk = eval('models.%s.objects.filter(status=1).values("pk").last()' % meter)
    if pk:
        pk = pk.get("pk")
    return pk


def delete(request):
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    types = request.POST.get("type")

    if types == "reply":
        with transaction.atomic():
            commentId = request.POST.get("commentId")
            res = models.Comment.objects.filter(nid=commentId, user_id=user_id).values("parent_comment",
                                                                                       "article")  # comm_count=F("comm_count") + 1
            res.update(status=-1)
            models.Msg.objects.filter(user_id=user_id, article_id=res.first().get("article"),
                                      commentId_id=commentId).update(status=0)
            models.Comment.objects.filter(nid=res.first().get("parent_comment")).update(
                reply_count=F("reply_count") - 1)
            models.Article.objects.filter(nid=res.first().get("article")).update(comm_count=F("comm_count") - 1)
            return JsonResponse(resp)
    elif types == "publish":
        articleId = request.POST.get("articleId")
        models.Article.objects.filter(nid=articleId, user_id=user_id).update(status=0)
        return JsonResponse(resp)


def msg(request):
    """
    用户通知
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {'msg': False, 'sign': False}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    date = str(datetime.datetime.now()).split(' ')[0]
    if request.method == "GET":
        print(user_id, "??")
        info = models.Msg.objects.filter(commentUserId_id=user_id, read=1, status=1).values("describe").first()
        user = list(models.Sign.objects.filter(user_id=user_id).order_by("-pk").values("create_time")[:7])

        if user:
            date_record = datetime.datetime.strftime(user[0].get("create_time"), '%Y-%m-%d')
            if date == date_record:
                resp['data']['sign'] = True

        if info:
            resp['data']['msg'] = True

        return JsonResponse(resp)
    models.Msg.objects.filter(commentUserId_id=user_id, read=1, status=1).update(read=0)
    info = models.Msg.objects.filter(commentUserId_id=user_id, status=1).values("user__username", "user__openid", "user__avatar",
                                                                                "article_id", "article__desc",
                                                                                "describe", "create_time").order_by(
        "-create_time")[0:30]
    for item in info:
        date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
        item['create_time'] = date
    resp['data'] = list(info)
    return JsonResponse(resp)


def inform(request):
    """
    小程序使用申明
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    data = models.Inform.objects.filter(status=1).values("content").order_by("-create_time").first()
    resp['data'] = data
    return JsonResponse(resp)


def report(request):
    """
    举报
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}

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
    username = request.POST.get("username")
    sex = request.POST.get("sex")

    telephone = request.POST.get("telephone")
    qq = request.POST.get("qq")
    wechat = request.POST.get("wechat")
    email = request.POST.get("email")
    img = request.FILES.get('avatar')

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

    return JsonResponse(resp)


def test(request):
    """
    接口测试
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}

    from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage
    # current_page = request.GET.get('page')

    # article_info = models.Article.objects.filter(status=1).values('nid', 'title', 'desc', 'create_time',
    #                                                               'img', 'comm_count', 'up_count',
    #                                                               'category__title', 'user__avatar', 'user__username')[
    #                0:2]
    #
    # for item in article_info:
    #     # print(item)
    #     date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
    #
    #     article = {
    #         'id': item.get('nid'),
    #         'title': item.get('title'),
    #         'desc': item.get('desc'),
    #         'create_time': item.get('create_time'),
    #         'img': item.get('img'),
    #         'comm_count': item.get('comm_count'),
    #         'up_count': item.get('up_count'),
    #         'category': item.get('category__title'),
    #         'username': item.get('user__username'),
    #         'avatar': item.get('user__avatar')
    #     }
        # print(article)
    time.sleep(10)
    return JsonResponse(resp)
