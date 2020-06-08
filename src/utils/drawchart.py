#  -*- coding:utf-8 -*-
'''
Created on 2019年7月21日

@author: 魔天一念
'''
import os
from pandas import read_csv,DataFrame,Series
from utils.tranchart import chartdict,paramsdict
from datetime import datetime
from utils.generatechartoptions import Dataformats
import chardet
import copy
from pyecharts.charts.radar import Radar
from pyecharts.charts.scatter3D import Scatter3D
from copy import deepcopy
# 单图画布长宽
canvas_width=800
canvas_height=400
ec_visual_map = {
                "type": "continuous",
                "inRange": {'color':["#50a3ba", "#eac763", "#d94e5d"]},
                "calculable": True,
                "splitNumber": 5,
                "orient": 'vertical', 
                "left": 'left',
                "top": '20px',
                "showLabel": True,
            }
es_visual_map = {
                "type": "continuous",
                "inRange": {'symbolSize':[10,30]},
                "calculable": True,
                "splitNumber": 5,
                "orient": 'horizontal',
                "left": 'left',
                "top": 'bottom',
                "showLabel": True,
            }
class single_chartrender:
    """
        单文件图表渲染器
    $getDataFormat 获取当前文件的dataframe
    $drawchart 根据charttype绘制单图
    """
    global canvas_width,canvas_height

    def __init__(self,mediaroot,username,filename=None):
        self.username=username
        self.__dataformat=None
        self.__filepath=os.path.join(mediaroot,"upload",username,filename)
        self.filename=filename
        self.dataframe=self.getDataFrame(self.__filepath)
        

        

    def getDataFormat(self,charttype):
        self.__dataformat=Dataformats.get(charttype,None)
        return self.__dataformat   
    
    def __draw(self,ChartCls,final_dataformats,final_options,extra_color=None,extra_size=None,**clsoptions):
        chartobj=ChartCls(**clsoptions)
        for dataformat in final_dataformats:
            if ChartCls==Radar:
                schema=dataformat.pop('schema')
                chartobj.config(schema=schema)
            if type(dataformat)==dict:
                chartobj.add(**dataformat,**final_options)
            else:
                chartobj.add(*dataformat,**final_options)
        # 插入两个visualmap从颜色和大小表示4维度或5维
        if ChartCls==Scatter3D:
            vmlist=[]
            if extra_color:
                extra_color.update(ec_visual_map)
                vmlist.append(extra_color)
            if extra_size:
                extra_size.update(es_visual_map)
                vmlist.append(extra_size)
            print("++++++++++-",vmlist)
            chartobj._option["visualMap"]=vmlist
        return chartobj
    def drawchart(self,charttype="bar",dataformats=None,options=None,title=""):
        """
        $根据charttype绘制单图
        @charttype:图表种类
        @dataformats:基础数据格式 例如{name:[a,b],xaxis:[姓名,学号]，yxais:[英语成绩,数学成绩]}
        @options:样式参数
        """
        ec,es,finaldataformats=self.__dataformatHanding(dataformats)
        ChartCls=self.__getEchartCls(charttype)
        params=self.__getParams(charttype)#默认样式
        if not ChartCls:
            raise DrawChartException("不支持这种图表")
        if not params:
            raise DrawChartException("找不到图表参数")
        if not self.__dataformat:
            self.getDataFormat(charttype)
        tmparams=copy.deepcopy(params)
        tmparams.update(options)
        finaloptions=tmparams
        if finaloptions.get("funnel_gap", None) is not None:
            finaloptions["funnel_gap"]=float(finaloptions["funnel_gap"])
        
        if charttype in ["bar","line"] and len(finaldataformats)*len(finaldataformats[0]['x_axis'])>20:
            finaloptions.update(is_datazoom_show=True)
        clsoptions=dict(title=title,width=canvas_width,height=canvas_height,title_pos="left")
        return self.__draw(ChartCls, finaldataformats, finaloptions,extra_color=ec,extra_size=es,**clsoptions) 
        # ,dict(ChartCls=ChartCls, dataformats=finaldataformats, options=options,clsoptions=clsoptions)

    
    def __check_dataformats(self,dataformats):
        '''
        $校验dataformats的格式是否正确，并且删除空的组
        '''
        length=len(dataformats['name'])
        deltemp=[]
        deltempnum=0
        for idx in range(length):
            if [ v[idx] for k,v in dataformats.items()]==['']*len(dataformats):
                deltemp.append(idx-deltempnum)
                deltempnum+=1
        for i in deltemp:
            for k in dataformats.keys():
                dataformats[k].pop(i)
        return dataformats

    def __scatter3dChant(self,reallistdata,ecv,esv,ein): 
        ec={}
        es={}
        tol=["x","y","z"]
        ecdimension=0
        if ecv:
            if ecv in ein :
                ecdimension=ein.index(ecv)
                ec.update(dimension=ecdimension,
                          text=['color',ecv],
                          min=min(reallistdata[tol[ecdimension]]),
                          max=max(reallistdata[tol[ecdimension]]))
            else:
                ec.update(dimension=3,
                          text=['color',ecv],
                          min=min(reallistdata["extra_color"]),
                          max=max(reallistdata["extra_color"]))
        if esv:
            if esv in ein :
                esdimension=ein.index(esv)
                es.update(dimension=esdimension,
                          text=['size',esv],
                          min=min(reallistdata[tol[esdimension]]),
                          max=max(reallistdata[tol[esdimension]]))
            elif ecdimension!=3:
                es.update(dimension=3,
                          text=['size',esv],
                          min=min(reallistdata["extra_size"]),
                          max=max(reallistdata["extra_size"]))
            else:
                es.update(dimension=4,
                          text=['size',esv],
                          min=min(reallistdata["extra_size"]),
                          max=max(reallistdata["extra_size"])) 
        print("******",ec,es)
        return ec,es
    def __dataformatHanding(self,dataformats):
        '''
         $ 关于dataformat的总操作：
         $校验dataformat的格式，并删除空的组
         $再进行分组 ，并进行数据填充
         $  return    dataformatsresult=={a:{.....}  b:{.....}}
        '''
        dataformats=self.__check_dataformats(dataformats)
        dataformatsresult=[]
        length=len(dataformats['name'])
        for idx in range(length):
            tempdict={}
            for k in dataformats.keys():
                if k=='name':
                    tempdict['name']=dataformats[k][idx]
                # 非必须 +空  忽视跳过
                elif k.startswith("extra") and dataformats[k][idx]=='':
                    continue
                # 必须+空    异常
                elif not k.startswith("extra") and dataformats[k][idx]=='':
                    raise DrawChartException('坐标数据不完整')
                # 非空 填充
                else:
                    tempdict[k]=dataformats[k][idx]

            #替换实际列数据
            reallistdata=self.__dataformat_separate(self.dataframe,tempdict)
            
            # scatter3d特殊处理
            ecv=tempdict.get("extra_color")
            esv=tempdict.get("extra_size")
            print(ecv,"$$$$$$$$$$",esv)
            if ecv or esv:
                ein=[tempdict["x"],tempdict["y"],tempdict["z"]]
                ec,es=self.__scatter3dChant(reallistdata, ecv, esv, ein)  
            else :
                ec,es=None,None
            #有机整合，有的是字典，有的是二元数组
            resdata=self.__dataformat.dataformattranst(reallistdata)
            dataformatsresult.append(resdata)
        
        return ec,es,dataformatsresult
                    

    
    def __dataformat_separate(self,df,dataformat):
        """
        @dataformat: 例如{name:柱状图,xaxis:姓名，yxais:英语成绩}
        return {name:柱状图,xaxis:[张三，李四....]，yxais:[60,57....]}
        $ 将dataformat里的关于df的列名换成实际数据
        """
        dataformat=deepcopy(dataformat)
        allcolumns=df.columns.values.tolist()
        for k,v in dataformat.items():
            if k!='name':
                if v not in allcolumns:
                    raise DrawChartException("表格没有"+str(v)+"这一列")
                # scatter3d特别处理 减少数据量
                elif (k=="extra_color" or k=="extra_size") and k in [dataformat["x"],dataformat["y"],dataformat["z"]]:
                    continue
                else:
                    print(df[v].to_list())
                    dataformat.update({k:df[v].dropna().to_list()})
        return dataformat

    
    def __separate(self,df,axes,values):
        """
        $ 检查@df中是否有axes指定的 列和values指定的列，并且将df按照axes,values分成两个dataframe
        """
        allcolumns=df.columns.values.tolist()
        for axis in axes:
            if axis not in allcolumns:
                raise DrawChartException("表格没有"+str(axis)+"这一列")
        for value in values:
            if value not in allcolumns:
                raise DrawChartException("表格没有"+str(value)+"这一列")
        return (df[axes],df[values])
            
    def getDataFrame(self,csv_file,encode="utf-8"):
        """
        $根据文件名读取文件，因为文件编码不一样，读取时需要指定编码方式，用chardet推测出文件编码
        """
        df=None
        encodeName=None
        with open(csv_file,"rb") as ef:
            data=ef.read(100000)
            encodeName=chardet.detect(data).get("encoding")
        try:
            df=DataFrame(read_csv(csv_file,encoding=encode))
        except Exception :
            df=DataFrame(read_csv(csv_file,encoding=encodeName))
        finally:
            return df
            
    def getColumns(self):
        """
        $获取列名，及表头
        """
        return self.dataframe.columns.to_list()
    def __getEchartCls(self,chartstype):
        """
        $ 获取对应的pyecharts的单图渲染器
        """
        return chartdict.get(chartstype.lower(),None)
    def __getParams(self,chartstype):
        """
        $ 获取对应图表种类的默认样式参数 
        """
        return paramsdict.get(chartstype.lower(),None)
    def getSupporttype(self):
        """
        $ 获取支持的单图种类 
        """
        return tuple(chartdict.keys())
    def __isstr(self,series):
        """ 
        $ 判断某一列是否为字符串类型
        """
        return series.dtype==Series(["o"]).dtype or series.dtype==str
    
    def mathpro(self,mathpro_name,valuesname,base_title):
        """
        $ 简单运算
        @mathpro_name: 四种简单运算
        @valuesname:        需要进行运算的列名
        @base_title:    标题前缀
        """
        global canvas_width,canvas_height
        axisdf,datadf=self.__separate(self.dataframe,[],valuesname)
        Bar=self.__getEchartCls('bar')
        params=self.__getParams('bar')
        mathpro_data=None
        title=None
        if  mathpro_name=="average":
            mathpro_data=datadf.mean().to_list()
            title=base_title+"_"+mathpro_name
        elif  mathpro_name=="min":
            mathpro_data=datadf.min().to_list()
            title=base_title+"_"+mathpro_name
        elif  mathpro_name=="max":
            mathpro_data=datadf.max().to_list()
            title=base_title+"_"+mathpro_name
        elif  mathpro_name=="sum":
            mathpro_data=datadf.sum().to_list()
            title=base_title+"_"+mathpro_name
        bar=Bar(title,datetime.today().strftime("%Y-%m-%d"),width=canvas_width,height=canvas_height,title_pos="left")
        bar.add("", valuesname, mathpro_data ,**params)
        return bar
        


class DrawChartException(Exception):
    """
    异常类型
    """
    def __init__(self,info):
        self.wornningmsg=info
        super().__init__(self,info)
    def wornning(self):
        return self.wornningmsg
    
