from django.urls import path, re_path
from backstage import views

urlpatterns = [
    re_path("login/*$", views.login, name="login"),
    re_path("pc-geetest/register/*$", views.pcgetcaptcha, name="pcgetcaptcha"),
    re_path("register/*$", views.register, name="register"),
    re_path("logout/*$", views.logout, name="logout"),
    re_path("datacube/*$", views.datacube, name="datacube"),
    re_path('test/*$', views.test, name="test")

]