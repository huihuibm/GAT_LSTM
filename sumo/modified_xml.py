import xml.etree.ElementTree as ET
'''
移除不存在的节点
'''
# 加载 XML 文件
tree = ET.parse("../cd_road_sumo/config/modified_routes11.xml")
root = tree.getroot()
edge_id=['2460','2461','-2460','-2461']
# 遍历每个 <trip> 元素
for trip in root.findall('trip'):
    # 获取 from、to 和 via 属性的值
    from_value = trip.get('from')
    to_value = trip.get('to')
    via_value = trip.get('via')

    # 检查是否需要删除该条 trip
    if from_value in edge_id or to_value in edge_id:
        root.remove(trip)
    else:
        # 检查 via 属性中是否包含 edge_id，如果包含，则删除该值
        if via_value is not None:
            via_list = via_value.split()
            via_list = [item for item in via_list if item not in edge_id]
            trip.set('via', ' '.join(via_list))

# 保存修改后的 XML 文件
tree.write("modified_routes11-5.xml")
