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

from pyecharts import Surface3D


def create_surface3d_data():
    for t0 in range(-60, 60, 1):
        y = t0 / 60
        for t1 in range(-60, 60, 1):
            x = t1 / 60
            if math.fabs(x) < 0.1 and math.fabs(y) < 0.1:
                z = '-'
            else:
                z = math.sin(x * math.pi) * math.sin(y * math.pi)
            yield [x, y, z]

range_color = [
    "#313695",
    "#4575b4",
    "#74add1",
    "#abd9e9",
    "#e0f3f8",
    "#ffffbf",
    "#fee090",
    "#fdae61",
    "#f46d43",
    "#d73027",
    "#a50026",
]

_data = list(create_surface3d_data())
surface3d = Surface3D("3D 曲面图示例", width=1200, height=600)
surface3d.add(
    "",
    _data,
    is_visualmap=True,
    visual_range_color=range_color,
    visual_range=[-3, 3],
    grid3d_rotate_sensitivity=5,
)
surface3d.render(path="/home/hxy/桌面/surface3d.html")