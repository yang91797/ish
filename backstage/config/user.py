from stark.service.stark import site, StarkConfig, Option, get_choice_text
from backstage.permission.base import RbacPermission


class UserConfig(RbacPermission, StarkConfig):
    list_display = [
        "id",
        "username",
        "name",
        "phone",
        get_choice_text("gender", "性别"),
        "email"
    ]

    order_by = ["-id"]
