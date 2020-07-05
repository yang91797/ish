from django.db import models
from rbac.models import UserInfo as RbacUserInfo
from django.utils.timezone import now
import datetime
# Create your models here.


class UserInfo(RbacUserInfo):
    """
    管理员信息表
    """
    avatar = models.FileField(verbose_name='头像', upload_to="avatars/", default="default.png")
    name = models.CharField(verbose_name="真实姓名", max_length=16)
    phone = models.CharField(verbose_name="手机号", max_length=32, null=True, blank=True)
    genderChoices = (
        (1, '男'),
        (2, '女')
    )
    gender = models.IntegerField(verbose_name="性别", choices=genderChoices, default=1)
    email = models.EmailField(verbose_name="邮箱", )
    depart = models.ForeignKey(verbose_name='部门', to="Department", null=True, blank=True, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(verbose_name='部门名称', max_length=16)

    def __str__(self):
        return self.title


class Inform(models.Model):
    """
    管理员通知信息
    """
    source = models.ForeignKey(verbose_name="发布者", to="UserInfo", related_name="source_re", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="关联的用户", to="UserInfo", related_name="user_re", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="标题", max_length=32)
    content = models.TextField()
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    read = models.IntegerField(verbose_name="已读：0，未读：1", default=1)
    status = models.IntegerField(verbose_name='状态 1：有效， 0:无效', default=1)

