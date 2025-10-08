import xml.etree.ElementTree as ET
import random

# 定义可用的边
available_edges = [1746, 1742, 3882, 1744, 1743, 1824]

# 创建路由文件的根元素
routes = ET.Element('routes')

# 定义车辆类型
vType = ET.SubElement(routes, 'vType', id='car', accel='2.6', decel='4.5', sigma='0.5', length='5', maxSpeed='70')

# 随机生成 100 辆车的行程
for i in range(100):
    # 随机选择起始边
    start_edge = random.choice(available_edges)
    # 随机选择目标边，确保和起始边不同
    end_edge = start_edge
    while end_edge == start_edge:
        end_edge = random.choice(available_edges)

    # 随机选择经过的边
    via_edges = random.sample([edge for edge in available_edges if edge not in [start_edge, end_edge]],
                              random.randint(0, len(available_edges) - 2))
    via_edges_str = " ".join(map(str, via_edges))

    # 随机生成出发时间（0 到 100 秒之间）
    depart_time = random.randint(0, 100)
    # 随机生成出发速度（10 到 30 之间）
    depart_speed = random.randint(10, 30)

    # 创建 trip 元素
    trip = ET.SubElement(routes, 'trip',
                         id=f'trip_{i}',
                         depart=str(depart_time),
                         from_=str(start_edge),
                         to=str(end_edge),
                         departSpeed=str(depart_speed),
                         via=via_edges_str)

# 创建 XML 树并写入文件
tree = ET.ElementTree(routes)
tree.write('routes_with_100_trips.xml', encoding='utf-8', xml_declaration=True)
