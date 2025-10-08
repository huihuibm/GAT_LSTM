import xml.etree.ElementTree as ET

# 解析XML文件
tree = ET.parse('../cd_road_sumo/config/modified_xml_file1.xml')
root = tree.getroot()

# 替换为你希望处理的边的标识符
edges_to_consider = ['-3296', '3369', '3368', '6307', '3360', '3692', '3282', '2458', '2486', '2459', '-2486', '-2459',
                     '3359', '-2458', '-3359', '3360', '2487', '2480', '-2487', '-2480', '2460', '2461', '-2460',
                     '-2461', '2481', '2464', '-2481', '-2464', '3363']
trip_ids = []
n = 0

# 收集需要保留的 trip_id
for trip_elem in root.findall('trip'):
    from_attr = trip_elem.get('from')
    to_attr = trip_elem.get('to')
    via_attr = trip_elem.get('via')

    if from_attr in edges_to_consider or to_attr in edges_to_consider:
        trip_ids.append(trip_elem.get('id'))
        n += 1
    elif via_attr:
        via_edges = via_attr.split()
        if any(edge in edges_to_consider for edge in via_edges):
            trip_ids.append(trip_elem.get('id'))
            n += 1

# 创建一个新的根元素来存储符合条件的 trip 信息
new_root = ET.Element(root.tag)

# 将符合条件的 trip 元素复制到新的 XML 结构中
for trip_elem in root.findall('trip'):
    if trip_elem.get('id') in trip_ids:
        new_root.append(trip_elem)

# 创建一个新的 XML 文件来存储新的根元素
new_tree = ET.ElementTree(new_root)
new_tree.write('filtered_xml_file_1111.xml', encoding='utf-8')

print(f"经过指定边的 trip id：{trip_ids}")
print(f"符合条件的 trip 数量：{n}")
