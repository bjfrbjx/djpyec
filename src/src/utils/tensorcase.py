'''
Created on 2020年1月28日

@author: 魔天一念
'''
import numpy as  np
from TensorLib import tools
from pandas import Series ,DataFrame,concat
import copy
import re
from joblib.parallel import delayed
from utils.drawchart import DrawChartException, single_chartrender
import uuid
import os
from djpyec.settings import MEDIA_ROOT
import numpy
from django.core.cache import cache
import pickle
p = re.compile(r'[(](.*?)[)]', 16)



def listprod(la,lb,spltpont="-"):
    """
    $ 将列表内元素全拼接  
    @la:[a,b] 
    @lb :[c,d]
    return [a-c,a-d,b-c,b-d]
    """
    if not isinstance(la, list):
        la=[la]
    if not isinstance(lb, list):
        lb=[lb]
    return [str(a)+spltpont+str(b) for b in lb for a in la ]

class shapeException(Exception):
    def __init__(self,info):
        super.__init__(self,info)
        
        
class TensorModel(object):
    """
    np的array的封装类
    """
    def __init__(self, data,axisdict=None,valueName='value',ndimaxis=None):
        """
        data 张量数据(numpy.narry)
        shape 张量的形状(整数元组)
        axisdict 张量的维度信息，例如{"a":[1,2,3],'b':[3,4,5]}
        ndimaxis 张量的阶数["a","b"]
        """
        if axisdict is None:
            axisdict=dict()
            for i,v in enumerate(data.shape):
                axisdict[i]=list(range(v))
        
        if len(data.shape)!=len(axisdict):
            raise DrawChartException("维度不合")

        self.data=data
        self.shape=data.shape
        self.valueName=valueName
        if ndimaxis is None:
            self.ndimaxis=list(axisdict.keys())
        else:
            self.ndimaxis=ndimaxis
        for i,v in enumerate(self.ndimaxis):
            if data.shape[i]!=len(axisdict[v]):
                
                raise shapeException("第{}维度不合".format(i))
        self.axisdict=axisdict

    def getM(self):
        """
        return 最大值，最小值，平均值 中间值
        """
        return float(axisOpr_max(self)),float(axisOpr_min(self)),float(axisOpr_mean(self)),float(axisOpr_median(self))

    def casshape(self,newshape):
        """
        $ 变形
        """
        if np.prod(self.data.shape)!=np.prod(newshape):
            raise shapeException("size 不一致，无法换形")
        self.shape=self.data.shape=newshape
        self.axisdict={i:list(range(i)) for i in newshape}
        self.ndimaxis=newshape
        
    def setAxisDict(self,newaxisdict):
        """
        setAxisDict 设置AxisDict
        """
        self.axisdict=newaxisdict
        self.ndimaxis=list(newaxisdict.keys())
    def setPubaxisdict(self,axisdict,ndimaxis):
        """
        设置部分AxisDict
        """
        if ndimaxis:
            for i in ndimaxis:
                self.ndimaxis[int(i)]=ndimaxis[i]
        if axisdict:
            for i in axisdict:
                self.axisdict[int(i)]=axisdict[i]
        self.axisdict=dict(zip(self.ndimaxis,self.axisdict.values()))
    def __ChangetoAxis(self,axisindex):
        """
        axisindex 将axisindex的索引表示转化为标签表示  比如  1->成绩
        """
        res={self.ndimaxis[ok]:[self.axisdict[self.ndimaxis[ok]][vidx] for vidx in ov] for ok,ov in axisindex.items()}    
        return res
            
    def __ChangetoIndex(self,axisinfo):
        """
        axisinfo 取子张量的信息{“阶”：[维度,]}  如{'成绩'：[优,良],}==》{1：{5，4}}
               将其转化为索引表示
        """
        IndexAxisInfo={}
        for item in axisinfo:
            itemindex=self.ndimaxis.index(item)
            IndexAxisInfo[itemindex]=tuple(self.axisdict[item].index(i) for i in axisinfo[item])
        return IndexAxisInfo

    def __getCompaxisdict(self,axisinfo):
        """
        用于补全子张量的阶级维度,比如选中{‘性别’：男}
        返回包含其他阶的维度信息：{‘性别’：男 ，'年级': [1, 2, 3], '脱发': [1, 2, 3, 4, 5]}
        :param axisinfo:
        :return:
        """
        for item in self.axisdict:
            if item not in axisinfo:
                axisinfo[item]=self.axisdict[item]
        return axisinfo
    
    def deepcopy(self):
        axisdict=copy.deepcopy(self.axisdict)
        return TensorModel(self.data.copy(),axisdict=axisdict,valueName=self.valueName,ndimaxis=self.ndimaxis)




    def getSonTensorByaxisdict(self,axisinfo,pure=False):
        """
                取子张量操作
        axisinfo 取子张量的信息{“阶”：[维度,]}  如{'成绩'：[50,51],}
        """
        
        if all(isinstance(i, int) for i in axisinfo.keys()) and all(all(isinstance(k, int) for k in j) for j in axisinfo.values()):
            IndexAxisInfo=copy.deepcopy(axisinfo)
            k=axisinfo.keys()
            for i,v in enumerate(self.shape):
                if i not in k:
                    axisinfo[i]=tuple(range(v))
            NewAxisInfo=self.__ChangetoAxis(axisinfo)
        else:
            NewAxisInfo=self.__getCompaxisdict(axisinfo)
            IndexAxisInfo=self.__ChangetoIndex(NewAxisInfo)
        data=self.data
        l=len(self.shape)
        for i in IndexAxisInfo:
            casestr="data[{}{}{}]".format(":,"*i,repr(IndexAxisInfo[i]),",:"*(l-1-i))
            data=eval(casestr)
        return  data if pure else TensorModel(data,axisdict=NewAxisInfo,valueName=self.valueName,ndimaxis=self.ndimaxis)

    def TensorOperations(self,func,*args,**kwargs):
        """
        func(self.data,axis=axis)
        张量操作 ：累加cumsum，求和sum，累乘cumprod，求比例，平均值，中间值，最大值
        :param func:
        :param argtensor:
        :return:
        """
        return TensorModel(func(self.data,*args,**kwargs),copy.deepcopy(self.axisdict))
    def ndimlistprod(self,ndls,spltpont="—"):
        """
        $ 列表组全排序拼接
        @ndls: [[a,b,c],[d,e],[f,g]]
        return [a-d-f，a-d-g,... , c-e-g]
        """
        t=ndls[0]
        for nd in ndls[1:]:
            t=listprod(t,nd,spltpont=spltpont)
        return t
    def __check_grpcond(self,grpcondstr):
        """
        $ 校验分组条件语句
        @grpcondstr: 分组条件语句
        """
        v=0
        grpcondstr=grpcondstr.lower()
        if grpcondstr!="all" and not "v" in grpcondstr:
            raise shapeException("条件语句不合规范，请用ALL或者v==0或者v>1 或者 (v>1)|(v<-1)或者(v<1)&(v>-1) 的格式")
        try:
            eval(grpcondstr)
            return True
        except:
            raise shapeException("条件语句不合规范，请用ALL或者v==0或者v>1 或者 (v>1)|(v<-1)或者(v<1)&(v>-1) 的格式")
    def Tensor2Dataframe(self,ismat,tagargs=None):
        """
        $ 张量转化为dataframe
        @ismat:        坐标化             或者     矩阵化
        @tagargs: 分组条件语句列表    或者    列名列表
        """
        if ismat:
            if tagargs:
                matrixcolumns=tagargs
            else:
                matrixcolumns=[self.ndimaxis[0],]
            if len(self.data.shape)==len(self.ndimaxis)==1:
                indexcol=Series(self.axisdict[self.ndimaxis[0]])
                datacol=Series(np.squeeze(self.data))
                return DataFrame(list(zip(indexcol, datacol)),columns=(self.ndimaxis[0],"value"))
            else:
                shapelen=len(self.shape)
                tmpaxisdict=copy.deepcopy(self.axisdict)
                cls=[]
                for mc in matrixcolumns:
                    if isinstance(mc, int) or (mc.isdigit() and not mc.startswith("0")) or (mc[1:].isdigit() and mc.startswith("-")):#索引记号
                        if int(mc)<shapelen and int(mc)>=-shapelen:
                            cls.append(tmpaxisdict[self.ndimaxis[int(mc)]])
                        else :
                            continue
                    else:#便签记号
                        if mc in tmpaxisdict:
                            cls.append(tmpaxisdict[mc])
                        else:
                            continue
                    del tmpaxisdict[mc]
                rls=list(tmpaxisdict.values())
                fromcls=[self.ndimaxis.index(i) for i in matrixcolumns]
                tocls=list(range(shapelen-len(fromcls),shapelen))
                newdata=np.moveaxis(self.data,fromcls,tocls)
                matshape=(np.prod(newdata.shape[0:shapelen-len(fromcls)]),np.prod(newdata.shape[shapelen-len(fromcls):]))
                
                matdata=self.data.reshape(matshape)
                clsname=self.ndimlistprod(cls)
                rlsname=self.ndimlistprod(rls)
                indexcol=Series(rlsname)
                datacols=DataFrame(matdata)
                resultdata=concat([indexcol,datacols],axis=1)
                resultdata.columns=["&".join(tmpaxisdict.keys()),]+clsname
                return resultdata
                
        else:#坐标化
            if tagargs:
                grpconds=tagargs
            else :
                grpconds=["ALL"]
            dfstmp=[]
            for grpcond in grpconds:
                if grpcond is None or grpcond.strip()=="":
                    continue
                if grpcond.upper().strip()=="ALL":
                    grpcond="v==v"
                if self.__check_grpcond(grpcond):
                    V=v=self.data
                    grpdataindex=np.where(eval(grpcond))# locals={"v":v}
                    grpdatavalue=v[grpdataindex]
                    susfix="" if grpcond.lower()=="v==v" else "["+grpcond+"]" 
                    columns=[str(k)+susfix for k in self.ndimaxis]+["value"+susfix,]
                    nandata = np.full((grpdatavalue.size,len(grpdataindex)+1), np.nan)
                    
                    subsdf=DataFrame(data=nandata,columns=columns,dtype=str)
                    for idx,val in enumerate(columns[:-1]):
                        subsdf[val]=grpdataindex[idx]
                    subsdf["value"+susfix]=grpdatavalue
                    dfstmp.append(subsdf)
            tmpaxisdict=copy.deepcopy(self.axisdict)#坐标轴矩阵，空值填充
            maxlen= max(self.shape)
            tmpk=list(tmpaxisdict.keys())
            for k in tmpk:
                tmpaxisdict[str(k)+"轴"]=tmpaxisdict[k]+[None]*(maxlen-len(tmpaxisdict[k]))
                del tmpaxisdict[k]
            dfstmp.append(DataFrame(data=tmpaxisdict))
            return concat(dfstmp,axis=1)

    
            columns=self.ndimaxis+['value',]
            nandata = np.full((len(self.data.flat),len(columns), np.nan))
            subsdf=DataFrame(data=nandata,columns=columns,dtype=str)#数值矩阵
            tmpaxisdict=copy.deepcopy(self.axisdict)#坐标轴矩阵，空值填充
            maxlen= max(self.shape)
            tmpk=list(tmpaxisdict.keys())
            for k in tmpk:
                tmpaxisdict[str(k)+"轴"]=tmpaxisdict[k]+[None]*(maxlen-len(tmpaxisdict[k]))
                del tmpaxisdict[k]
                
            coldf=DataFrame(data=tmpaxisdict)
            axisvalues=tuple(self.axisdict.values())
            for idx,flatv in enumerate(self.data.flat):
                for i,v in enumerate(tools.ind2sub(self.shape,idx)):
                    subsdf.iat[idx,i]=v #axisvalues[i][v]
                subsdf.at[idx,'value']=flatv
            return concat([subsdf,coldf],axis=1)
    def operchanel(self,opertype,axischeck=None,ndimcheck=None):
        """
        $ 对张量的操作
        @opertype: 操作类型
        @axischeck: 操作所指定的轴
        @ndimcheck: 截取指定的维度
        $先截取子张量
        $在根据操作类型和指定轴对子张量操作
        """
        
        #1 ndimcheck 截取子张量
        data=self.data
        if ndimcheck:
            deltmp={}
            
            for i,v in ndimcheck.items():
                deltmp[int(i)]=[int(k) for k in v]
            data=self.getSonTensorByaxisdict(deltmp,pure=True)
        #2 axischeck 操作
        
        opr=Oprfuncs[opertype]
        
        if axischeck and opertype!="截取子张量":
            for i,v in enumerate(axischeck):
                data=opr(data,axis=int(v),pure=True)
        elif opertype=="绝对值":
            data=opr(data,pure=True)
        return TensorModel(data.squeeze())
            
        
