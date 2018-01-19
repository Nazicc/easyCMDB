#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 17-12-23 上午11:00
# @Author : Chenkai
# @File  : urls.py
# @Software: PyCharm

from django.conf.urls import url
from . import views

from django.views.generic import TemplateView

app_name = 'user'

urlpatterns = [
    # url(r'^$', view=views.index, name='index'),
    url(r'^$', TemplateView.as_view(template_name='user/login.html'), name='index'),
    url(r'^login/$', view=views.login, name='login'),
    url(r'^users/$', view=views.users, name='users'),
    # url(r'^create/$', view=views.create, name='create'),
    url(r'^create/$', TemplateView.as_view(template_name='user/create.html'), name='create'),
    url(r'^save/$', view=views.save, name='save'),
    url(r'^edit/$', view=views.edit, name='edit'),
    url(r'^modify/$', view=views.modify, name='modify'),
    url(r'^delete/$', view=views.delete, name='delete'),
    url(r'^logout/$', view=views.logout, name='logout'),
]