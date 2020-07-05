from stark.service.stark import site, StarkConfig, Option, get_choice_text
from backstage.permission.base import RbacPermission
from django.urls import reverse
from django.shortcuts import HttpResponse, render, redirect
from django.utils.safestring import mark_safe
from django.urls import path, re_path
from wxapi import models


class InformConfig(RbacPermission, StarkConfig):
    def display_inform(self, row=None, header=False):
        if header:
            return "发布申明"
        # url=reverse("stark:wxapi_inform_detail", kwargs=(row.pk))
        return HttpResponse("????")

    def display_date(self, row=None, header=False):
        if header:
            return "发布时间"
        return row.create_time.strftime("%Y-%m-%d %H:%M")

    def get_add_btn(self):
        """
        自定义添加页面
        :return:
        """
        url = reverse("stark:wxapi_inform_addInform")
        print(url, "????")

        return mark_safe('<a href="%s" class="btn btn-success">添加</a>' % url)

    def display_edit(self, row=None, header=False):
        """
        自定义编辑页面
        :param row:
        :param header:
        :return:
        """
        if header:
            return "编辑"
        url = reverse("stark:wxapi_inform_editInform", kwargs={'pk': row.pk})

        return mark_safe(
            '<a href="%s"><i class="fa fa-edit" aria-hidden="true"></i></a></a>' % url
        )

    def extra_url(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name

        urlpatterns = [
            re_path('addInform/', self.wrapper(self.addInform_view), name='%s_%s_addInform' % info),
            re_path('editInform/(?P<pk>\d+)/', self.wrapper(self.editInform_view), name='%s_%s_editInform' % info)
        ]

        return urlpatterns

    def addInform_view(self, request):
        if request.method == "POST":

            title = request.POST.get("title")
            content = request.POST.get("content")

            models.Inform.objects.create(title=title, content=content)
            return redirect("/stark/wxapi/inform/list/")
        return render(request, "addInform.html")

    def editInform_view(self, request, pk):
        if request.method == "POST":
            title = request.POST.get('title')
            content = request.POST.get("content")
            models.Inform.objects.filter(pk=pk).update(title=title, content=content)
            return redirect("/stark/wxapi/inform/list/")
        article = models.Inform.objects.filter(pk=pk).first()

        return render(request, "editInform.html", {"article": article})

    def get_list_display(self):
        val = super().get_list_display()
        val.remove(StarkConfig.display_edit)     # 移除自带编辑功能
        val.insert(0, StarkConfig.display_checkbox)     # 插入了一个选项框
        return val

    list_display = [
        "title",
        display_edit,
        display_date,
        "status"
    ]