def Proportion(data,axis=None):
    """
    $ 归一化操作 就是求比例
    先求指定axis的和张量
    将原张量的axis轴移到0再除以和张量
    结果移轴复原就是归一化
    """
    if axis is not None:
        s=np.sum(data,axis=axis)
        return np.moveaxis(np.divide(np.moveaxis(data,axis,0),s),0,axis)
    else:
        return data/np.sum(data)

def axisOpr_Proportion(tensor,*args,**kwargs):
    """
    $ 归一化
    """
    if kwargs.get('pure',False) and isinstance(tensor, np.ndarray):
        axis=kwargs['axis']
        new_data=Proportion(tensor.data,axis=axis)
        return new_data
    new_axisdict=copy.deepcopy(tensor.axisdict)
    if isinstance(kwargs.get('axis',None),int) :
        axis=kwargs['axis']
        new_data=Proportion(tensor.data,axis=axis)
    else:
        new_data=Proportion(tensor.data)
    return TensorModel(new_data,new_axisdict,valueName = "比例"+tensor.valueName,ndimaxis=tensor.ndimaxis)

def axisOpr_cumsum(tensor,*args,**kwargs):
    """
    $ 累加
    """
    if kwargs.get('pure',False) and isinstance(tensor, np.ndarray):
        axis=kwargs['axis']
        new_data = np.cumsum(tensor,axis=axis)
        shape=list(tensor.shape)
        shape[axis]=1
        shape=tuple(shape)
        casestr="new_data[{}{}].reshape{}".format(":,"*axis,"-1",repr(shape))
        return eval(casestr)
    new_data=np.cumsum(tensor.data,*args,**kwargs)
    if isinstance(kwargs.get('axis',None),int) :
        new_ndimaxis=tensor.ndimaxis.copy()
        new_axisdict=copy.deepcopy(tensor.axisdict)
        axis=kwargs['axis']
        oldaxis=tensor.ndimaxis[axis]
        m=new_axisdict[new_ndimaxis[axis]]
        new_ndimaxis[axis]="累加"+str(new_ndimaxis[axis])
        new_axisdict[new_ndimaxis[axis]]=[i for i in m]
        del new_axisdict[oldaxis]
        return TensorModel(new_data,new_axisdict,ndimaxis=new_ndimaxis,valueName = "累和"+tensor.valueName)
    return TensorModel(new_data,valueName = "累和"+tensor.valueName)

