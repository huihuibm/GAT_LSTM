import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from shapely import wkt

# 读取点shp文件
points_shapefile_path = "nodes.shp"
points_gdf = gpd.read_file(points_shapefile_path)

# 读取边CSV文件
edges_csv_path = "G_1_data.csv"
edges_df = pd.read_csv(edges_csv_path)

# 将几何信息转换为LineString类型
edges_df['geometry'] = edges_df['geometry'].apply(wkt.loads)

# 创建边的GeoDataFrame
edges_gdf = gpd.GeoDataFrame(edges_df, geometry='geometry')

# 读取记录了行驶过的道路特征的CSV文件
driven_roads_csv_path = "result_dataset.csv"
driven_roads_df = pd.read_csv(driven_roads_csv_path)

# 将行驶过的道路与未行驶过的道路进行区分
edges_gdf['driven'] = edges_gdf['road_id'].isin(driven_roads_df['road_id'])

# 创建一个新的图形
fig, ax = plt.subplots()

# 可视化点，设置颜色为白色
points_gdf.plot(ax=ax, color='white', markersize=5)

# 根据行驶状态可视化边
driven_color = 'red'
undriven_color = 'blue'
edges_gdf[edges_gdf['driven']].plot(ax=ax, color=driven_color, linewidth=1, label='Driven Roads')
edges_gdf[~edges_gdf['driven']].plot(ax=ax, color=undriven_color, linewidth=1, linestyle='--', label='Un-driven Roads')

# 设置图例
ax.legend()

# 设置图形标题
plt.title('Driven and Un-driven Roads')

# 保存为SVG格式
#plt.savefig('road_network.svg', format='svg')

# 显示图形
plt.show()
