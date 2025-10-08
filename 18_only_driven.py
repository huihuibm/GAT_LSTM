import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely import wkt

# 读取节点数据
points_shapefile_path = "nodes.shp"
points_gdf = gpd.read_file(points_shapefile_path)

# 读取道路数据
edges_csv_path = "G_1_data.csv"
edges_df = pd.read_csv(edges_csv_path)
edges_df['geometry'] = edges_df['geometry'].apply(wkt.loads)
edges_gdf = gpd.GeoDataFrame(edges_df, geometry='geometry')

# 读取已驱动的道路数据
driven_roads_csv_path = "result_dataset.csv"
driven_roads_df = pd.read_csv(driven_roads_csv_path)

# 将道路数据中是否已驱动的信息添加到 GeoDataFrame 中
edges_gdf['driven'] = edges_gdf['road_id'].isin(driven_roads_df['road_id'])
driven_edges_gdf = edges_gdf[edges_gdf['driven']]

# 找到孤立的点
connected_nodes = set(driven_edges_gdf['u']).union(set(driven_edges_gdf['v']))
isolated_nodes = points_gdf[~points_gdf['osmid'].isin(connected_nodes)]

# 删除孤立的点
filtered_points_gdf = points_gdf[~points_gdf['osmid'].isin(isolated_nodes['osmid'])]

# 创建图形和轴对象
fig, ax = plt.subplots()

# 绘制筛选后的节点
filtered_points_gdf.plot(ax=ax, color='blue', markersize=5)

# 绘制驱动的道路
driven_edges_gdf.plot(ax=ax, color='red', linewidth=1)

# 设置图形标题
#plt.title('Driven Roads without Isolated Points')

# 显示图形
#plt.show()


import geopandas as gpd
from shapely.geometry import Point

# 输入的经纬度坐标
input_lon = 104.064910   # 替换为你的经度
input_lat = 30.661526# 替换为你的纬度
input_point = Point(input_lon, input_lat)

# 读取道路数据
edges_csv_path = "G_1_data.csv"
edges_df = pd.read_csv(edges_csv_path)
edges_df['geometry'] = edges_df['geometry'].apply(wkt.loads)
edges_gdf = gpd.GeoDataFrame(edges_df, geometry='geometry')

# 找到距离输入点最近的道路边
nearest_edge = None
min_distance = float('inf')

for idx, row in edges_gdf.iterrows():
    distance = input_point.distance(row['geometry'])
    if distance < min_distance:
        min_distance = distance
        nearest_edge = row['road_id']

# 输出最近道路边的ID值
print(f"距离输入经纬度最近的道路边的ID值是: {nearest_edge}")

# 保存筛选后的节点数据为 CSV
#filtered_points_gdf.to_csv("filtered_points.csv", index=False)

# 保存驱动的道路数据为 CSV
#driven_edges_gdf.to_csv("driven_edges.csv", index=False)


