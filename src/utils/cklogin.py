#  -*- coding:utf-8 -*-
'''
Created on 2019年7月21日

@author: 魔天一念
'''
from django.views.static import serve
from django.shortcuts import redirect
from djpyec.settings import LOGIN_URL ,WORK_URL
import pandas
import chardet
from django.core.cache import cache
from pyech.models import CacheChartRender
from login.models import User
import pickle
import sys
from utils.drawchart import DrawChartException
def login_required(view_func):
    """
        登录检测函数，后面只要@login_required 就能在回应请求前检测用户是否已经登录，否则转到登陆页面
    """
    def wrapper(request,*view_args,**view_kwargs):
        if request.session.get("is_login",False):
            return view_func(request,*view_args,**view_kwargs)
        else:
            return redirect(LOGIN_URL)
    return wrapper


@login_required
def myserve(request, path, document_root=None, show_indexes=False):
    """ 
    myserve是对serve的封装，配合urls.py下的media的path请求使用
    保证用户请求media下的静态媒体资源（数据文件 ）时先进行用户检测，不是对应用户的请求就拒绝
    """
    login_username=request.session.get("user_name",False)
    if path.split("/")[1]==login_username:
        return serve(request, path, document_root, show_indexes)
    else:
        return redirect(WORK_URL)

def getcsvinfo(fullfilename):
    """ 
         鼠标悬浮时，需要预览文件内容，提取表头和一行数据，过长只显示部分
    """
    if fullfilename.endswith(".csv"):
        with open(fullfilename,"rb") as ef:
            data=ef.read(3000)
            encodeName=chardet.detect(data).get("encoding")
        fn=pandas.read_csv(fullfilename,nrows=1,encoding=encodeName)
        cl=[str(i) for i in fn.columns.tolist()]
        fl=[str(i) for i in fn.loc[0].tolist()] 
        if len(cl)>6:
            cl=cl[:3]+["..."]+cl[-3:]
            fl=fl[:3]+["..."]+fl[-3:]
        res="\t".join(cl)+"\n"+"\t".join(fl)
        return res
    else:
        return "无法获取"

def delsingle_CR(session,fnames):
    print("del ",fnames)
    for fname in fnames:
        if session.get("work_book") and session["work_book"].filename==fname:
            del session["work_book"]
        elif cache.has_key(session["user_name"]+"::"+fname):
            cache.expire(session["user_name"]+"::"+fname,0)
        else:
            print("没有该文件的图表")
def getCacheChartRenders(userid,username,instance=False,chartids=None):
    """
    @instance：是实例化还是仅仅取用title
    @chartids：筛选部分图表的id
    """
    chart_renders={"user_name":username} if instance else []
    content="chartrender_text"  if instance else  "charttitle"
    kwargs={"author":User.objects.get(id=userid)}
    if chartids and isinstance(chartids, list):
        kwargs.update({"chartid__in":chartids})
    CCRs=CacheChartRender.objects.filter(**kwargs).values_list("chartid",content)
    if instance:
        for ccr in CCRs:
            chart_renders[ccr[0]]=pickle.loads(ccr[1])
    else:
        for ccr in CCRs:
            
            chart_renders.append({"chartid":ccr[0],"charttitle":ccr[1]})
    return chart_renders

def getCacheChart(userid,chartid):
    try:
        chartobjORM=CacheChartRender.objects.get(author=User.objects.get(id=userid),chartid=chartid)
        return pickle.loads(chartobjORM.chartrender_text)
    except CacheChartRender.DoesNotExist:
        raise DrawChartException("临时图表丢失")
    
    