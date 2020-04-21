#  -*- coding:utf-8 -*-
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
import pyech.views
from .settings import MEDIA_ROOT
from utils.cklogin import myserve
from pyech.views import npy2df, nparray_opr
urlpatterns = [
    path('test/',pyech.views.test),
    path('csv2table/',pyech.views.csv2table),
    path('admin/', admin.site.urls),
    path('delfiles/',pyech.views.delfiles),
    path('index/', pyech.views.demo3d),
    path('cachechart/',pyech.views.cachechart),
    path('conformchart/',pyech.views.conformchart),
    path("work/",pyech.views.workon),
    path("nparray_opr/",nparray_opr),
    path("npy2df/",npy2df),
    path("upload/",pyech.views.upload),
    path("getchartoptions/",pyech.views.getchartoptions),
    path("select/",pyech.views.select),
    path("drawchart/",pyech.views.draw),
    path("structure/",pyech.views.structure),
    path("dataprocess/",pyech.views.dataprocess),
    path("np_oper/",pyech.views.np_oper),# 
    path("getMInfo/",pyech.views.getMInfo),
    path("getNdimdict/",pyech.views.getNdimdict),
    path("hoverheaderinfo/",pyech.views.hoverheaderinfo),
    path("downloaddatafile/",pyech.views.downloaddatafile),
    url(r'^relog/', include(('login.urls',"relog"),namespace="relog")),
    url(r'^captcha', include('captcha.urls')),
    url(r'^media/(?P<path>.*)$', myserve, {"document_root":MEDIA_ROOT}),
]
