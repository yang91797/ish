from django.contrib import admin
from wxapi import models
# Register your models here.

admin.site.register(models.Customer)
admin.site.register(models.Category)
admin.site.register(models.Article)
admin.site.register(models.ArticleUpDown)
admin.site.register(models.Comment)
admin.site.register(models.Sign)
admin.site.register(models.Advertise)
admin.site.register(models.StudyLink)
admin.site.register(models.Buy)
admin.site.register(models.Image)
admin.site.register(models.Trove)

