from django.http import JsonResponse
from wxapi import models
from wxapi.utils.tools import read_update, build_url
import datetime
import threading


def second(request):
    """
    查看二手详情
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    if request.method == "POST":  # 查看回复评论
        comment_list = []
        cid = request.POST.get("cid")
        comment_queryset = models.Comment.objects.filter(status=1, ancestor=cid).values('nid', 'user_id',
                                                                                        "user__openid",
                                                                                        'user__username',
                                                                                        'user__avatar', 'content',
                                                                                        'create_time', 'parent_comment',
                                                                                        'like_count', 'reply_count',
                                                                                        'ancestor',
                                                                                        'parent_comment__user__openid',
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
                                                                             'read_count', 'user__username',
                                                                             'user__openid',"valid",
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
        "-pk").values('nid', 'user_id', 'user__openid', 'user__username', 'user__avatar', 'parent_comment',
                      'reply_count', "ancestor",
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


def phone(request):
    """
    接单返回联系方式
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    openid = request.META.get("HTTP_IDMD5")
    id = request.GET.get("id")

    relation = models.Errand.objects.filter(id=id, valid=1, status=1).values("user_id", "user__qq", "user__wechat", "user__telephone", "user__order").first()
    if relation.get("user__wechat"):
        resp['data']['wechat'] = relation.get("user__wechat")
    elif relation.get("user__qq"):
        resp['data']['qq'] = relation.get("user__qq")
    elif relation.get("user__telephone"):
        resp['data']['telephone'] = relation.get("user__telephone")

    if not relation.get("user__order"):
        models.Customer.objects.filter(nid=relation.get("user_id")).update(order=1)
    models.ErrandRecord.objects.create(user_id=user_id, errand_id=id)

    return JsonResponse(resp)


def collect(request):
    """
    返回办公联系方式
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    user_id = request.META.get('HTTP_AUTHORIZATION')
    pid = request.GET.get("id")

    phone = models.Telephone.objects.filter(status=1, category_id=pid).values("name", "phone")

    resp["data"]["phone"] = list(phone)
    return JsonResponse(resp)
