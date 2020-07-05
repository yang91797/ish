from wxapi import models
from django.http import JsonResponse
from wxapi.utils.tools import build_url, hs, saveFormId
import datetime
import jieba
import threading


def advertise(request):
    """
    首页
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    openid = request.META.get("HTTP_IDMD5")
    if request.method == "POST":
        nid = request.POST.get("nid")

        ad_detail = models.Advertise.objects.filter(status=1, nid=nid).values("nid", "title", "content").first()
        ad_detail_image = models.AdImage.objects.filter(status=1, ad=ad_detail.get("nid")).values("image")
        ad_image = []
        for item in ad_detail_image:
            ad_image.append(build_url('advertise/' + item.get("image")))

        resp['data']['ad_detail'] = ad_detail
        resp["data"]["ad_image"] = ad_image
        return JsonResponse(resp)
    ad_info = models.Advertise.objects.filter(status=1).values('nid', 'title', 'image', 'url', "place", "update_time",
                                                                                         'desc', 'content').order_by("-weight")
    Inform = models.Inform.objects.filter(status=1).values("content").first()

    if user_id != '0' and openid != '0':
        user_info = models.Customer.objects.filter(status=1, openid=openid, nid=user_id).values("telephone", "qq",
                                                                                                "wechat", "email"
                                                                                                            ).first()

        if user_info.get("telephone") or user_info.get("qq") or user_info.get("wechat"):
            resp['data']['phone'] = True
        else:
            resp['data']['phone'] = False
    ad_head = []
    ad_center = []
    for item in ad_info:
        item["pic_url"] = build_url('advertise/' + item.get('image'))
        item['update_time'] = datetime.datetime.strftime(item.get('update_time'), "%Y-%m-%d %H:%M")
        if item.get("place") == "0":
            ad_head.append(item)
        elif item.get("place") == "1":
            ad_center.append(item)
    resp['data']['advertise'] = ad_head
    resp['data']["ad_center"] = ad_center
    resp["data"]["info"] = Inform
    return JsonResponse(resp)


def secondary(request):
    """
    二手信息
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    page_size = 20
    p = int(request.GET.get("p"))
    article_info = models.Article.objects.filter(status=1, category=3).values('nid', 'title', 'desc',
                                                                                        'create_time',
                                                                                        'comm_count', 'up_count',
                                                                                        'category__title',
                                                                                        'user__avatar',
                                                                                        'user__username').order_by(
        "-weight", "-create_time")[page_size * p:page_size * p + page_size]
    for item in article_info:
        date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
        item["create_time"] = date
        image = models.Article.objects.filter(nid=item.get("nid")).values("img__image").first()
        if image.get("img__image") and image.get("img__image") != "undefined":
            item["img__image"] = build_url('images/' + image.get("img__image"))
    resp['data']['has_more'] = 0 if len(article_info) < page_size else 1
    resp['data']['article'] = list(article_info)
    return JsonResponse(resp)


def study_class(request):
    """
    显示资料分类列表
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    if request.method == "POST":
        id = request.POST.get("id")

        if id == "undefined":
            study_link = models.Article.objects.filter(status=1, category_id=4, study_class__isnull=True).values('nid', 'title', 'desc',
                                                                                        'create_time',
                                                                                        'comm_count', 'up_count',
                                                                                        'category__title',
                                                                                        'user__avatar',
                                                                                        'user__username').order_by(
                                                                                "-weight", "-create_time")

            for item in study_link:
                date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
                item["create_time"] = date
            resp['data'] = list(study_link)
            return JsonResponse(resp)
        study_link = models.Article.objects.filter(status=1, study_class=id).values('nid', 'title', 'desc',
                                                                                        'create_time',
                                                                                        'comm_count', 'up_count',
                                                                                        'category__title',
                                                                                        'user__avatar',
                                                                                        'user__username').order_by(
                                                                                "-weight", "-create_time")
        for item in study_link:
            date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
            item["create_time"] = date

        resp['data'] = list(study_link)
        return JsonResponse(resp)
    category = models.StudyClass.objects.filter(status=1).values("id", "category", "num")
    other = models.Article.objects.filter(status=1, category_id=4, study_class__isnull=True).count()

    resp['data']['other'] = other
    resp["data"]['category'] = list(category)
    return JsonResponse(resp)


def rent(request):
    """
    出租信息
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    page_size = 20
    p = int(request.GET.get("p"))
    article_info = models.Article.objects.filter(status=1, category=2).values('nid', 'title', 'desc',
                                                                              'create_time',
                                                                              'comm_count', 'up_count',
                                                                              'category__title',
                                                                              'user__avatar',
                                                                              'user__username').order_by(
        "-weight", "-create_time")[page_size * p:page_size * p + page_size]
    for item in article_info:
        date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
        item["create_time"] = date
        image = models.Article.objects.filter(nid=item.get("nid")).values("img__image").first()
        if image.get("img__image") and image.get("img__image") != "undefined":
            item["img__image"] = build_url('images/' + image.get("img__image"))
    resp['data']['has_more'] = 0 if len(article_info) < page_size else 1

    resp['data']['article'] = list(article_info)
    return JsonResponse(resp)


def errand(request):
    """
    跑腿信息
    :param erquest:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    page_size = 20
    p = int(request.GET.get("p"))
    errand_list = models.Errand.objects.filter(status=1).values("id", "user__avatar", "user__username", "content", "kg",
                                                                "site", "deadline", "price", "valid", "create_time").order_by(
        "-weight", "-create_time")[page_size * p:page_size * p + page_size]
    for item in errand_list:
        date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
        item["create_time"] = date
        if not item.get("valid"):       # 是否已接单，接单则禁用按钮
            item['valid'] = True
        else:
            item['valid'] = False
    resp['data']['has_more'] = 0 if len(errand_list) < page_size else 1

    resp['data']['article'] = list(errand_list)
    return JsonResponse(resp)


def collect(request):
    """
    查询信息
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}

    phone_category = models.CategoryPhone.objects.filter(status=1).values("id", "category")

    resp['data']['phone_category'] = list(phone_category)
    return JsonResponse(resp)


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
    content = jieba.lcut(searchTitle)
    t1 = threading.Thread(target=saveFormId, args=(request,))
    t1.start()
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

    resp['data'] = result

    return JsonResponse(resp)