def axisOpr_cumpro(tensor,*args,**kwargs):
    """
    $ 累积
    """
    if kwargs.get('pure',False) and isinstance(tensor, np.ndarray):
        axis=kwargs['axis']
        new_data = np.cumprod(tensor,axis=axis)
        shape=list(tensor.shape)
        shape[axis]=1
        shape=tuple(shape)
        casestr="new_data[{}{}].reshape{}".format(":,"*axis,"-1",repr(shape))
        k=eval(casestr)
        
        return eval(casestr)
    new_data=np.cumprod(tensor.data,*args,**kwargs)
    if isinstance(kwargs.get('axis',None),int) :
        new_ndimaxis=tensor.ndimaxis.copy()
        new_axisdict=copy.deepcopy(tensor.axisdict)
        axis=kwargs['axis']
        oldaxis=tensor.ndimaxis[axis]
        m=new_axisdict[new_ndimaxis[axis]]
        new_ndimaxis[axis]="累乘"+str(new_ndimaxis[axis])
        new_axisdict[new_ndimaxis[axis]]=[i for i in m]
        del new_axisdict[oldaxis]
        return TensorModel(new_data,new_axisdict,ndimaxis=new_ndimaxis,valueName = "累积"+tensor.valueName)
    return TensorModel(new_data,valueName = "累积"+tensor.valueName)

