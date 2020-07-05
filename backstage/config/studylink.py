from stark.service.stark import site, StarkConfig, Option, get_choice_text
from backstage.permission.base import RbacPermission


class StudyLinkConfig(RbacPermission, StarkConfig):
    list_display = [
        "nid",
        "study_url",
        "gold"
    ]

    order_by = ["-nid"]