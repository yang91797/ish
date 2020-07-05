from django.http import JsonResponse
from django.db import transaction
from django.db.models import F, Q
from wxapi.utils.tools import build_url, hs, saveFormId
from wxapi import models
from ish import settings
import threading
import os
import datetime


def publish(request):
    """
    我的发布
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    openid = request.META.get("HTTP_IDMD5")
    category = request.POST.get("category")
    page_size = 10
    p = int(request.POST.get('p'))

    if category == "跑腿":
        article = models.Errand.objects.filter(user_id=user_id, status=1).values("id",
                                                                                 "content", "kg", "site", "deadline",
                                                                                 "price", "valid", "create_time").order_by(
                                                                "-create_time")[page_size * p:page_size * p + page_size]

        resp['data']['has_more'] = 0 if len(article) < page_size else 1
        resp['data']['article'] = list(article)
        return JsonResponse(resp)

    article = models.Article.objects.filter(user_id=user_id, status=1, category__title=category).values('nid', 'title',
                                                                                                        'desc',
                                                                                                        'create_time',
                                                                                                        'comm_count',
                                                                                                        'up_count',
                                                                                                        'category__title',
                                                                                                        "valid"
                                                                                                        ).order_by(
                                                                "-create_time")[page_size * p:page_size * p + page_size]

    for item in article:
        date = datetime.datetime.strftime(item.get('create_time'), "%Y-%m-%d %H:%M")
        item['create_time'] = date
    resp['data']['has_more'] = 0 if len(article) < page_size else 1
    resp['data']['article'] = list(article)
    return JsonResponse(resp)


def valid(request):
    """
    发布的内容是否完成
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    openid = request.META.get("HTTP_IDMD5")
    category = request.POST.get("category")
    id = request.POST.get("id")

    if category == "跑腿":
        isTrue = models.Errand.objects.filter(user_id=user_id, status=1, pk=id).values("valid")
        if isTrue.first().get("valid"):
            isTrue.update(valid=False)
        else:
            isTrue.update(valid=True)

        return JsonResponse(resp)

    article = models.Article.objects.filter(user_id=user_id, status=1, nid=id).values("valid")
    if article.first().get("valid"):
        article.update(valid=False)
    else:
        article.update(valid=True)

    return JsonResponse(resp)