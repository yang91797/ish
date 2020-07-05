"""ish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from stark.service.stark import site
from wxapi import view
from django.views.generic import TemplateView
from django.views.static import serve
from ish import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^wxapi/', include(("wxapi.urls", "wxapi"))),
    re_path(r'media/(?P<path>.*)/$', serve, {"document_root": settings.MEDIA_ROOT}),
    re_path('^backstage/', include(('backstage.urls', "backstage"))),
    re_path("^rbac/", include(('rbac.urls', 'rbac'))),
    re_path("^stark/", site.urls),
    re_path(r'^static/(?P<path>.*)/$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path('robots\.txt/*$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    
]

