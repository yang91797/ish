from django.db import models

# Create your models here.


class Menu(models.Model):
    """
    菜单
    """
    title = models.CharField(verbose_name='一级菜单', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32)

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128)

    name = models.CharField(verbose_name='真实姓名', max_length=64, unique=True, null=False, blank=False)
    pid = models.ForeignKey(verbose_name='默认选中权限', to='Permission', related_name='ps', null=True, blank=True,
                            help_text='对于无法作为菜单的URL,可以为其选择一个可以作为菜单的权限，那么访问时，则默认选中此权限',
                            limit_choices_to={'menu__isnull': False}, on_delete=models.SET_NULL)
    menu = models.ForeignKey(verbose_name='菜单', to='Menu', null=True, blank=True, help_text='null表示非菜单',on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name='用户名', max_length=32, null=True, blank=True)
    password = models.CharField(verbose_name='密码', max_length=64, null=True, blank=True)
    email = models.CharField(verbose_name='邮箱', max_length=32, null=True, blank=True)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to=Role, blank=True)         # 如果使用abstract = True与其他表做关联，to后面关联的表不加引号

    class Meta:
        abstract = True         # 有此字段不会生成表

    def __str__(self):
        return self.username


"""
current_user = models.UserInfo.objects.filter(name=user, password=pwd).first()

# 获取当前用户所拥有的权限
permission_list = current_user.roles.filter(permissions__isnull=False).values(permissions__id,permissions__url).distinct()

# 问题一：
    1. 一个用户是否可以拥有多个角色？是
    2. 一个角色是否可以用拥有多个权限？是

    CEO：
        /index/
        /order/
    总监：
        /index/
        /customer/

    销售：
        /user/
        /add_user/
    金牌讲师

# 问题二：
    权限表：
        /index/
        ....

    角色表：
        CEO：
        总监：
        销售：
        金牌讲师

    角色和权限关系：
         CEO：     /index/
         总监：     /order/

    用户和角色关系表：
        1 1 
        1 1 
        1 1 

    用户表：
        wupeiqi



总监 /index/
总监 /customer/
销售 /user/
销售 /add_user/
金牌讲师 null

"""