#  -*- coding:utf-8 -*-
'''
Created on 2019年7月15日

@author: 魔天一念
默认样式参数
'''

baseparams=dict(
    is_toolbox_show=True,
    is_more_utils=False,
    is_legend_show=True,#显示图例
    is_label_show=False,#显示标注
    label_pos='inside',
            )

bar_params={**baseparams,
    "datazoom_type":'slider',
    "is_datazoom_show":False,
    "is_more_utils":True,
    }
line_params={**baseparams,
    "datazoom_type":'slider',#"slider",
    "is_datazoom_show":False,
    "is_more_utils":True,
    }
funnel_params={**baseparams,
    "is_label_show":True,#显示标注
    "label_pos":'inside'
    }
wordcloud_params={**baseparams,
    # "shape":'diamond',#'circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow'
    # "word_gap":30
    }
scatter_params={**baseparams,
    "is_visualmap":True,
    "visual_dimension":2,
    "visual_type":"size",#'size',
    }
effectscatter_params={**baseparams,
    "symbol_size":20, 
    "effect_scale":3.5,  
    "effect_period":3, 
    }
pie_params={**baseparams,
    "is_legend_show":True,#显示图例
    "is_label_show":False,#显示标注
    "label_pos":'inside',
    }
heatmap_params={**baseparams,
    "is_visualmap":True,
    "visual_dimension":1,
    "visual_orient":'horizontal',
    "visual_text_color":"#000"
    }
calendarheatmap_params={
    **heatmap_params,
    "is_calendar_heatmap":True
                        }

geo_params={**baseparams,
    "symbol_size" :1,
    "is_visualmap":True,#热点可见
    "type":'heatmap',#热图模式
    "is_datazoom_show":False
                }
geolines_params={**baseparams,
    "geo_effect_symbol":"plane",
    "geo_effect_symbolsize":10,
    "tooltip_formatter":"{a} : {c}",
    "line_curve":0.2,
    "line_opacity":0.6,
    "legend_text_color":"#eee",
    "legend_pos":"right",
                }
bar3d_params={**baseparams,
        "is_visualmap":True,
        "grid3d_rotate_sensitivity":1,
        "is_grid3d_rotate":True,
        "visual_type":"color",
              }
scatter3d_params=line3d_params=surface3d_params={**baseparams,
        "is_visualmap":True,
        "visual_range_color":['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf','#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026'],
        "is_grid3D_rotate":True, 
        "grid3D_rotate_speed":1,
        "visual_type":"color"
               }
kline_params={**baseparams,
              
              }
radar_params={**baseparams,
    }


