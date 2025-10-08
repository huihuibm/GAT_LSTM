import pandas as pd
import networkx as nx
from shapely.wkt import loads
import csv
import matplotlib.pyplot as plt
import pickle

# 从 CSV 加载点数据
points_df = pd.read_csv("only_driven/filtered_points.csv", usecols=['osmid', 'x', 'y', 'geometry'])

# 从 CSV 加载边数据
edges_df = pd.read_csv("only_driven/driven_edges.csv", usecols=['road_id', 'u', 'v', 'osmid', 'geometry'])
road_avg_coordinates = {}
for index, row in edges_df.iterrows():
    road_id = row['road_id']
    geometry = row['geometry']
    geometry = loads(geometry)
    coords = geometry.coords
    sum_lon = 0
    sum_lat = 0
    for lon, lat in coords:
        sum_lon += lon
        sum_lat += lat
    avg_lon = sum_lon / len(coords)
    avg_lat = sum_lat / len(coords)
    road_avg_coordinates[road_id] = (avg_lon, avg_lat)

    # 在这里进行你想要的操作



# 创建一个空的有向多重图对象
G = nx.Graph()


# 添加点到图中
for index, row in points_df.iterrows():
    G.add_node(row['osmid'], geometry=loads(row['geometry']))  # 只保留 geometry

# 添加边到图中
for index, row in edges_df.iterrows():
    G.add_edge(row['u'], row['v'], key=row['road_id'], geometry=(row['geometry']))  # 添加 road_id 和 geometry 属性


# 可视化图像
plt.figure(figsize=(30, 24))

# 提取节点的位置信息
node_pos = {node: (data['geometry'].x, data['geometry'].y) for node, data in G.nodes(data=True)}

# 绘制节点
nx.draw_networkx_nodes(G, pos=node_pos, node_size=10, node_color='blue', alpha=0.7)

# 绘制边
nx.draw_networkx_edges(G, pos=node_pos, width=1.0, alpha=0.5)

# 显示图像
plt.title("Graph Visualization")  # 添加标题
plt.axis('off')  # 关闭坐标轴
#plt.show()



# 生成线图 L
L = nx.line_graph(G)

isolated_nodes = list(nx.isolates(L))

# 从图中删除孤立节点
L.remove_nodes_from(isolated_nodes)




# 从 CSV 加载相邻边的相似度数据
similarity_data = {}
with open("adjacent_edges_similarity.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        road_id_1 = int(row["road_id_1"])
        road_id_2 = int(row["road_id_2"])
        similarity = float(row["cosine_similarity"])
        similarity_data[(road_id_1, road_id_2)] = similarity

# 更新线图 L 的边属性
'''
for u,v,key,attrs in L.edges(data=True, keys=True):
    road_id_1 =u[2]
    road_id_2 = v[2]
    similarity = similarity_data.get((road_id_1, road_id_2), None)
    if similarity is not None:
         attrs["cosine_similarity"] = similarity
'''

# 提取图 L 中的节点位置信息
#node_positions = {node: road_avg_coordinates[int(node[2])] for node in L.nodes()}
def on_edge_click(event):
    # 检查点击是否在轴范围内
    if event.inaxes is not None:
        # 获取点击位置
        click_x, click_y = event.xdata, event.ydata
        for (u, v, d) in L.edges(data=True):
            # 获取边的起点和终点位置
            x1, y1 = node_positions[u]
            x2, y2 = node_positions[v]
            # 判断点击点是否在边的附近
            if min(x1, x2) <= click_x <= max(x1, x2) and min(y1, y2) <= click_y <= max(y1, y2):
                road_id_1 = u[2]
                road_id_2 = v[2]
                similarity = d.get("cosine_similarity", "N/A")
                plt.text(click_x, click_y, f"({road_id_1}, {road_id_2}): {similarity:.2f}", fontsize=12, color="red")
                plt.draw()
                break

def draw_graph():
    fig, ax = plt.subplots(figsize=(10, 10))
    nx.draw(L, pos=node_positions, node_size=10, node_color="b", edge_color="gray", with_labels=False, ax=ax)
    fig.canvas.mpl_connect("button_press_event", on_edge_click)
    plt.show()
#draw_graph()
def save_node_positions_to_csv(node_positions, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['node_id', 'x_coordinate', 'y_coordinate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for node_id, (x, y) in node_positions.items():
            writer.writerow({'node_id': node_id, 'x_coordinate': x, 'y_coordinate': y})

# 调用函数保存节点位置到 CSV 文件
#save_node_positions_to_csv(node_positions, 'Line_graph/node_positions.csv')


def save_graph_to_csv(graph, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['start_node', 'end_node', 'cosine_similarity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for u, v, attrs in graph.edges(data=True):
            start_node = u[2]
            end_node = v[2]
            cosine_similarity = attrs.get('cosine_similarity', 'N/A')
            writer.writerow({'start_node': start_node, 'end_node': end_node, 'cosine_similarity': cosine_similarity})

# 调用函数保存图到 CSV 文件
#print(L.nodes)

