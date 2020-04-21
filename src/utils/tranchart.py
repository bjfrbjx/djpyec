#  -*- coding:utf-8 -*-
'''
Created on 2019年7月21日

@author: 魔天一念
'''
from pyecharts import Bar,Line,Pie,Funnel , WordCloud,Scatter,EffectScatter,HeatMap,Geo,GeoLines,Kline,Bar3D,Line3D,Scatter3D,Surface3D,Radar
from pyecharts import Page,Overlap,Grid,Timeline
from .echartsparams import bar_params,effectscatter_params,funnel_params,line_params,wordcloud_params,pie_params,scatter_params,calendarheatmap_params
from .echartsparams import geolines_params,heatmap_params,geo_params,bar3d_params,line3d_params,scatter3d_params,kline_params,radar_params,surface3d_params
'''
支持的组图种类
'''
custom_chart={
    "page":Page,
    "overlap":Overlap,
    "grid":Grid,
    "timeline":Timeline
    }

'''
支持的单图种类
'''
chartdict={
            'bar': Bar,
            'line': Line,
            'pie': Pie,
            'funnel':Funnel,
            'wordcloud':WordCloud,
            'scatter':Scatter,
            'effectscatter':EffectScatter,
            'heatmap':HeatMap,
            'geo':Geo,
            'geolines':GeoLines,
            'bar3d':Bar3D,
            'line3d':Line3D,
            'scatter3d':Scatter3D,
            'kline':Kline,
            'radar':Radar,
            'surface3d':Surface3D,
            'calendarheatmap':HeatMap
    }
'''
支持的单图种类-中文名称
'''
chartNamedict=(
            '柱状图',
            '折线图',
            '饼图',
            '漏斗图',
            '词云图',
            '散点图',
            '动态散点图',
            '热力图',
            '地理图',
            '地理连线图',
            '3d柱状图',
            '3d折线图',
            '3d散点图',
            'k线图',
            '雷达图',
            '曲面图',
            '日历图'
    )
'''
支持的单图种类到默认样式参数映射
'''
paramsdict={
            'bar': bar_params,
            'line': line_params,
            'pie': pie_params,
            'funnel':funnel_params,
            'wordcloud':wordcloud_params,
            'scatter':scatter_params,
            'effectscatter':effectscatter_params,
            'heatmap':heatmap_params,
            "geo":geo_params,
            'geolines':geolines_params,
            'bar3d':bar3d_params,
            'line3d':line3d_params,
            'scatter3d':scatter3d_params,
            'kline':kline_params,
            'radar':radar_params,
            'calendarheatmap':calendarheatmap_params,
            'surface3d':surface3d_params
    }


def getSupporttype():
    return list(zip(tuple(chartdict.keys()),chartNamedict))