def axisOpr_median(tensor,*args,**kwargs):
    """
    $ 中间值
    """
    if kwargs.get('pure',False) and isinstance(tensor, np.ndarray):
        axis=kwargs['axis']
        new_data = np.median(tensor,axis=axis)
        shape=list(tensor.shape)
        shape[axis]=1
        shape=tuple(shape)
        casestr="new_data.reshape{}".format(repr(shape))
        return eval(casestr)
    new_data=np.median(tensor.data,*args,**kwargs)
    if isinstance(kwargs.get('axis',None),int) :
        new_ndimaxis=tensor.ndimaxis.copy()
        new_axisdict=copy.deepcopy(tensor.axisdict)
        axis=kwargs['axis']
        del new_axisdict[tensor.ndimaxis[axis]]
        del new_ndimaxis[axis]
        return TensorModel(new_data,new_axisdict,valueName="中间值"+tensor.valueName,ndimaxis=new_ndimaxis)
    return new_data

def axisOpr_max(tensor,*args,**kwargs):
    """
    $ 最大值
    """
    if kwargs.get('pure',False) and isinstance(tensor, np.ndarray):
        axis=kwargs['axis']
        new_data = np.max(tensor,axis=axis)
        shape=list(tensor.shape)
        shape[axis]=1
        shape=tuple(shape)
        casestr="new_data.reshape{}".format(repr(shape))
        return eval(casestr)
    new_data=np.max(tensor.data,*args,**kwargs)
    if isinstance(kwargs.get('axis',None),int) :
        new_axisdict=copy.deepcopy(tensor.axisdict)
        new_ndimaxis=tensor.ndimaxis.copy()
        axis=kwargs['axis']
        del new_axisdict[tensor.ndimaxis[axis]]
        del new_ndimaxis[axis]
        return TensorModel(new_data,new_axisdict,valueName="最大值"+tensor.valueName,ndimaxis=new_ndimaxis)
    return new_data
