from stark.service.stark import site, StarkConfig, Option, get_choice_text
from backstage.permission.base import RbacPermission


class UserInfoConfig(RbacPermission, StarkConfig):
    def display_title(self, row=None, header=False):
        if header:
            return "姓名"
        return row.username

    def display_telephone(self, row=None, header=False):
        if header:
            return "电话"
        return row.telephone

    list_display = [
        'nid',
        display_title,
        get_choice_text("sex", "性别"),
        "email",
        display_telephone,
        "asset",
        "status"
    ]

    search_list = ["username"]

    order_by = ["-nid"]
