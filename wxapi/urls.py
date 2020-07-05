from django.urls import path, re_path
from wxapi import view
from wxapi.views import home
from wxapi.views import create
# from wxapi.views import auth
from wxapi.views import details
from wxapi.views import my
from wxapi.views import userinfo
from wxapi import tests
from wxapi.views import advertise
from django.views.static import serve
from ish import settings

urlpatterns = [
    re_path('^login/*', view.login, name='login'),
    re_path('^check-reg/*$', view.check_reg, name='check_reg'),
    # re_path('advertise/*$', view.advertise, name='advertise'),

    re_path("home/advertise/*$", home.advertise, name="advertise"),
    re_path("^home/secondary/*$", home.secondary, name="secondary"),
    re_path('home/studyclass/*$', home.study_class, name="study_class"),
    re_path("^home/errand/*$", home.errand, name="second_list"),
    re_path("^home/rent/*$", home.rent, name="rent"),
    re_path("^home/collect/*$", home.collect, name="collect"),
    re_path("^create/add/*$", create.add, name="add"),
    re_path("^create/errand/*$", create.errand, name="errand"),
    re_path("create/upload/*$", create.upload, name="createUpload"),
    re_path("^create/comment/*$", create.comment, name="create_comment"),
    # re_path("auth/jou/*$", auth.jou, name="jou"),
    re_path("^details/second/*$", details.second, name="second"),
    re_path("^details/phone/*$", details.phone, name="phone"),
    re_path("^details/collect/*$", details.collect, name="detail_collect"),
    re_path("^my/publish/*$", my.publish, name="my_publish"),
    re_path("^my/valid/*$", my.valid, name="valid"),
    re_path('^userinfo/login/*$', userinfo.login, name='userinfo_login'),
    re_path("^userinfo/changeUser/*$", userinfo.change_user, name="userinfo_change"),
    re_path('^userinfo/check-reg/*$', userinfo.check_reg, name='userinfo_check_reg'),
    re_path("^advertise/auth/*$", advertise.auth_key, name="auth_key"),
    re_path("^advertise/change/*$", advertise.change, name="change"),
    re_path("^advertise/upload/*$", advertise.upload, name="ad_upload"),

    re_path('index/*', view.index, name='index'),
    re_path('category/*$', view.category, name='category'),
    re_path('search/*$', view.search, name='search'),
    # re_path('media/(?P<path>.*)/*', serve, {"document_root": settings.MEDIA_ROOT}, name="serve"),
    re_path('create/*$', view.create, name='create'),
    re_path('upload/*$', view.upload, name='upload'),
    re_path('details/*$', view.details, name='details'),
    re_path('comment/*$', view.comment, name='comment'),
    re_path('like/*$', view.like, name='like'),
    re_path('study_link/*$', view.study_link, name='study_link'),
    re_path("sign/*$", view.sign, name='sign'),
    re_path("collect/*$", view.collect, name="collect"),
    re_path("reply/*$", view.reply, name="reply"),
    re_path("storage/*$", view.storage, name="storage"),
    re_path("publish/*$", view.publish, name="publish"),
    re_path("delete/*$", view.delete, name="delete"),
    re_path("msg/*$", view.msg, name="msg"),
    re_path("inform/*$", view.inform, name="inform"),
    re_path("report/*$", view.report, name="report"),
    re_path("changeUser/*$", view.change_user, name='change_user'),
    re_path("saveFormId/*$", view.saveFormId, name='saveFormId'),
    re_path('test/*$', tests.test, name='test')

]