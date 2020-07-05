from stark.service.stark import site, StarkConfig, Option, get_choice_text
from backstage.permission.base import RbacPermission


class CommentConfig(RbacPermission, StarkConfig):
    def display_user(self, row=None, header=False):
        if header:
            return "评论者"
        return row.user.username

    list_display = [
        "nid",
        "article",
        display_user,
        "content",
        "status"
    ]

    order_by = ['-nid']