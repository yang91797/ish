from stark.service.stark import site, StarkConfig, Option, get_choice_text
from backstage.permission.base import RbacPermission


class CategoryConfig(RbacPermission, StarkConfig):

    list_display = [
        "nid",
        "title"
    ]

