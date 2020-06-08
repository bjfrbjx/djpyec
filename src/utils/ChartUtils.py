#  -*- coding:utf-8 -*-
'''
Created on 2019年7月21日

@author: 魔天一念
'''
from .tranchart import custom_chart
from .drawchart import DrawChartException
from djpyec.settings import MEDIA_ROOT
from os import makedirs,path
from datetime import datetime
from pyecharts import Line,Bar,Kline,Scatter,EffectScatter,HeatMap,Boxplot,Pie
from pyecharts import Page,Grid,Overlap,Timeline
# 组合图表的默认长宽和间隔距离
WIDTH=1600
HEIGHT=800
INTERVAL=60

#grid并行组图允许的图表种类
grid_enable_charts=(Line,Bar,Kline,Scatter,EffectScatter,HeatMap,Boxplot,Pie)
def ck_enable_grid(chartobj):
    """ 
     确认grid支持这种图表
    """
    global grid_enable_charts
    #return isinstance(chartobj, grid_enable_charts)
    return True


def getCustom_chart(customtype):
    """ 
     获取组图类的工厂对象
    """
    return custom_chart.get(customtype.lower(),None)

def page_custom_chart(chart_renders,**kwargs):
    """ 
    顺序组图：
      @single_chart_ids :  选择的单图id
      @chart_renders :    单图渲染器字典，
      return 根据id找到对应渲染器，通过pyecharts的顺序组图生成器-page 生成这些单图的顺序组图
    """
    page=Page(page_title=kwargs.get("page_title","PAGE_TITLE"))
    for _,single_chart in chart_renders.items():
        if _ !="user_name":
            if single_chart :
                page.add(single_chart)
            else:
                raise DrawChartException("服务器未找到图表,可能已被删除")
    return page


