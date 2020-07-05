from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# create database ish default charset utf8mb4


class Customer(models.Model):
    """
    用户信息
    """
    nid = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name="用户名", max_length=120)
    openid = models.CharField(verbose_name="微信用户唯一标识openid", max_length=64, blank=True, null=True, unique=True)
    key = models.CharField(verbose_name="密匙", max_length=16, blank=True, null=True)
    telephone = models.CharField(max_length=11, null=True, blank=True)
    avatar = models.URLField(verbose_name='头像')
    sex_choices = [
        (1, '男'),
        (2, '女')
    ]
    sex = models.IntegerField(verbose_name='性别', choices=sex_choices, default=1)
    province = models.CharField(verbose_name='省份', max_length=32, blank=True, null=True)
    city = models.CharField(verbose_name='城市', max_length=32, blank=True, null=True)
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    qq = models.CharField(verbose_name="QQ", max_length=13, blank=True, null=True)
    wechat = models.CharField(verbose_name="微信", max_length=64, blank=True, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    asset = models.IntegerField(verbose_name='资产', default=50)
    score = models.IntegerField(verbose_name='积分', default=50)
    study_buy = models.ManyToManyField(to='Article', through='Buy', through_fields=('user', 'study', ))            # 半自动创建第三张表
    inform = models.ManyToManyField(to="Inform", through="Inform2Customer", through_fields=('user', 'inform'))
    student_number = models.IntegerField(verbose_name="学号", null=True, blank=True)
    name = models.CharField(verbose_name="姓名", max_length=16, null=True, blank=True)
    order = models.IntegerField(verbose_name='是否预定跑腿信息通知，已预定:1,未预定：0', default=0)
    status = models.IntegerField(verbose_name='状态 1：有效， 0:无效', default=1)


class Formid(models.Model):
    """
    form_id
    """
    formid = models.CharField(verbose_name="form_id", max_length=64)
    user = models.ForeignKey(verbose_name="用户", to=Customer, to_field='nid', on_delete=models.CASCADE)

    expire = models.CharField(verbose_name="过期时间戳", max_length=64)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Msg(models.Model):
    """
    用户信息通知记录
    """
    user = models.ForeignKey(verbose_name="关联的用户", to="Customer", related_name='user2id', on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name="关联的文章", to="Article", null=True, blank=True, on_delete=models.CASCADE)
    commentUserId = models.ForeignKey(verbose_name="被评论用户的id", to="Customer", related_name='commentUser2id', null=True, blank=True, on_delete=models.CASCADE)
    commentId = models.ForeignKey(verbose_name="评论信息的id", to="Comment", null=True, blank=True, on_delete=models.CASCADE)
    describe = models.CharField(verbose_name="描述信息", max_length=255)
    create_time = models.DateTimeField(verbose_name="时间", auto_now_add=True)
    read = models.IntegerField(verbose_name="已读：0，未读：1", default=1)
    status = models.IntegerField(verbose_name='状态 1：有效， 0:无效', default=1)


class Inform(models.Model):
    """
    用户告知
    """
    title = models.CharField(verbose_name="标题", max_length=32, null=True, blank=True)
    content = models.TextField()
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    status = models.IntegerField(verbose_name='状态 1：有效， 0:无效', default=1)


class Inform2Customer(models.Model):
    """
    用户通知记录
    """
    user = models.ForeignKey(verbose_name="通知的用户", to="Customer", on_delete=models.CASCADE)
    inform = models.ForeignKey(verbose_name="通知信息", to="Inform", on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(verbose_name="阅读时间", auto_now_add=True)
    read = models.IntegerField(verbose_name="已读：0，未读：1", default=1)
    status = models.IntegerField(verbose_name='状态 1：有效， 0:无效', default=1)


class Category(models.Model):
    """
    分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    文章表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题', null=True, blank=True)
    desc = models.CharField(max_length=255, verbose_name='文章描述', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    content = models.TextField(verbose_name="正文内容", null=True, blank=True)
    comm_count = models.IntegerField(verbose_name="评论数", default=0)
    up_count = models.IntegerField(verbose_name="点赞数", default=0)
    read_count = models.IntegerField(verbose_name="阅读数", default=0)

    type_choice = (
        ('html', 'html格式'),
        ('md', 'markdown格式'),
        ('text', '文本格式')
    )
    type = models.CharField(verbose_name='文章类型,html:text:md', choices=type_choice, default='html', max_length=6)
    study_url = models.ForeignKey(verbose_name='分享学习资料的链接', null=True, blank=True, to='StudyLink', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='发布者', to='Customer', on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name='分类', to='Category', to_field='nid', null=True, blank=True, on_delete=models.CASCADE)
    study_class = models.ForeignKey(verbose_name="资料类型：科目", to="StudyClass", to_field="id", null=True, blank=True, on_delete=models.CASCADE)
    img = models.ManyToManyField(verbose_name="图片", to="Image")             # 全自动创建第三张表
    weight = models.IntegerField(verbose_name="文章权重", default=0)
    valid = models.BooleanField(verbose_name="是否有效", default=True)
    status = models.IntegerField(verbose_name='状态 1：发布， 0:删除', default=1)

    def __str__(self):
        return self.title


class StudyClass(models.Model):
    """
    资料分类
    """
    category = models.CharField(verbose_name="资料分类", max_length=80)
    num = models.IntegerField(verbose_name="资料数量", default=0)
    status = models.IntegerField(verbose_name='状态 1：有效， 0:无效', default=1)


class StudyLink(models.Model):
    """
    资料链接
    """
    nid = models.AutoField(primary_key=True)
    study_url = models.CharField(max_length=255, verbose_name='分享学习资料的链接', null=True, blank=True)
    gold = models.IntegerField(verbose_name="多少金币兑换", default=0)
    study_class = models.ForeignKey(to="StudyClass", to_field="id", on_delete=models.CharField, null=True, blank=True)


class Buy(models.Model):
    """
    用户购买的资料
    """
    user = models.ForeignKey(to="Customer", to_field='nid', on_delete=models.CASCADE)
    study = models.ForeignKey(to="Article", to_field='nid', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('user', 'study')
        ]


class Image(models.Model):
    """
    文章中,评论中的图片
    """
    nid = models.AutoField(primary_key=True)
    image = models.FileField(verbose_name='上传的图片', upload_to='images/')


class ArticleUpDown(models.Model):
    """
    文章点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('Customer', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]


class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='评论者', to='Customer', to_field='nid', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容', max_length=500)
    img = models.ManyToManyField(verbose_name="评论中的图片", to="Image", through="CommentImage", through_fields=("commentId", "image"))
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    parent_comment = models.ForeignKey(verbose_name='上一级评论', to='self', related_name="parent_comment_comm", blank=True, null=True, on_delete=models.CASCADE)
    like_count = models.IntegerField(verbose_name='点赞数', default=0)
    reply_count = models.IntegerField(verbose_name="回复数", default=0)
    ancestor = models.ForeignKey(verbose_name='主楼评论', to='self', related_name="ancestor_comment", blank=True, null=True, on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='评论状态，-1为删除，0为待审核，1为已发布', default=1)
    send = models.BooleanField(verbose_name="是否发送，True为已发送，False为未发送", default=False)

    def __str__(self):
        return self.content


class CommentImage(models.Model):
    """
    评论中的图片
    """
    commentId = models.ForeignKey(verbose_name="评论id", to="Comment", to_field="nid", on_delete=models.CASCADE)
    image = models.ForeignKey(verbose_name="图片id", to="Image", to_field="nid", on_delete=models.CASCADE)


class Sign(models.Model):
    """
    签到表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='签到用户', to='Customer', on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Trove(models.Model):
    """
    文章收藏表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name="收藏文章的用户", to="Customer", on_delete=models.CASCADE)
    article = models.ForeignKey(verbose_name="文章", to="Article", on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('user', 'article'),
        ]


class Advertise(models.Model):
    """
    宣传
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name="关联用户", to="Customer", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(verbose_name='宣传项目名称', max_length=24, null=True, blank=True)
    image = models.FileField(verbose_name='宣传首页图片', upload_to='advertise/', null=True, blank=True)
    url = models.URLField(verbose_name='相关URL', null=True, blank=True)
    place = models.CharField(verbose_name='宣传位置', max_length=10, null=True, blank=True)
    desc = models.CharField(verbose_name="简述", max_length=120, blank=True, null=True)
    content = models.TextField(verbose_name='描述信息', blank=True, null=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, null=True, blank=True)
    over_time = models.DateTimeField(verbose_name="到期时间", null=True, blank=True)
    weight = models.IntegerField(verbose_name="文章权重", default=0)
    status = models.IntegerField(verbose_name='状态 1：有效， 0:无效', default=1)
    
    def __str__(self):
        return self.title


class AdImage(models.Model):
    """
    宣传图片
    """
    image = models.FileField(verbose_name='宣传文章图片', upload_to='advertise/')
    ad = models.ForeignKey(verbose_name="宣传文章", to="Advertise", on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(verbose_name="状态 1：有效， 0:无效", default=1)


class Errand(models.Model):
    """
    跑腿
    """
    user = models.ForeignKey(verbose_name="发布者", to="Customer", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="描述", max_length=150)
    kg = models.IntegerField(verbose_name="重量")
    site = models.CharField(verbose_name="地点", max_length=60)
    deadline = models.CharField(verbose_name="截止时间", max_length=60)
    price = models.FloatField(verbose_name="价格", max_length=5, default=0)
    valid = models.BooleanField(verbose_name="是否有效", default=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    weight = models.IntegerField(verbose_name="文章权重", default=0)
    status = models.IntegerField(verbose_name='状态 1：发布， 0:删除', default=1)


class ErrandRecord(models.Model):
    """
    跑腿接单记录
    """
    user = models.ForeignKey(verbose_name="接单者", to="Customer", on_delete=models.CASCADE)
    errand = models.ForeignKey(verbose_name="订单", to="Errand", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="接单时间", auto_now_add=True)


# class IpRecord(models.Model):
#     """
#     代理ip记录
#     """
#     ip = models.CharField(verbose_name="ip", max_length=32)
#     create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
#     status = models.IntegerField(verbose_name='状态 1：有效， 0:无效', default=1)


class Telephone(models.Model):
    """
    常用电话
    """
    name = models.CharField(verbose_name="名称", max_length=16, null=True, blank=True)
    phone = models.CharField(verbose_name="号码", max_length=16)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    site = models.CharField(verbose_name="地点", max_length=64, null=True, blank=True)
    category = models.ForeignKey(verbose_name="分类", to="CategoryPhone", on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='状态 1：有效， 0:无效', default=1)


class CategoryPhone(models.Model):
    """
    电话分类
    """
    category = models.CharField(verbose_name="电话分类", max_length=32)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    status = models.IntegerField(verbose_name='状态 1：有效， 0:无效', default=1)
