import random
from pyecharts.conf import configure
from pyecharts.charts.scatter import Scatter
from pyecharts.charts.scatter3D import Scatter3D
from pyecharts.charts.line3D import Line3D
print("-success-")
# from pyecharts.conf import configure
# configure(jshost="http://127.0.0.1:8080/static/JS/",force_js_embed=False)
# from pyecharts import Geo as Map
# districts = ['运河区', '新华区', '泊头市', '任丘市', '黄骅市', '河间市', '沧县', '青县', '东光县', '海兴县', '盐山县', '肃宁县', '南皮县', '吴桥县', '献县', '孟村回族自治县']
# areas = [109.92, 109.47, 1006.5, 1023.0, 1544.7, 1333.0, 1104.0, 968.0, 730.0, 915.1, 796.0, 525.0, 794.0, 600.0, 1191.0, 387.0]
# map_1 = Map("沧州市图例－各区面积", width=1200, height=600)
# map_1.add("", districts, areas, type="heatmap",maptype='沧州', is_visualmap=True, visual_range=[min(areas), max(areas)],
#         visual_text_color='#000', is_map_symbol_show=False, is_label_show=True)
# map_1.render(path="/home/hxy/桌面/map3.html")
# Create your tests here.

import math
# configure(jshost="127.0.0.1:8080/static/JS/",force_js_embed=False)
from pyecharts import Surface3D


def create_surface3d_data():
    return [[3,5,3,1],[5,3,7,2],[8,1,6,3]]
#     for t0 in range(-60, 60, 1):
#         y = t0 / 60
#         for t1 in range(-60, 60, 1):
#             x = t1 / 60
#             if math.fabs(x) < 0.1 and math.fabs(y) < 0.1:
#                 z = '-'
#             else:
#                 z = math.sin(x * math.pi) * math.sin(y * math.pi)
#             yield [x, y, z,random.random()]

range_color = ['#50a3ba', '#eac763', '#d94e5d']

if __name__=="__main__":
    _data = list(create_surface3d_data())
    print(len(_data),_data[:10])
    surface3d = Scatter3D("3D 曲面图示例", width=1200, height=600)
    # 指定visual_dimension就覆盖visual_range为维度的上下限
    surface3d.add(
        "",
        _data,
        is_visualmap=True,
        visual_dimension=1,
        visual_type="size",
        #visual_range_color=range_color,
        visual_range_size=[5,10],
        visual_range_text=['a','b'],
        #visual_range=[3, 5],
        grid3d_rotate_sensitivity=1,
    )
    surface3d.render(path="E:\桌面\Desktop\surface3d.html")