def grid_custom_chart(chart_renders,**kwargs):
    """ 
    并行组图：
      @single_chart_ids :  选择的单图id
      @chart_renders :    单图渲染器字典，
      @kwargs 中的single_option  根据对应参数对每个单图进行定位，没有就是默认定位
      return 根据id找到对应渲染器，通过pyecharts的并行组图生成器-grid 生成这些单图的并行组图
    """
    global WIDTH,HEIGHT
    container_width=float(kwargs.get("width",WIDTH))
    container_height=float(kwargs.get("height",HEIGHT))
    grid=Grid(page_title=kwargs.get("page_title","PAGE_TITLE"),width=container_width,height=container_height)
    kwargs.update({"user_name":chart_renders.pop("user_name")})
    chartsnum=len(chart_renders )
    if chartsnum==1:
        auto_width=container_width
        auto_height=container_height
    else:
        auto_width=container_width/(chartsnum//2)-(chartsnum//2)*INTERVAL
        auto_height=container_height/2-INTERVAL
    
    print("len-",len(chart_renders.keys()))
    for idx,single_chart_id in enumerate(chart_renders.keys()):
        single_chart=chart_renders.get(single_chart_id)
        if single_chart:
            if not ck_enable_grid(single_chart):
                raise DrawChartException("grid仅支持Line,Bar,Kline,Scatter,EffectScatter,HeatMap,pie")
            single_chart._option.pop("toolbox",None)
            single_option=kwargs.get(single_chart_id,None)
            if single_option:
                # 根据参数对每个单图进行定位
                x0=float(single_option.get("grid_left"))
                y0=float(single_option.get("grid_top"))
                this_width=float(single_option.get("grid_width"))
                this_height=float(single_option.get("grid_height"))
                
                single_chart._option["title"][0]["left"]=x0
                single_chart._option["title"][0]["top"]=y0
                single_chart._option["legend"][0]["left"]=x0+150
                single_chart._option["legend"][0]["top"]=y0
                if isinstance(single_chart,Pie):
                    single_chart._option["series"][0]["center"]=[x0+this_width/2,y0+this_height/2]
                    r_bz=min(this_width,this_height)
                    r,R=single_chart._option["series"][0]["radius"]
                    if "%" in r :
                        r=float(r.strip('%'))*0.008*r_bz
                    if "%" in R :
                        R=float(R.strip('%'))*0.008*r_bz
                    single_chart._option["series"][0]["radius"]=[r,R]                    
                grid.add(single_chart,
                         grid_left=x0,
                         grid_top=y0+INTERVAL,
                         grid_width=this_width,
                         grid_height=this_height
                         )
            else:
                # 默认定位 
                x0=single_chart._option["title"][0]["left"]=(INTERVAL+auto_width)*(idx//2)+INTERVAL//2
                y0=single_chart._option["title"][0]["top"]=(auto_height+INTERVAL)*(idx%2)
                single_chart._option["legend"][0]["left"]=x0+150
                single_chart._option["legend"][0]["top"]=y0
                grid_left=x0+INTERVAL//2
                grid_top=y0+INTERVAL//2
                if isinstance(single_chart,Pie):
                    single_chart._option["series"][0]["center"]=[x0+auto_width//2,y0+auto_height//2]
                    r_bz=min(auto_width,auto_height)
                    r,R=single_chart._option["series"][0]["radius"]
                    if "%" in r :
                        r=float(r.strip('%'))*0.008*r_bz
                    if "%" in R :
                        R=float(R.strip('%'))*0.008*r_bz
                    single_chart._option["series"][0]["radius"]=[r,R]
                print(single_chart_id,single_chart)
                grid.add(single_chart,
                                grid_left=grid_left,
                                grid_top=grid_top,
                                grid_width=auto_width,
                                grid_height=auto_height,#grid_bottom=single_chart._option["title"][0]["top"]+auto_height
                                )
        else:
            raise DrawChartException("服务器未找到图表,可能已被删除")
    chart_renders.update({"user_name":kwargs.pop("user_name")})
    return grid

def overlap_custom_chart(chart_renders,**kwargs):
    """ 
    叠加组图：
      @single_chart_ids :  选择的单图id
      @chart_renders :    单图渲染器字典，
      return 根据id找到对应渲染器，通过pyecharts的叠加组图生成器-overloap 生成这些单图的叠加组图
    """
    global INTERVAL,WIDTH,HEIGHT
    container_width=float(kwargs.get("width",WIDTH))
    container_height=float(kwargs.get("height",HEIGHT))
    overlap=Overlap(page_title=kwargs.get("page_title","PAGE_TITLE"),width=container_width,height=container_height)
    x,y=0,0
    kwargs.update({"user_name":chart_renders.pop("user_name")})
    for single_chart_id,single_chart in chart_renders.items():
        if single_chart:
            if not single_chart._option.get("xAxis"):
                raise DrawChartException("overlap ,只能叠加有xy轴的图表")
            single_chart._option.pop("toolbox",None)
            single_option=kwargs.get(single_chart_id,None)
            if single_option:
                xaxis_index,yaxis_index=0,0
                is_add_xaxis,is_add_xaxis=False,False
                if single_option.get("extra_xaxis",False):
                    is_add_xaxis=True
                    x+=1
                    xaxis_index=x
                if single_option.get("extra_yaxis",False):
                    is_add_yaxis=True
                    y+=1
                    yaxis_index=y   
                overlap.add(single_chart,
                            xaxis_index=xaxis_index,
                            yaxis_index=yaxis_index,
                            is_add_xaxis=is_add_xaxis,
                            is_add_yaxis=is_add_yaxis)
            else:
                overlap.add(single_chart)
            
        else:
            raise DrawChartException("服务器未找到图表,可能已被删除")
    chart_renders.update({"user_name":kwargs.pop("user_name")})
    return overlap


def timeline_custom_chart(chart_renders,**kwargs):
    """
    时间轮播组图：
      @single_chart_ids :  选择的单图id
      @chart_renders :    单图渲染器字典，
      return 根据id找到对应渲染器，通过pyecharts的轮播组图生成器-timeline 生成这些单图的轮播组图
     @kwargs：
        is_loop_play=True,循环播放
        is_rewind_play=False,可以倒序播放
        is_timeline_show=True,显示时间线
        timeline_play_interval=2000,间隔
    
    """
    global INTERVAL,WIDTH,HEIGHT
    page_title=kwargs.pop("page_title","PAGE_TITLE")
    container_width=float(kwargs.pop("width",WIDTH))
    container_height=float(kwargs.pop("height",HEIGHT))

    single_option={}
    for i in chart_renders.keys():
        single_option[i]=kwargs.pop(i,None)
    m=chart_renders.pop("user_name")
    timeline=Timeline(page_title=page_title,width=container_width,height=container_height,**kwargs)
    for single_chart_id,single_chart in chart_renders.items():
        if single_chart:
            single_chart._option.pop("toolbox",None)
            if single_option[single_chart_id]:
                time_point=single_option[single_chart_id]["time_point"]
            else:
                time_point=single_chart._option["title"][0]["text"]
            timeline.add(single_chart,time_point)
        else:
            raise DrawChartException("服务器未找到图表,可能已被删除")
    print("oooooooooooooooo")
    chart_renders.update({"user_name":m})
    return timeline
    

def str2bool(strlist):
    """
        将字典中的字符串转化为bool：
        '' None Null undefined 'false'   ==>false
    """
    rmtemp=[]
    print(strlist)
    for key  in strlist:
        if type(strlist[key])==dict:
            vs=list(strlist[key].values())
            if not all(vs):
                rmtemp.append(key)    
        elif isinstance(strlist[key], str):
            if strlist[key]=="false":
                strlist[key]=False
            elif strlist[key]=="true":
                strlist[key]=True
            elif strlist[key].lower()=="none" or strlist[key].lower()=="undefined": 
                rmtemp.append(key)
            
    for rmkey in rmtemp:
        del strlist[rmkey]
    return strlist

def DrawCustomChart(chart_renders,customtype='page',**kwargs):
    """
       组图选择器：根据customtype选择组图
           @customtype : 组图类型，pyecharts有四种
          @single_chart_ids :  选择的单图id
          @chart_renders :    单图渲染器字典，
          
          生成组图后渲染出网页代码，保存到服务器硬盘并返回相对路径
    """
    if customtype=='page':
        CustomChart= page_custom_chart(chart_renders,**kwargs)
    elif customtype=='grid':
        CustomChart= grid_custom_chart(chart_renders,**kwargs)
                
    elif customtype=="overlap":
        CustomChart= overlap_custom_chart(chart_renders,**kwargs)
                
    elif customtype=="timeline":
        CustomChart= timeline_custom_chart(chart_renders,**kwargs)
            
    userdir=path.join(MEDIA_ROOT,"download",chart_renders["user_name"])
    if not path.exists(userdir):
        makedirs(userdir)
    filepath=path.join(userdir,CustomChart.page_title+ datetime.now().strftime("%d-%H-%M-%S")+".html")
    CustomChart.render(path=filepath)
    return "download/"+chart_renders["user_name"]+"/"+CustomChart.page_title+ datetime.now().strftime("%d-%H-%M-%S")+".html"
    