def axisOpr_min(tensor,*args,**kwargs):
    """
    $ 最小值
    """
    if kwargs.get('pure',False) and isinstance(tensor, np.ndarray):
        axis=kwargs['axis']
        new_data = np.min(tensor,axis=axis)
        shape=list(tensor.shape)
        shape[axis]=1
        shape=tuple(shape)
        casestr="new_data.reshape{}".format(repr(shape))
        return eval(casestr)
    new_data=np.min(tensor.data,*args,**kwargs)
    if isinstance(kwargs.get('axis',None),int) :
        new_axisdict=copy.deepcopy(tensor.axisdict)
        new_ndimaxis=tensor.ndimaxis.copy()
        axis=kwargs['axis']
        del new_axisdict[tensor.ndimaxis[axis]]
        del new_ndimaxis[axis]
        return TensorModel(new_data,new_axisdict,valueName="最小值"+tensor.valueName,ndimaxis=new_ndimaxis)
    return new_data

def axisOpr_mean(tensor,*args,**kwargs):
    """
    $ 平均值
    """
    if kwargs.get('pure',False) and isinstance(tensor, np.ndarray):
        axis=kwargs['axis']
        new_data = np.mean(tensor,axis=axis)
        shape=list(tensor.shape)
        shape[axis]=1
        shape=tuple(shape)
        casestr="new_data.reshape{}".format(repr(shape))
        return eval(casestr)
    new_data=np.mean(tensor.data,*args,**kwargs)
    if isinstance(kwargs.get('axis',None),int) :
        new_axisdict=copy.deepcopy(tensor.axisdict)
        new_ndimaxis=tensor.ndimaxis.copy()
        axis=kwargs['axis']
        del new_axisdict[tensor.ndimaxis[axis]]
        del new_ndimaxis[axis]
        return TensorModel(new_data,new_axisdict,valueName="平均值"+tensor.valueName,ndimaxis=new_ndimaxis)
    return new_data

