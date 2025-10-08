import xml.etree.ElementTree as ET

# 解析XML文件
tree = ET.parse('../cd_road_sumo/config/tripinfo_4.xml')
root = tree.getroot()

# 用于存储所有waitingTime的值
waiting_times = []

# 查找所有的tripinfo元素
tripinfo_elements = root.findall('tripinfo')

# 遍历每个tripinfo元素并获取waitingTime的值，添加到列表中
for tripinfo in tripinfo_elements:
    waiting_time = float(tripinfo.get('waitingTime'))
    waiting_times.append(waiting_time)

# 计算平均值
if waiting_times:
    average_waiting_time = sum(waiting_times) / len(waiting_times)
    print(average_waiting_time)