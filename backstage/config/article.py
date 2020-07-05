from stark.service.stark import site, StarkConfig, Option, get_choice_text
from backstage.permission.base import RbacPermission


class ArticleConfig(RbacPermission, StarkConfig):
    def display_user(self, row=None, header=False):
        if header:
            return "发布者"
        return row.user.username
    list_display = [
        'nid',
        'title',
        'desc',
        'comm_count',
        'up_count',
        get_choice_text("type", "文章类型"),
        display_user,
        'category',
        'status',
    ]

    search_list = [
        'title',
        'desc',
        'comm_count',
        'up_count',
        'type',
        'user',
        'category',
        'status'
    ]

    list_filter = [
        Option(field='type', is_choice=True, is_multi=True, text_func=lambda x: x[1]),
        Option(field='category', is_choice=False, is_multi=True, text_func=lambda x:x.title, value_func=lambda x:x.pk)
    ]
    order_by = ["-nid"]