def axisOpr_abs(tensor,*args,**kwargs):
    if kwargs.get('pure',False) and isinstance(tensor, np.ndarray):
        return np.abs(tensor)
    new_data=np.abs(tensor.data)
    new_axisdict=copy.deepcopy(tensor.axisdict)
    return TensorModel(new_data,new_axisdict,valueName="绝对值"+tensor.valueName,ndimaxis=tensor.ndimaxis)

def axisOpr_moveaxis(tensor,source, destination):
    new_data=np.moveaxis(tensor.data,source, destination)
    old_ndimaxis=list(tensor.ndimaxis)
    new_ndimaxis=[None]*len(old_ndimaxis)
    for s,d in zip(source,destination):
        new_ndimaxis[d]=old_ndimaxis[s]
    allsource=range(len(old_ndimaxis))
    for s in allsource:
        if s not in source:
            new_ndimaxis[new_ndimaxis.index(None)]=old_ndimaxis[s]
    return TensorModel(new_data,tensor.axisdict,ndimaxis=new_ndimaxis)



def axisOpr_squeeze(tensor,*args,**kwargs):
    """
    $ 去除冗余的阶 3，1，4  ->   3，4
    """
    if kwargs.get('pure',False) and isinstance(tensor, np.ndarray):
        return np.squeeze(tensor)
    new_data=np.squeeze(tensor.data,*args,**kwargs)
    new_axisdict=copy.deepcopy(tensor.axisdict)
    new_ndimaxis=tensor.ndimaxis.copy()
    if isinstance(kwargs.get('axis',None),int) :
        axis=kwargs['axis']
        oldaxis=new_ndimaxis[axis]
        del new_ndimaxis[axis]
        del new_axisdict[oldaxis]
    else: #if kwargs.get('axis',None) is None
        rmk=[]
        for key in new_ndimaxis:
            if len(new_axisdict[key])==1:
                rmk.append(key)
                del new_axisdict[key]
        for key in rmk:
            new_ndimaxis.remove(key)
    return TensorModel(new_data,new_axisdict)

def axisOpr_renameValue(tensor,valueName):
    new_tensor=copy.copy(tensor)
    new_tensor.valueName=valueName
    return new_tensor

def axisOpr_renameAxisdict(tensor,axisdict):
    """
    $ 修改axisdict 更改维度信息
    """
    tensor=copy.copy(tensor)
    tup=tuple(len(i) for i in axisdict.values())
    if tensor.data.shape!=tup and np.prod(tup)== np.prod(tensor.data.shape):
        tensor=axisOpr_reshape(tensor,tup)
    tensor.axisdict=axisdict
    tensor.ndimaxis=list(axisdict.keys())
    return tensor

def axisOpr_reshape(tensor,newshape):
    tensor=copy.copy(tensor)
    tensor.casshape(newshape)
    return tensor
def axisOpr_cuttensor(tensor,axisdict):
    return tensor.getSonTensorByaxisdict(axisdict)
        

    
def argschanel(args,opertype,ndimaxis=None):
    """
    $根据操作种类转化操作的参数
    """
    if opertype =="绝对值":
        return {}
    elif opertype in ['累加','累积','比例','中间值','平均值','最大值','最小值',"去除多余阶"]:
        args=args.replace("axis","").strip()
        args=args.replace("=","").strip()
        args=args.replace(" ","").strip()
        if args=="" or args.upper()=="NONE" or args.upper()=="NULL":
            return {"axis":None}
        elif args.isdigit():
            return {"axis":int(args)}
        else:
            return {"axis":ndimaxis.index(args)}
