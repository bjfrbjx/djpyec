#  -*- coding:utf-8 -*-
from __future__ import unicode_literals
from pyecharts.chart import Chart
import json
from utils.drawchart import single_chartrender,DrawChartException
import os
from django.shortcuts import render,redirect
from utils.cklogin import login_required, getcsvinfo, delsingle_CR,\
    getCacheChartRenders,  getCacheChart
import pickle
import math
from .models import User,UploadFile,CustomChartFile
from pyecharts import Line3D
from django.core.files.base import File
from djpyec.settings import MEDIA_ROOT ,STATIC_URL,MEDIA_URL
from django.http.response import JsonResponse, FileResponse
from utils.ChartUtils import DrawCustomChart,str2bool
from utils.generatechartoptions import getChartOptions
from djpyec.settings import HOST
from utils.tranchart import getSupporttype
from utils.tensorcase import Oprfuncs,argschanel, select_csv,\
    select_npy
import uuid
import traceback
from pandas.core.series import Series
from pyech.models import CacheChartRender
import copy
ECHARTS_REMOTE_HOST = HOST+STATIC_URL+"JS"

from django.core.cache import cache




"""
session  
    @work_book : 存放用户当前使用的单文件渲染工厂对象
    @user_name : 用户名
    @user_id   : 用户id
    @npy_book  : 加工npy文件产生的临时数据文件
    @chart_render: 存放用户的单图渲染器，既临时图表<体积明显小于导出的代码文本>

"""
@login_required        
def demo3d(request):
    """
    $首页demo
    """
    def demoline3d():
        """
        $3d曲线图
        """
        _data = []
        for t in range(0, 25000):
            _t = t / 1000
            x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
            y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
            z = _t + 2.0 * math.sin(75 * _t)
            _data.append([x, y, z])
        range_color = [
            '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
            '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
        line3d = Line3D("3D line plot demo", width=1200, height=600)
        line3d.add("", _data, is_visualmap=True,
                   visual_range_color=range_color, visual_range=[0, 30],
                   is_grid3d_rotate=True, grid3d_rotate_speed=180)
        return line3d.render_embed() ,line3d.get_js_dependencies()
    
    render_embed =cache.get("render_embed")
    js_dependencies= cache.get("js_dependencies")
    if (render_embed is None) or (js_dependencies is None):
        
        render_embed,js_dependencies=demoline3d()
        cache.set("render_embed",render_embed,60*3)
        cache.set("js_dependencies",js_dependencies,60*3)
    context = dict(
        myechart=render_embed,
        host=ECHARTS_REMOTE_HOST,
        script_list=js_dependencies
    )
    result =render(request,'index_demo.html',context)
    return result




@login_required
def workon(request):
    """
    $工作空间页面，
    return {"files":数据文件 csv npy,
            "chartsfiles":组图网页文件,
            "username":用户名 ,
            "charttypes":支持的图表种类,
            "cachedcharts":缓存的临时单图
    """
    if request.method == "GET" or request.method=="POST":
        userupfiledir=os.path.join(MEDIA_ROOT,"upload",request.session["user_name"])
        usrechartfilesdir=os.path.join(MEDIA_ROOT,"download",request.session["user_name"])
        datafiles=[]
        chartsfiles=[]
        
        if not os.path.exists(userupfiledir):
            os.makedirs(userupfiledir)
        else:
            datafiles=[i for i in os.listdir(userupfiledir)]
            
        if not os.path.exists(usrechartfilesdir):
            os.makedirs(usrechartfilesdir)
        else:
            chartsfiles=[i for i in os.listdir(usrechartfilesdir)]
        temp=getCacheChartRenders(request.session["user_id"],request.session["user_name"]) 
        print(temp)               
        return render(request,"work/upload.html",{"files":datafiles,
                                                  "chartsfiles":chartsfiles,
                                                  "username":request.session["user_name"] ,
                                                  "charttypes":getSupporttype(),
                                                  "cachedcharts":temp})

@login_required
def upload(request):
    """
    $异步上传数据文件
    """
    if request.is_ajax():
        fileobj= File(request.FILES.get("file"))
        if not (fileobj.name.endswith(".csv") or fileobj.name.endswith(".npy")):
            return JsonResponse({"worning":"不能上传csv,npy以外的文件"})
        upfile,exist=UploadFile.objects.get_or_create(author=User.objects.get(id=request.session['user_id']),uploadfile="upload/"+request.session["user_name"]+"/"+request.FILES.get("file").name)
        upfile.uploadfile.save(request.FILES.get("file").name,fileobj)
        upfile.save()
        return JsonResponse({"files":[i for i in os.listdir(os.path.join(MEDIA_ROOT,"upload",request.session["user_name"]))]},safe=False)
    else:
        return redirect("/work/")
@login_required  
def getNdimdict(request):
    """
    $浮动层获取张量指定阶的信息
    """
    errormsg={"worning":"axis读取错误"}
    if request.method == "POST":
        data=json.loads(request.body.decode())
        tm=request.session["npy_book"][data["keyid"]]
        reslist=tm.axisdict[tm.ndimaxis[data["axis"]]]
        return JsonResponse({"ndimlist":reslist},safe=False)
    else:
        return JsonResponse(errormsg,safe=False)

@login_required  
def getMInfo(request):
    """
    $浮动层获取张量最值平均值等信息
    """
    errormsg={"worning":"axis读取错误"}
    if request.method == "POST":
        data=json.loads(request.body.decode())
        tm=request.session["npy_book"][data["keyid"]]
        reslist=[*tm.getM(),tm.shape]
        
        return JsonResponse({"infolist":reslist},safe=False)
    else:
        return JsonResponse(errormsg,safe=False)
@login_required
def hoverheaderinfo(request):
    """
    $鼠标悬停获取表头信息
    """
    errormsg={"worning":"文件读取错误"}
    if request.method == "POST":
        try:
            data=json.loads(request.body.decode())
            filename=data["filename"]
            fullfilename=os.path.join(MEDIA_ROOT,"upload",request.session["user_name"],filename)
            headinfo=getcsvinfo(fullfilename)
            
            return JsonResponse({"headinfo":headinfo},safe=False)
        except Exception as e:
            
            traceback.print_exc()
            return JsonResponse(errormsg,safe=False)
    else:
        return redirect("/work/")
@login_required
def npy2df(request):
    """
    $将张量数据导出为dataframe
    """
    errormsg={"worning":"文件读取错误"}
    if request.method == "POST":
        try:
            data=json.loads(request.body.decode())
            name=data["name"]
            axisname=data["axisname"]
            ndimname=data.get("ndimname",None)
            key=data["keyid"]
            tm=request.session["npy_book"][key]
            tm.setPubaxisdict(ndimname,axisname)
            
            df=tm.Tensor2Dataframe(ismat=data["ismat"],tagargs=data.get("tagargs",None))
            uploadfile="upload/"+request.session["user_name"]+"/"+name+".csv"
            realpath=os.path.join(MEDIA_ROOT,uploadfile)
            df.to_csv(realpath,index=False)
            fileobj= File(realpath)
            upfile,exist=UploadFile.objects.get_or_create(author=User.objects.get(id=request.session['user_id']),uploadfile=uploadfile)
            upfile.save()
            useruploaddir=os.path.join(MEDIA_ROOT,"upload",request.session["user_name"])
            result={"files":[i for i in os.listdir(useruploaddir)]}
            result.update(select_csv(request.session, name+".csv",refresh=True))
            return JsonResponse(result,safe=False)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse(errormsg,safe=False)
    else:
        return redirect("/work/")
    
    



@login_required         
def select(request):
    """
    @ 读取文件，如果时csv文件直接跳到下一步，如果是npy则构建浮动层准备加工
    """
    errormsg={"worning":"文件读取错误"}
    tensorcase=None
    if request.method == "POST":
        data=json.loads(request.body.decode())
        try:
            if data["selected_name"].endswith(".csv"):
                result=select_csv(request.session, data["selected_name"])
            elif data["selected_name"].endswith(".npy"):
                result=select_npy(request.session,data["selected_name"])
            return JsonResponse(result,safe=False)
        except Exception as e:
            
            return JsonResponse(errormsg,safe=False)
    return JsonResponse(errormsg,safe=False)

@login_required         
def nparray_opr(request):
    """
    @ 对npy张量的操作加工
    """
    errormsg={"worning":"npy加载错误"}
    if request.method == "POST":
        data=json.loads(request.body.decode())
        try:
            key=data["keyid"]
            opr=Oprfuncs[data["operation"]]
            args=data["args"]
            tm=request.session["npy_book"][key]
            args=argschanel(args,data["operation"],tm.ndimaxis)
            new_tm=opr(tm,**args)
            new_key="NP"+str(uuid.uuid4())
            request.session["npy_book"][new_key]=new_tm
            ast={"keyid":new_key,"info":[new_tm.shape,new_tm.axisdict,*new_tm.getM()]}
            return JsonResponse({"tensor_model":ast},safe=False)
        except Exception as e:
            
            return JsonResponse(errormsg,safe=False)
    return JsonResponse(errormsg,safe=False)



@login_required
def draw(request):
    """
    $ 进行单图绘制,并且将单图渲染器缓存，作为临时目录
    """
    errormsg={"worning":"绘图出现错误"}
    if request.is_ajax():
        try:
            data=json.loads(request.body.decode())
            data["options"]=str2bool(data["options"])
            single_CR=request.session["work_book"]
            chartobj=single_CR.drawchart(charttype=data['charttype'],dataformats=data['dataformats'],options=data["options"],title=data["title"])
            CacheChartRender.objects.create(author=User.objects.get(id=request.session["user_id"]),chartid=chartobj._chart_id,chartrender_text=pickle.dumps(chartobj),charttitle=data["title"]).save()
            context= dict(
                echart=chartobj.render_embed(),
                chart_id=chartobj._chart_id,
                script_list=chartobj.get_js_dependencies(),
                title=chartobj._option["title"][0]["text"],
                file_name=single_CR.filename,
                host=ECHARTS_REMOTE_HOST)
            return JsonResponse(context,safe=False)   
        except DrawChartException as e:
            errormsg.update(worning=e.wornning())
            return JsonResponse(errormsg,safe=False)
        else:
            return JsonResponse(errormsg,safe=False)
    return JsonResponse(errormsg,safe=False)


@login_required
def conformchart(request):
    """
    $ 进行组图绘制,导出html文件
    """
    errormsg={"worning":"绘图出现错误"}
    if request.is_ajax():
        try:
            data=json.loads(request.body.decode())
            data["options"]=str2bool(data["options"])
            chart_renders=copy.copy(getCacheChartRenders(request.session["user_id"],request.session["user_name"],instance=True,chartids=data["conform_charts"]))
            customchartfilepath=DrawCustomChart( chart_renders, data["customtype"],**data["options"])
            CCF=CustomChartFile(author=User.objects.get(id=request.session["user_id"]),ChartPath=customchartfilepath)
            CCF.save()
            charturl=os.path.join(MEDIA_URL,customchartfilepath)
            return JsonResponse({"customfileurl":charturl},safe=False)
        except DrawChartException as e:
            errormsg.update(worning=e.wornning())
            return JsonResponse(errormsg,safe=False)
    return JsonResponse(errormsg,safe=False)

@login_required
def getchartoptions(request):
    """
    获取该图表的样式参数配置组，方便前端解析和提交
    """
    errormsg={"worning":"配置参数出现错误"}
    if request.is_ajax():
        try:
            data=json.loads(request.body.decode())
            options_list=getChartOptions(data["charttype"])
            return JsonResponse({"options":options_list },safe=False)
        except DrawChartException as e:
            errormsg.update(worning=e.wornning())
            return JsonResponse(errormsg,safe=False)
    return JsonResponse(errormsg,safe=False)

@login_required
def  dataprocess(request):
    """
    简单的网页数据处理，
    """
    errormsg={"worning":"绘图出现错误"}
    if request.is_ajax():
        try:
            data=json.loads(request.body.decode())
            if request.session["work_book"].filename==data['filename']:
                single_CR=request.session["work_book"]
            else:
                single_CR=single_chartrender(MEDIA_ROOT,request.session["user_name"],data["filename"])
            chartobj=single_CR.mathpro(data["mathpro"],data["values"],data["title"] )
            CacheChartRender.objects.create(author=User.objects.get(id=request.session["user_id"]),chartid=chartobj._chart_id,chartrender_text=pickle.loads(chartobj)).save()

            request.session.save()
            context= dict(
                echart=chartobj.render_embed(),
                chart_id=chartobj._chart_id,
                title=chartobj._option["title"][0]["text"]
                )
            return JsonResponse(context,safe=False)   
        except DrawChartException as e: 
            errormsg.update(worning=e.wornning())
            return JsonResponse(errormsg,safe=False)
        else:
            return JsonResponse(errormsg,safe=False)
    return JsonResponse(errormsg,safe=False)

@login_required         
def np_oper(request):
    """
    $ 接受处理操作张量的请求，对其进行截取，归一化.....等操作
    """
    errormsg={"worning":"npy加载错误"}
    if request.method == "POST":
        data=json.loads(request.body.decode())
        try:
            key=data["keyid"]
            tm=request.session["npy_book"][key]
            new_tm=tm.operchanel(data["oper"],axischeck=data.get("axischeck"),ndimcheck=data.get("ndimcheck"))
            new_key=data["new_keyid"]
            request.session["npy_book"][new_key]=new_tm
            ast={"keyid":new_key,"info":[new_tm.shape,new_tm.ndimaxis]}
            return JsonResponse({"tensor_model":ast},safe=False)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse(errormsg,safe=False)
    return JsonResponse(errormsg,safe=False)


@login_required
def delfiles(request):
    """
    删除指定的文件
    """
    errormsg={"worning":"删除文件出现错误"}  
    if request.is_ajax():
        try:
            data=json.loads(request.body.decode())
            pathFieldName=''
            mediadir=''
            filesfilter=None
            if data.get("file_port")=="chartslist":
                pathFieldName="ChartPath__in"
                mediadir='download'
                filesfilter=CustomChartFile.objects.filter(author=User.objects.get(id=request.session['user_id']))
                #删除对应的单文件渲染
            elif data.get("file_port")=="fileslist":
                pathFieldName="uploadfile__in"
                mediadir="upload"
                filesfilter=UploadFile.objects.filter(author=User.objects.get(id=request.session['user_id']))
            elif data.get("file_port")=="cachelist":
                try:
                    del_ids=data["del_files"]
                    CacheChartRender.objects.filter(author=User.objects.get(id=request.session["user_id"]),chartid__in=del_ids).delete()
                    return JsonResponse({},safe=False)
                except Exception as e:
                    return JsonResponse(errormsg,safe=False) 
            else:
                raise DrawChartException("文件目录错误")
            kwargs={pathFieldName:[ mediadir+"/"+request.session["user_name"]+"/"+del_file for del_file in data.get("del_files")]}
            filesfilter.filter(**kwargs).delete()
            delsingle_CR(request.session,data.get("del_files"))
            return JsonResponse({"deleted":True},safe=False)
        except DrawChartException as e:
            errormsg.update(worning=e.wornning())
            return JsonResponse(errormsg,safe=False)
        else:
            return JsonResponse(errormsg,safe=False)
 
@login_required       
def cachechart(request):
    """
    找到缓存在数据库里的，指定的临时单图渲染器，重新渲染出前端代码
    """
    errormsg={"worning":"缓存文件丢失"}  
    if request.is_ajax():
        try:
            data=json.loads(request.body.decode())
            
            chartobj=getCacheChart(request.session["user_id"],data['cachechart_id'])
            context= dict(
                echart=chartobj.render_embed(),
                chart_id=chartobj._chart_id,
                script_list=chartobj.get_js_dependencies(),
                title=chartobj._option["title"][0]["text"],
                host=ECHARTS_REMOTE_HOST
                )
            return JsonResponse(context,safe=False)
        except DrawChartException as e:
            return JsonResponse(errormsg,safe=False)

@login_required
def csv2table(request):
    if request.method == "POST" and request.is_ajax():
        filename=request.POST['fname']
        single_CR=request.session["work_book"]
        if filename==single_CR.filename:
            all_result=single_CR.dataframe
        else:
            fullfilename=os.path.join(MEDIA_URL,"upload",request.session["user_name"],filename)
            print(fullfilename)
            all_result=single_CR.getDataFrame(fullfilename)
        recordsTotal=all_result.shape[0]
            # 第一条数据的起始位置
        start = int(request.POST['start'])
            # 每页显示的长度，默认为10
        length = int(request.POST['length'])
            # 计数器，确保ajax从服务器返回是对应的
        draw = int(request.POST['draw'])
            # 全局收索条件
        new_searchs = request.POST['search[value]']
            # 排序列的序号
        new_order= request.POST['order[0][column]']
            # 排序列名
        by_name = request.POST['columns[{0}][data]'.format(new_order)]
            # 排序类型，升序降序
        fun_order = request.POST['order[0][dir]']
            # 排序开启，匹配表格列
        if by_name:
            if fun_order=="asc":
                ascending=True
            else:
                ascending=False
            all_result=all_result.sort_values(by=by_name , ascending=ascending)
        
            # 模糊查询，包含内容就查询
        if new_searchs:                
            new_searchs=new_searchs.split(" ")
            print(new_searchs)
            allserch=Series([False]*all_result.shape[0])
            for new_search in new_searchs:
                cutsearch=Series([False]*all_result.shape[0])
                for col in all_result.columns:
                    if all_result[col].dtype==str or all_result[col].dtype==object:
                        cutsearch=cutsearch|all_result[col].str.contains(new_search)
                allserch=cutsearch|allserch
            all_result=all_result[allserch]
            # 获取首页的数据
        recordsFiltered=all_result.shape[0]
        datas = all_result.iloc[start:(start+length)].fillna('')
            # 转为字典

        resp  = [dict(obj.items()) for _,obj in datas.iterrows()]
            #返回计数，总条数，返回数据
        result = {
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': recordsFiltered,
            'data': resp,
            }
        return JsonResponse(result,safe=False)
    

@login_required
def structure(request):
    """
    传输指定图表所必须的数据格式信息  {name,xaxis。。。}
    """
    errormsg={"worning":"获取图表构造失败,可能是工作文件已删除，请刷新或重新指定"}  
    print("-------------")
    if request.is_ajax():
        try:
            single_CR=request.session.get("work_book",None)
            if single_CR:
                data=json.loads(request.body.decode())
                return JsonResponse(single_CR.getDataFormat(data['charttype']).clientdatadict,safe=False)
            else:
                return JsonResponse(errormsg,safe=False)
        except DrawChartException as e:
            return JsonResponse(errormsg,safe=False)
    
@login_required
def downloaddatafile(request):
    """
    ￥异步下载数据文件
    """
    errormsg={"worning":"下载失败"}  
    try:
        filename=json.loads(request.body.decode())["filename"]
        
        fullfilename=os.path.join(MEDIA_URL,"upload",request.session["user_name"],filename)
        return JsonResponse({"fileURL":fullfilename},safe=False)
        
    except DrawChartException as e:
        return JsonResponse(errormsg,safe=False)
    