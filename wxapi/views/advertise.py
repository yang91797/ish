from wxapi import models
from django.http import JsonResponse
from wxapi.utils.tools import build_url, hs
import datetime
from ish import settings
import os


def auth_key(request):
    """
    用户认证
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    key = request.GET.get("key")
    user = models.Customer.objects.filter(key=key, status=1).first()
    if not user:
        resp['code'] = 403

    return JsonResponse(resp)


def change(request):
    """
    更改内容
    :param request:
    :return:
    """
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    user_id = request.META.get('HTTP_KEY')

    title = request.POST.get('title')
    content = request.POST.get('content')
    img_obj = request.POST.get('images')

    desc = content[0:33] + '......' if len(content) > 33 else content
    if img_obj:
        img_list = img_obj.split(',')
        ad = models.Advertise.objects.create(title=title, desc=desc, content=content, image=img_list.pop(0))
        for item in img_list:
            models.AdImage.objects.create(image=item, ad_id=ad.pk)
    else:
        models.Advertise.objects.create(title=title, desc=desc, content=content)
        # res = models.Image.objects.create(image=img)

    return JsonResponse(resp)


def upload(request):
    """
    上传的广告内容
    :param request:
    :return:
    """

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    user_id = request.META.get('HTTP_KEY')
    img = request.FILES.get('file')

    path = os.path.join(settings.MEDIA_ROOT, "advertise", img.name)

    with open(path, 'wb') as f:
        for line in img:
            f.write(line)
    resp['data'] = img.name
    return JsonResponse(resp)