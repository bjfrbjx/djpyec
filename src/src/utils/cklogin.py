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