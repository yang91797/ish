from django.http import JsonResponse
from django.db import transaction
from django.db.models import F, Q
from wxapi.utils.tools import build_url, hs, saveFormId, SecCheck
from wxapi import models
from ish import settings
import threading
import os
import time
import requests
import json


def add(request):
    """
    添加
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '上传成功', 'data': {}}

    user_id = request.META.get('HTTP_AUTHORIZATION')
    title = request.POST.get('title')
    content = request.POST.get('content')
    img_url = request.POST.get('images')
    types = request.POST.get('type')
    category_id = request.POST.get('category')
    study_url = request.POST.get('study_url')
    gold = request.POST.get('gold')

    t1 = threading.Thread(target=saveFormId, args=(request,))
    t1.start()
    check = SecCheck(request)
    if not check:
        resp["code"] = 405
        resp['msg'] = "发布的内容具有敏感信息"
        return JsonResponse(resp)

    desc = content[0:60] + '......' if len(content) > 60 else content
    with transaction.atomic():
        if study_url != "undefined":
            subject = request.POST.get("subject")
            study_class = models.StudyClass.objects.filter(status=1, category=subject).values("id")
            study_class.update(num=F("num") + 1)

            link = models.StudyLink.objects.create(study_url=study_url, gold=gold)
            if study_class:
                obj = models.Article.objects.create(title=title, desc=desc, content=content, type=types,
                                                    user_id=user_id, category_id=category_id, study_url_id=link.pk,
                                                    study_class_id=study_class.first().get("id"))
            else:
                obj = models.Article.objects.create(title=title, desc=desc, content=content, type=types,
                                                    user_id=user_id, category_id=category_id, study_url_id=link.pk)

            resp['msg'] = "上传成功,请等待管理员审核"
        else:

            obj = models.Article.objects.create(title=title, desc=desc, content=content, type=types,
                                                user_id=user_id, category_id=category_id)

        if img_url:
            img_list = img_url.split(',')
            for img in img_list:
                if img == "[object Object]":
                    continue
                res = models.Image.objects.create(image=img)
                obj.img.add(res.nid)

    return JsonResponse(resp)
    # if category_id == '2':
    #     # 租借信息
    #     pass
    # elif category_id == "3":
    #     # 二手信息
    #     if second(request):
    #
    #         return JsonResponse(resp)
    #
    # elif category_id == "4":
    #     # 学习资料
    #     pass


def second(request):
    """
    添加二手信息
    :param request:
    :return:
    """
    pass


def rent(request):
    pass


def source(request):
    """
    添加资料信息
    :param request:
    :return:
    """
    pass


def upload(request):
    """
    接收上传的图片
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}

    check = SecCheck(request)
    if not check:
        resp["code"] = 405
        resp['msg'] = "发布的内容具有敏感信息"
        return JsonResponse(resp)
    img = request.FILES.get('images')
    path = os.path.join(settings.MEDIA_ROOT, "images", img.name)
    with open(path, 'wb') as f:
        for line in img:
            f.write(line)
    resp['data'] = img.name
    return JsonResponse(resp)


def errand(request):
    """
    添加跑腿信息
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    openid = request.META.get("HTTP_IDMD5")
    check = SecCheck(request)
    if not check:
        resp["code"] = 405
        resp['msg'] = "发布的内容含有敏感信息"
        return JsonResponse(resp)

    desc = request.POST.get("desc")
    kg = request.POST.get("kg")
    price = request.POST.get("price")
    site = request.POST.get("site")
    outdate = request.POST.get("outdate")

    models.Errand.objects.create(user_id=user_id, content=desc, kg=kg, price=price, site=site, deadline=outdate)
    return JsonResponse(resp)


def comment(request):
    """
    评论
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
    check = SecCheck(request)
    if not check:
        resp["code"] = 405
        resp['msg'] = "发布的内容含有敏感信息"
        return JsonResponse(resp)

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

            if comment_id != ancestor:  # 回复
                models.Comment.objects.filter(pk=ancestor).update(reply_count=F("reply_count") + 1)

            if user_id != commentUserId:
                models.Msg.objects.create(user_id=user_id, article_id=article_id, commentUserId_id=commentUserId,
                                          commentId=obj, describe=comment)

        return JsonResponse(resp)

    articleUserId = articleUser.get("user_id")

    with transaction.atomic():

        if images:
            img_list = images.split(',')
            obj = models.Comment.objects.create(article_id=article_id, user_id=user_id, content=comment)
            models.Article.objects.filter(pk=article_id).update(comm_count=F("comm_count") + 1)
            des = ""
            for img in img_list:
                if img == "[object Object]":
                    continue

                res = models.Image.objects.create(image=img)
                models.CommentImage.objects.create(commentId=obj, image=res)
                des = des + "[[图片]]"

            if int(user_id) != articleUserId and comment == "null":
                models.Msg.objects.create(user_id=user_id, article_id=article_id,
                                          commentUserId_id=articleUserId, commentId=obj,
                                          describe=des)

        else:
            obj = models.Comment.objects.create(article_id=article_id, user_id=user_id, content=comment)
            models.Article.objects.filter(pk=article_id).update(comm_count=F("comm_count") + 1)

            if int(user_id) != articleUserId:
                models.Msg.objects.create(user_id=user_id, article_id=article_id, commentUserId_id=articleUserId,
                                          commentId=obj, describe=comment)

    return JsonResponse(resp)



