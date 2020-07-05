from stark.service.stark import site, StarkConfig, Option, get_choice_text
from backstage.permission.base import RbacPermission
from django.shortcuts import HttpResponse


class AdvertiseConfig(RbacPermission, StarkConfig):
    def display_detail(self, row=None, header=False):
        if header:
            return "查看详细"
        return HttpResponse("查看详细。。。")

    list_display = [
        "nid",
        "title",
        "content",
        "status",
        display_detail
    ]