#     elif opertype =="移轴":
#         args=args.replace("，",",").replace("；",";").replace("{","[").replace("}","]").replace("（","(").replace("）",")")
#         argscell=re.findall(p, args)
#         return {"source":eval("["+argscell[0]+"]"),"destination":eval("["+argscell[1]+"]")}
#     elif opertype =="值命名":
#         return {"valueName":args}
    elif opertype in ["维度设置","截取子张量"]:
        args=args.replace("，",",").replace("；",";")
        return {"axisdict":eval(args)}
    elif opertype =="重塑形状":
        args=args.replace("，",",").replace("；",";").replace("{","(").replace("}","")
        return {"newshape":eval(args)}   
    else :
        raise shapeException("暂不支持这种处理方法")     
    
    
Oprfuncs={
    '累加':axisOpr_cumsum,
    '累积':axisOpr_cumpro,
    '归一化':axisOpr_Proportion,
    '绝对值':axisOpr_abs,
    # '移轴':axisOpr_moveaxis,
    '中间值':axisOpr_median,
    '平均值':axisOpr_mean,
    '最大值':axisOpr_max,
    '最小值':axisOpr_min,
    # '去除多余阶':axisOpr_squeeze,
    # '值命名':axisOpr_renameValue,
    # '维度设置':axisOpr_renameAxisdict,
    # '重塑形状':axisOpr_reshape,
    '截取子张量':axisOpr_cuttensor
}


def select_npy(request,data):
    """
    选取npy文件
    """
    Tensorcase=None
    key="NP"+str(uuid.uuid4())
    realpath=os.path.join(MEDIA_ROOT,"upload",request.session["user_name"],data["selected_name"])
    np_array=numpy.load(realpath).squeeze()
    tm=TensorModel(np_array)
    request.session["npy_book"]={key:tm}
    ast={"keyid":key,"info":[tm.shape,tm.ndimaxis]}
    return {"tensor_model":ast,"operations":list(Oprfuncs.keys()),"uptype":"npy"}
    
    
def select_csv(request,data,refresh=False):
    """
    选取csv文件
    @refresh: 刷新缓存，当文件内容更改时，需要刷新
    """
    print("select_csv")
    if refresh is False:
        if request.session.get("work_book",False) and request.session["work_book"].filename==data["selected_name"]:
            return {"items":request.session["work_book"].getColumns(),"uptype":"csv"}
        
        single_CR=None
        key=request.session["user_name"]+"::"+data["selected_name"]
        if cache.has_key(key):
            single_CR=pickle.loads(cache.get(key))
            cache.expire(key,60)
        elif request.session.get("work_book",None) is not None:
            oldpkstr=pickle.dumps(request.session["work_book"])
            old_work_bookkey=request.session["user_name"]+"::"+request.session["work_book"].filename
            cache.set(old_work_bookkey,oldpkstr,60*5)
            single_CR=single_chartrender(MEDIA_ROOT,request.session["user_name"],data["selected_name"])
            pkstr=pickle.dumps(single_CR)
            cache.set(key,pkstr,60*5)
        else:
            single_CR=single_chartrender(MEDIA_ROOT,request.session["user_name"],data["selected_name"])
    else:
        single_CR=single_chartrender(MEDIA_ROOT,request.session["user_name"],data["selected_name"])
    request.session["work_book"]=single_CR
    cols=[{"data":c,"title":c} for c in single_CR.dataframe.columns]
    print(cols)
    return {"items":single_CR.getColumns(),"uptype":"csv","cols":cols}

if __name__=="__main__":
    tensork=TensorModel(np.arange(1,121,1).reshape(2,3,4,5),{"性别":["男","女"],"年级":[1,2,3],"压力":['a','b','c','d'],"脱发":[1,2,3,4,5]})
    p=tensork.TensorOperations(np.cumsum,axis=0)
    print(tensork.data)
    print("--------------------------------------------")
    print(p.data)