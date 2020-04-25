class SingleChartsOption:
    """
    样式参数单位类，目的是构建前端后端的样式参数映射,通过keys和__getitem__可以在__tran_dicts时直接字典化。
    比如样式参数，有line_type 只能选('solid', 'dashed', 'dotted')之一，转化为对象就是
    SingleChartsOption("line_type","radio",enable_option_values=__line_types ,option_default_value="solid",option_other_name="线条类型"),
    """
    def __init__(self,option_name,option_type,enable_option_values=None,option_default_value=None,option_other_name=""):
        """
        @option_name:  参数名称
        @option_type: 参数类型
                                    有value,checks,radio,range对应前端html的input
                    value对应text，radio对应radio,  checks对应checkbox，range会生成两个input并利用js拼接
        @enable_option_values: 可选值
        @option_default_value: 默认值
        @option_other_name: 别名
        """
        self.name=option_name
        self.type=option_type
        self.enable_values=enable_option_values
        self.default_value=option_default_value
        self.other_name=option_other_name
    
    def keys(self):
        return ('name', 'type', 'enable_values',"default_value","other_name")
    def __getitem__(self, item):
        return getattr(self, item)        

        
class ChartsOptionsBuild:
    """
    $构造出所有参数，并进行分组
    @允许选项
    @基础样式参数配置组
    @图表对应参数配置组
    """
    # 允许选项
    __pie_rosetype=("aera","radius")
    __grid3d_shading=("color","lambert","realistic")
    __point_symbols=("pin", "rect" , "roundRect" ,"diamond", "arrow" ,"triangle")
    __geo_effect_symbols=('circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'plane' )
    __funnel_sorts=('ascending','descending','none')
    __wordcloud_shapes=('circle', 'cardioid', 'diamond', 'triangle-forward', 'triangle', 'pentagon', 'star')
    __geo_types=('scatter', 'effectscatter', 'heatmap')
    __bool_values=(True,False)
    __mark_types=("average","max", "min")
    __radar_shapes=("polygon","circle")
    __effectdraw_types=('stroke', 'fill')
    __orient_types=('horizontal', 'vertical')
    __legend_selectedmodes=('single' , 'multiple' ,'false')
    __axisname_pos=('start','middle','end')
    __xaxis_pos=('top','bottom')
    __yaxis_pos=('left','right')
    __line_types=('solid', 'dashed', 'dotted')
    __label_pos=('top', 'left', 'right', 'bottom', 'inside','outside')
    __visual_types=('color', 'size')
    
    # legend样式参数配置组
    __legend_options=(
        SingleChartsOption("is_legend_show","radio",enable_option_values=__bool_values,option_default_value=True,option_other_name="是否显示图例"),
        SingleChartsOption("legend_top","value",option_default_value="top" ,option_other_name="标注水平位置"),
        SingleChartsOption("legend_pos","value",option_default_value="left" ,option_other_name="标注竖直位置"),
        SingleChartsOption("legend_text_size","value",option_default_value=15 ,option_other_name="标注字体大小"),
        SingleChartsOption("legend_text_color","value",option_default_value="#fff" ,option_other_name="标注字体颜色"),
        SingleChartsOption("legend_orient","radio",enable_option_values=__orient_types,option_default_value='horizontal',option_other_name="标注显示方式"),
        SingleChartsOption("legend_selectedmode","radio",enable_option_values=__legend_selectedmodes,option_default_value="multiple",option_other_name="标注选择方式"),
                    ) 
    # xy轴样式参数配置组
    __xyaxis_options= (
        SingleChartsOption("is_convert","radio",enable_option_values=__bool_values,option_default_value=False,option_other_name="横向坐标系"),
        SingleChartsOption("is_splitline_show ","radio",enable_option_values=__bool_values,option_default_value=False,option_other_name="显示网格线"),
        
        SingleChartsOption("is_xaxislabel_align","radio",enable_option_values=__bool_values,option_default_value=False,option_other_name="x 轴标签对齐"),
        SingleChartsOption("is_xaxis_inverse","radio",enable_option_values=__bool_values,option_default_value=False,option_other_name="反向 x轴"),
        SingleChartsOption("is_xaxis_show","radio",enable_option_values=__bool_values,option_default_value=False,option_other_name="显示x轴"),
        SingleChartsOption("xaxis_name","value",option_default_value="",option_other_name="x轴名称"),
        SingleChartsOption("xaxis_name_size","value",option_default_value=16,option_other_name="x轴名称大小"),
        SingleChartsOption("xaxis_name_gap","value",option_default_value=25,option_other_name="x轴名称与轴线距离"),
        SingleChartsOption("xaxis_name_pos","radio",enable_option_values=__axisname_pos ,option_default_value="end",option_other_name="x轴名称定位"),
        SingleChartsOption("xaxis_pos","radio",enable_option_values=__xaxis_pos ,option_default_value="bottom",option_other_name="x轴定位"),
        SingleChartsOption("xaxis_margin","value",option_default_value=8,option_other_name="x轴标签与轴线距离"),
        SingleChartsOption("xaxis_rotate","value",option_default_value=0,option_other_name="x轴标签角度"),
        SingleChartsOption("xaxis_line_color","value",option_default_value="",option_other_name="x轴线颜色"),
        SingleChartsOption("xaxis_line_width","value",option_default_value=1,option_other_name="x轴线宽"),
        
        SingleChartsOption("is_yaxislabel_align","radio",enable_option_values=__bool_values,option_default_value=False,option_other_name="y轴标签对齐"),
        SingleChartsOption("is_yaxis_inverse","radio",enable_option_values=__bool_values,option_default_value=False,option_other_name="反向 y轴"),
        SingleChartsOption("is_yaxis_show","radio",enable_option_values=__bool_values,option_default_value=False,option_other_name="显示y轴"),
        SingleChartsOption("yaxis_name","value",option_default_value="",option_other_name="y轴名称"),
        SingleChartsOption("yaxis_name_size","value",option_default_value=16,option_other_name="y轴名称大小"),
        SingleChartsOption("yaxis_name_gap","value",option_default_value=25,option_other_name="y轴名称与轴线距离"),
        SingleChartsOption("yaxis_name_pos","radio",enable_option_values=__axisname_pos ,option_default_value="end",option_other_name="y轴名称定位"),
        SingleChartsOption("yaxis_pos","radio",enable_option_values=__yaxis_pos ,option_default_value="right",option_other_name="y轴定位"),
        SingleChartsOption("yaxis_margin","value",option_default_value=8,option_other_name="y轴标签与轴线距离"),
        SingleChartsOption("yaxis_rotate","value",option_default_value=0,option_other_name="y轴标签角度"),
        SingleChartsOption("yaxis_line_color","value",option_default_value="",option_other_name="y轴线颜色"),
        SingleChartsOption("yaxis_line_width","value",option_default_value=1,option_other_name="y轴线宽"),
                       )
    # 线条样式参数配置组
    __linestyle_options=(
        SingleChartsOption("line_curve","value",option_default_value=0.0,option_other_name="曲度"),
        SingleChartsOption("line_width","value",option_default_value=1,option_other_name="线粗"),
        SingleChartsOption("line_opacity","value",option_default_value=1.0,option_other_name="线透明度"),
        SingleChartsOption("line_type","radio",enable_option_values=__line_types ,option_default_value="solid",option_other_name="线条类型"),
                   )
    # 3d样式参数配置组
    __grid3d_options=(
        SingleChartsOption("grid3d_opacity","value",option_default_value=0.0,option_other_name="3d透明度"),
        SingleChartsOption("grid3d_width","value",option_default_value=100,option_other_name="宽度"),
        SingleChartsOption("grid3d_depth","value",option_default_value=100,option_other_name="深度"),
        SingleChartsOption("grid3d_height","value",option_default_value=100,option_other_name="高度"),
        SingleChartsOption("grid3d_rotate_speed","value",option_default_value=10,option_other_name="自转速度"),
        SingleChartsOption("grid3d_rotate_sensitivity","value",option_default_value=1,option_other_name="操作灵敏度"),
        SingleChartsOption("grid3d_shading","radio",enable_option_values=__grid3d_shading, option_default_value="realistic",option_other_name="阴影效果"),
        SingleChartsOption("is_grid3d_rotate","radio",enable_option_values=__bool_values, option_default_value=False,option_other_name="自转模式"),
        
        SingleChartsOption("yaxis3d_name","value",option_default_value="",option_other_name="y轴名称"),
        SingleChartsOption("yaxis3d_name_size","value",option_default_value=16,option_other_name="y轴名称大小"),
        SingleChartsOption("yaxis3d_name_gap","value",option_default_value=25,option_other_name="y轴名称与轴线距离"),
        SingleChartsOption("yaxis3d_margin","value",option_default_value=8,option_other_name="y轴标签与轴线距离"),
        SingleChartsOption("xaxis3d_name","value",option_default_value="",option_other_name="x轴名称"),
        SingleChartsOption("xaxis3d_name_size","value",option_default_value=16,option_other_name="x轴名称大小"),
        SingleChartsOption("xaxis3d_name_gap","value",option_default_value=25,option_other_name="x轴名称与轴线距离"),
        SingleChartsOption("xaxis3d_margin","value",option_default_value=8,option_other_name="x轴标签与轴线距离"),
        SingleChartsOption("zaxis3d_name","value",option_default_value="",option_other_name="z轴名称"),
        SingleChartsOption("zaxis3d_name_size","value",option_default_value=16,option_other_name="z轴名称大小"),
        SingleChartsOption("zaxis3d_name_gap","value",option_default_value=25,option_other_name="z轴名称与轴线距离"),
        SingleChartsOption("zaxis3d_margin","value",option_default_value=8,option_other_name="z轴标签与轴线距离"),
       )
    # 标签样式参数配置组
    __label_options=(
        SingleChartsOption("is_random","radio",enable_option_values=__bool_values,option_default_value=False,option_other_name="随机排列颜色"),
        SingleChartsOption("is_label_show","radio",enable_option_values=__bool_values,option_default_value=False,option_other_name="平时显示所有标签"),
        SingleChartsOption("is_label_emphasis","radio",enable_option_values=__bool_values,option_default_value=True,option_other_name="选中数据时高亮显示选中标签"),
        SingleChartsOption("label_pos","radio",enable_option_values=__label_pos,option_default_value="top",option_other_name="平时标签定位"),
        SingleChartsOption("label_emphasis_pos","radio",enable_option_values=__label_pos,option_default_value="top",option_other_name="选中标签定位"),
        
        SingleChartsOption("label_text_color","value",option_default_value= "#000" ,option_other_name="平时标签颜色"),
        SingleChartsOption("label_emphasis_textcolor","value",option_default_value= "#fff" ,option_other_name="选中标签颜色"),
        SingleChartsOption("label_text_size","value",option_default_value=12 ,option_other_name="平时标签大小"),
        SingleChartsOption("label_emphasis_textsize","value",option_default_value=12 ,option_other_name="选中标签大小"),
        )
    # 映射样式参数配置组
    __visualmap_options=(
        SingleChartsOption("is_visualmap","radio",enable_option_values=__bool_values,option_default_value=False,option_other_name="启用映射组件"),
        SingleChartsOption("visual_dimension","radio" ,enable_option_values=(None,0,1,2),option_default_value=None,option_other_name="映射维度"),
        SingleChartsOption("visual_type","radio",enable_option_values=__visual_types,option_default_value="color",option_other_name="映射方式"),
        SingleChartsOption("visual_range","range",option_default_value=[0,100],option_other_name="数据显示范围"),
        SingleChartsOption("visual_range_text","range",option_default_value=['low', 'hight'],option_other_name="映射两端标签"),
        SingleChartsOption("visual_range_color","range",option_default_value= ['#50a3ba', '#eac763', '#d94e5d'],option_other_name="过渡颜色"),
        SingleChartsOption("visual_range_size","range",option_default_value=[20,50],option_other_name="size映射时的圆点直径范围"),
        SingleChartsOption("visual_orient","radio",enable_option_values=__orient_types,option_default_value="vertical",option_other_name="组件方向"),
        SingleChartsOption("visual_pos","value" ,option_default_value="left",option_other_name="组件水平定位"),
        SingleChartsOption("visual_top","value" ,option_default_value="top",option_other_name="组件垂直定位"),
        SingleChartsOption("is_piecewise","radio" ,enable_option_values=__bool_values,option_default_value=False,option_other_name="分段式组件"),
        SingleChartsOption("visual_split_number","value" ,option_default_value=5,option_other_name="分段数量")
        )

    def __tran_dicts(self,options_list):
        """
        将某个配置组转化成字典，方便json异步传输给前端
        """
        dict_list=[ dict(i)  for i in options_list ] 
        return dict_list
    
    #图表对应参数配置组
    def __add_bar_options(self):
        options=[]
        options.append(SingleChartsOption("is_stack","radio",enable_option_values=self.__bool_values,option_default_value=False ,option_other_name="堆叠"))
        options.append(SingleChartsOption("mark_line","checks",enable_option_values=self.__mark_types,option_default_value="average"  ,option_other_name="标记线"))
        options.append(SingleChartsOption("bar_category_gap","value",option_default_value="20%" ,option_other_name="柱状间隔"))
        options.append(SingleChartsOption("mark_point","checks",enable_option_values=self.__mark_types,option_default_value="average",option_other_name="标记点"))
        #options.extend(self.__xyaxis_options)
        ##options.extend(self.__legend_options)
        return options
    
    def __add_line_options(self):
        options=[]
        options.append(SingleChartsOption("is_symbol_show","radio",enable_option_values=self.__bool_values,option_default_value=True,option_other_name="显示标记"))
        options.append(SingleChartsOption("symbol_size","value",option_default_value=4,option_other_name="标记尺寸"))
        options.append(SingleChartsOption("is_smooth","radio",enable_option_values=self.__bool_values,option_default_value=False,option_other_name="曲线"))
#         options.append(SingleChartsOption("is_stack","radio",enable_option_values=self.__bool_values,option_default_value=False,option_other_name="堆叠"))
        options.append(SingleChartsOption("is_step","radio",enable_option_values=self.__bool_values,option_default_value=False,option_other_name="阶梯"))
        options.append(SingleChartsOption("area_opacity","value",option_default_value=0.0,option_other_name="区域透明度"))
        #options.extend(self.__xyaxis_options)
        #options.extend(self.__linestyle_options)
        #options.extend(self.__legend_options)
        return options
    
    def __add_funnel_options(self):
        options=[]
        options.append(SingleChartsOption("funnel_sort","radio",enable_option_values=self.__funnel_sorts,option_default_value="ascending",option_other_name="排序"))
        options.append(SingleChartsOption("funnel_gap","value",option_default_value=1,option_other_name="图形间距"))
        options.append(SingleChartsOption("funnel_width","value",option_default_value="90%",option_other_name="图像宽度"))
        options.append(SingleChartsOption("funnel_x","value",option_default_value="0%",option_other_name="水平定位"))
        #options.extend(self.__label_options)
        #options.extend(self.__legend_options)
        return options
    def __add_wordcloud_options(self):
        options=[]
        options.append(SingleChartsOption("shape","radio",enable_option_values=self.__wordcloud_shapes,option_default_value="circle",option_other_name="形状"))
        options.append(SingleChartsOption("word_gap","value",option_default_value="20",option_other_name="单词间隔"))
        options.append(SingleChartsOption("rotate_step","value",option_default_value="45",option_other_name="单词旋角"))
        options.append(SingleChartsOption("word_size_range","range",option_default_value=[12, 60],option_other_name="单词大小范围"))
        return options
    def __add_geo_options(self):
        options=[]
        options.append(SingleChartsOption("maptype","value",option_default_value="china",option_other_name="地图区域"))
        options.append(SingleChartsOption("type","radio",enable_option_values=self.__geo_types,option_default_value="heatmap",option_other_name="图例类型"))
        options.append(SingleChartsOption("symbol_size","value",option_default_value=4,option_other_name="标记尺寸"))
        options.append(SingleChartsOption("border_color","value",option_default_value="#111",option_other_name="边界颜色"))
        options.append(SingleChartsOption("geo_normal_color","value",option_default_value="#323c48",option_other_name="正常区域颜色"))
        options.append(SingleChartsOption("geo_emphasis_color","value",option_default_value="#2a333d",option_other_name="高亮区域颜色"))
        
        return options
    def __add_geolines_options(self):
        options=[]
        options.append(SingleChartsOption("maptype","value",option_default_value="china",option_other_name="地图区域"))
        options.append(SingleChartsOption("type","radio",enable_option_values=self.__geo_types,option_default_value="scatter",option_other_name="图例类型"))
        options.append(SingleChartsOption("symbol","radio",enable_option_values=self.__point_symbols,option_default_value="rect",option_other_name="标记形状"))
        options.append(SingleChartsOption("symbol_size","value",option_default_value=1,option_other_name="标记尺寸"))
        options.append(SingleChartsOption("border_color","value",option_default_value="#111",option_other_name="边界颜色"))
        options.append(SingleChartsOption("geo_normal_color","value",option_default_value="#323c48",option_other_name="正常区域颜色"))
        options.append(SingleChartsOption("geo_emphasis_color","value",option_default_value="#2a333d",option_other_name="高亮区域颜色"))
        options.append(SingleChartsOption("geo_effect_period","value",option_default_value="10",option_other_name="特效动画的时间"))
        options.append(SingleChartsOption("geo_effect_traillength","value",option_default_value=0.5,option_other_name="特效尾迹长度"))
        options.append(SingleChartsOption("geo_effect_color","value",option_default_value="#fff",option_other_name="特效标记的颜色"))
        options.append(SingleChartsOption("geo_effect_symbol","radio",enable_option_values=self.__geo_effect_symbols,option_default_value="plane",option_other_name="特效图形"))
        options.append(SingleChartsOption("geo_effect_symbolsize","value",option_default_value=5,option_other_name="特效图形大小"))
        return options
    def __add_grid3d_options(self):
        options=[]
        #options.extend(self.__grid3d_options)
        #options.extend(self.__legend_options)
        return options
    
    def __add_scatter_options(self):
        options=[]
        options.append(SingleChartsOption("symbol","radio",enable_option_values=self.__point_symbols,option_default_value="rect",option_other_name="标记形状"))
        options.append(SingleChartsOption("symbol_size","value",option_default_value=4,option_other_name="标记尺寸"))
        #options.extend(self.__xyaxis_options)
        #options.extend(self.__legend_options)
        options.extend(self.__visualmap_options)
        return options

    def __add_effectscatter_options(self):
        options=[]
        options.append(SingleChartsOption("symbol","radio",enable_option_values=self.__point_symbols,option_default_value="rect",option_other_name="标记形状"))
        options.append(SingleChartsOption("symbol_size","value",option_default_value=4,option_other_name="标记尺寸"))
        options.append(SingleChartsOption("effect_period","value",option_default_value=4,option_other_name="动画持续时间"))  
        options.append(SingleChartsOption("effect_scale","value",option_default_value=2.5,option_other_name="波纹缩放比例"))   
        options.append(SingleChartsOption("effect_brushtype","radio",enable_option_values=self.__effectdraw_types,option_default_value='stroke',option_other_name="波纹绘制方式")) 
        #options.extend(self.__xyaxis_options)
        #options.extend(self.__legend_options)
        return options

    def __add_pie_options(self):
        options=[]
        options.append(SingleChartsOption("radius","range",option_default_value=["0%", "70%"],option_other_name="半径范围"))
        options.append(SingleChartsOption("center","range",option_default_value=["50%", "50%"],option_other_name="圆心坐标")) 
        options.append(SingleChartsOption("rosetype","radio",enable_option_values=self.__pie_rosetype, option_default_value="radius",option_other_name="区域类型"))
        #options.extend(self.__legend_options)
        #options.extend(self.__label_options)
        return options
    def __add_radar_options(self):
        options=[]
        options.append(SingleChartsOption("shape","radio",enable_option_values=self.__radar_shapes, option_default_value="polygon",option_other_name="雷达形状"))  
        options.append(SingleChartsOption("radar_text_color","value",option_default_value="#000",option_other_name="字体颜色"))
        options.append(SingleChartsOption("radar_text_size","value",option_default_value=12,option_other_name="字体大小"))
        options.append(SingleChartsOption("area_opacity","value",option_default_value=0.0,option_other_name="区域透明度"))
        options.append(SingleChartsOption("is_splitline","radio",enable_option_values=self.__bool_values,option_default_value=True ,option_other_name="分割线"))
        options.append(SingleChartsOption("is_axisline_show","radio",enable_option_values=self.__bool_values,option_default_value=True,option_other_name="坐标线"))
        #options.extend(self.__legend_options)
        #options.extend(self.__label_options)
        #options.extend(self.__linestyle_options)
        return options
    def __add_calendarheatmap_options(self):
        options=[]
        options.append(SingleChartsOption("calendar_date_range","range",option_default_value=["2016-5-5", "2017-5-5"] ,option_other_name="日期范围"))
        options.append(SingleChartsOption("calendar_cell_size","range",option_default_value=["auto", 20],option_other_name="方格宽高")) 
        #options.extend(self.__legend_options)
        #options.extend(self.__visualmap_options)
        return options

    def  options_build(self,chartType):
        """
        @chartType 根据chartType导出合适的样式参数配置组
        """
        options=None
        if  chartType=="bar":
            options= self.__add_bar_options()

        elif chartType=="line":
            options= self.__add_line_options()

        elif chartType=="funnel":
            options= self.__add_funnel_options()
        elif chartType=="wordcloud":
            options= self.__add_wordcloud_options()
        elif chartType=="geo":
            options= self.__add_geo_options()
        elif chartType=="geolines":
            options= self.__add_geolines_options()
        elif chartType=="pie":
            options= self.__add_pie_options()
        elif chartType =="scatter":
            options= self.__add_scatter_options()
        elif chartType=="effectscatter":
            options=self.__add_effectscatter_options()
        elif chartType in ["bar3d" ,"line3d","surface3d","scatter3d"] :
            options= self.__add_grid3d_options()
        elif chartType=="calendarheatmap":
            options= self.__add_calendarheatmap_options()
        elif chartType=="radar":
            options= self.__add_radar_options()
        else:
            options=[]
        return self.__tran_dicts(options)

commonChartsOptionsbuilder=ChartsOptionsBuild()

def getChartOptions(charttype):
    global commonChartsOptionsbuilder
    return commonChartsOptionsbuilder.options_build(charttype)




#s不同图表的数据格式，xyz或者attr和value
class DataFormater:
    """
    $ 数据格式类
    @oldclientdataformmat: 数据格式字典
    @dataformatFunction: 解析函数
    """
    def __init__(self,oldclientdataformmat,dataformatFunction):
        #字典{name 组名  attr属性 value 值}
        self.clientdatadict=oldclientdataformmat
        self.dataformatFunction=dataformatFunction
    
    def dataformattranst(self,clientdatadict):
        return self.dataformatFunction(clientdatadict)
    

# 各种图表的解析函数
def Nodataformattranst(clientdatadict):
    return clientdatadict

def axis3Ddataformattranst(clientdatadict):
    return {'name':clientdatadict.get("name",""),"data":list(zip(clientdatadict["x"],clientdatadict["y"],clientdatadict["z"])) }

def scatter3Ddataformattranst(clientdatadict):
    xyzdata=[clientdatadict["x"],clientdatadict["y"],clientdatadict["z"]]
    if "extra_color" in clientdatadict:
        xyzdata.append(clientdatadict["extra_color"])
    if "extra_size" in clientdatadict:
        xyzdata.append(clientdatadict["extra_size"]) 
    resdata=list(zip(*xyzdata)) 
    print(resdata)
    return {'name':clientdatadict.get("name",""),"data":resdata}

def calendardataformattranst(clientdatadict):
    clientdatadict["date"]=[i.replace("/","-") for i in clientdatadict["date"] ]
    return (clientdatadict.get("name",""),list(zip(clientdatadict["date"],clientdatadict["value"])) )
def geolinesdataformattranst(clientdatadict):
    if clientdatadict.get("value",None) is not None:
        return {'name':clientdatadict.get("name",""),"data":list(zip(clientdatadict["from"],clientdatadict["to"],clientdatadict["value"])) }
    else:
        return {'name':clientdatadict.get("name",""),"data":list(zip(clientdatadict["from"],clientdatadict["to"])) }

def bar3ddataformattranst(clientdatadict):
    if isinstance(clientdatadict["x"][0],int):
        index_x=clientdatadict["x"]
    else:
        index_x=[ clientdatadict["x_axis"].index(i) for i in clientdatadict["x"]]
    if isinstance(clientdatadict["y"][0],int):
        index_y=clientdatadict["y"]
    else:
        index_y=[ clientdatadict["y_axis"].index(i) for i in clientdatadict["y"]]
    return {'name':clientdatadict.get("name",""),
            'x_axis':clientdatadict["x_axis"],
            'y_axis':clientdatadict["y_axis"],
            "data":list(zip(index_x,index_y,clientdatadict["value"])) 
            }
def heatmapdataformattranst(clientdatadict):
    if isinstance(clientdatadict["x"][0],int):
        index_x=clientdatadict["x"]
    else:
        index_x=[ clientdatadict["x_axis"].index(i) for i in clientdatadict["x"]]
    if isinstance(clientdatadict["y"][0],int):
        index_y=clientdatadict["y"]
    else:
        index_y=[ clientdatadict["y_axis"].index(i) for i in clientdatadict["y"]]
    return (clientdatadict.get("name",""),
            clientdatadict["x_axis"],
            clientdatadict["y_axis"],
            list(zip(index_x,index_y,clientdatadict["value"])) 
            )
    
def klinedataformattranst(clientdatadict):
    return {'name':clientdatadict.get("name",""),
            'x_axis':clientdatadict["x_axis"],
            "y_axis":list(zip(clientdatadict["open"],clientdatadict["close"],clientdatadict["lowest"],clientdatadict["highest"])) }
def radardataformattranst(clientdatadict):
    return {'name':clientdatadict.get("name",""),
            'value':[clientdatadict["value"]],
            "schema":list(zip(clientdatadict["attr"],clientdatadict["max"])) }

# 根据各个图表所需的数据项，构成DataFormater 
funnel_geo_pie_wordcould_dataformat=DataFormater({'name':'组名','attr':'项目名','value':'项目值'},Nodataformattranst)
line_bar_es_dataformat=DataFormater({'name':'组名','x_axis':'横坐标','y_axis':'纵坐标/值'},Nodataformattranst)
scatterdataformat=DataFormater({'name':'组名','x_axis':'横坐标','y_axis':'纵坐标/值','extra_data':'点的权值','extra_name':'点的别名'},Nodataformattranst)
geolinesdataformat=DataFormater({'name':'组名','from':'出发城市','to':'目标城市','value':'路线权值'},geolinesdataformattranst)
calendarsdataformat=DataFormater({'name':'组名','date':'日期','value':'值'},calendardataformattranst)
grid3d_dataformat=DataFormater({'name':'组名','x':'x坐标','y':'y坐标','z':'z坐标'},axis3Ddataformattranst)
scatter3d_dataformat=DataFormater({'name':'组名','x':'x坐标','y':'y坐标','z':'z坐标','extra_color':'点的颜色','extra_size':'点的大小'},scatter3Ddataformattranst)
bar3ddataformat=DataFormater({'name':'组名','x_axis':'横轴','y_axis':'纵轴','x':'横坐标','y':'纵坐标','value':'值'},bar3ddataformattranst)
heatmapdataformat=DataFormater({'name':'组名','x_axis':'横轴','y_axis':'纵轴','x':'横坐标','y':'纵坐标','value':'值'},heatmapdataformattranst)
klinedataformat=DataFormater({'name':'组名','x_axis':'横轴','open':'开盘价','close':'收盘价','highest':'高位价','lowest':'低位价'},klinedataformattranst)
radardataformat=DataFormater({'name':'组名','attr':'项目名','max':'项目上限','value':'值'},radardataformattranst)
Dataformats={
            'bar': line_bar_es_dataformat,
            'line': line_bar_es_dataformat,
            'pie': funnel_geo_pie_wordcould_dataformat,
            'funnel':funnel_geo_pie_wordcould_dataformat,
            'wordcloud':funnel_geo_pie_wordcould_dataformat,
            'scatter':scatterdataformat,
            'effectscatter':line_bar_es_dataformat,
            'heatmap':heatmapdataformat,
            "geo":funnel_geo_pie_wordcould_dataformat,
            'geolines':geolinesdataformat,
            'bar3d':bar3ddataformat,
            'line3d':grid3d_dataformat,
            'scatter3d':scatter3d_dataformat,
            'kline':klinedataformat,
            'radar':radardataformat,
            'calendarheatmap':calendarsdataformat,
            'surface3d':grid3d_dataformat
    }
