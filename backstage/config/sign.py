from stark.service.stark import site, StarkConfig, Option, get_choice_text
from backstage.permission.base import RbacPermission


class SignConfig(RbacPermission, StarkConfig):
    def display_user(self, row=None, header=False):
        if header:
            return "签到用户"
        return row.user.username

    def display_date(self, row=None, header=False):
        if header:
            return "签到时间"
        return row.create_time.strftime("%Y-%m-%d %H:%M")
    list_display = [
        "nid",
        display_user,
        display_date
    ]

    order_by = ["-nid"]