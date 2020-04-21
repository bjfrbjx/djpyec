#  -*- coding:utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^logout/', views.logout),

]

