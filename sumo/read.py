import csv
import xml.etree.ElementTree as ET

csv_file = '../cd_road_sumo/1.csv'
xml_file = '../cd_road_sumo/config/cd_routes_real.rou6-4-2.xml'
output_file = '../cd_road_sumo/updated_data.xml'

try:
    # 从CSV文件中读取第一列数据
    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        csv_data = [row[0] for row in csv_reader if row]

    # 解析XML文件
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # 记录删除的trip节点数
    deleted_trip_count = 0

    # 遍历XML文件中的所有trip节点
    for trip in root.findall('trip'):
        trip_id = trip.get('id')
        # 如果trip_id在CSV数据中存在，则删除该trip节点
        if trip_id in csv_data:
            root.remove(trip)
            deleted_trip_count += 1

    # 保存更新后的XML文件
    tree.write(output_file)

    print(f"Successfully removed {deleted_trip_count} trip nodes from the XML file.")
    print(f"Updated XML file saved as {output_file}")

except FileNotFoundError:
    print("File not found. Please check if the CSV and XML files exist.")
except Exception as e:
    print(f"An error occurred: {e}")
