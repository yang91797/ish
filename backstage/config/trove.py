from stark.service.stark import site, StarkConfig, Option, get_choice_text
from backstage.permission.base import RbacPermission


class TroveConfig(RbacPermission, StarkConfig):
    def display_user(self, row=None, header=False):
        if header:
            return "收藏着"
        return row.user.username

    list_display = [
        "nid",
        display_user,
        "article"
    ]

    order_by = ["-nid"]