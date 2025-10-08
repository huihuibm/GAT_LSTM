import csv
import ast
import networkx as nx
import matplotlib.pyplot as plt
import pandas as  pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 有一个包含节点特征的CSV文件，加载这些特征数据
node_features_df = pd.read_csv('result_dataset.csv')

# 构建一个字典来映射节点到特征的关系
node_features = dict(zip(node_features_df['road_id'], node_features_df['feature']))
# 将特征向量的空格分隔字符串转换为numpy数组
def parse_feature_vector(feature_str):
    return np.array([float(x) for x in feature_str.split()])

# 然后，定义一个函数来计算余弦相似度
def calculate_cosine_similarity(feature1, feature2):
    return cosine_similarity([feature1], [feature2])[0][0]
# 1. 解析边文件
edges = []
with open('graph_edges.csv', 'r') as f_edges:
    reader = csv.reader(f_edges)
    next(reader)  # skip header
    for row in reader:
        start_node = int(row[0])
        end_node = int(row[1])
        similarity_str = row[2].strip()
        if similarity_str != 'N/A':
            similarity = float(similarity_str)
            edges.append((start_node, end_node, similarity))

# 2. 解析节点位置文件
node_positions = {}
with open('node_positions.csv', 'r') as f_nodes:
    reader = csv.reader(f_nodes)
    next(reader)  # skip header
    for row in reader:
        node_id = int(ast.literal_eval(row[0])[2])  # extract node_id from "(...)" format
        x_coord = float(row[1])
        y_coord = float(row[2])
        node_positions[node_id] = (x_coord, y_coord)


G = nx.MultiDiGraph()

# 3. 添加节点和边到图中
for edge in edges:
    start_node, end_node, similarity = edge
    G.add_edge(start_node, end_node, similarity=similarity)

second_order_successors = {}

H = nx.MultiDiGraph()

def generate_n_neighbors(graph, n):
    H = nx.MultiDiGraph()

    for node in graph.nodes():
        neighbors = set([node])
        for _ in range(n):
            current_neighbors = set(neighbors)
            for neighbor in current_neighbors:
                neighbors.update(graph.successors(neighbor))
        neighbors.remove(node)  # Remove the node itself from its neighbors

        for neighbor in neighbors:
            H.add_edge(node, neighbor)
    save_graph_to_csv(H, f'{n}_graph_edges.csv')
    return H
def get_neigbors(g, node, depth=1):
    output = {}
    layers = dict(nx.bfs_successors(g, source=node, depth_limit=depth))
    nodes = [node]
    for i in range(1,depth+1):
        output[i] = []
        for x in nodes:
            output[i].extend(layers.get(x,[]))
        nodes = output[i]
    return output

def save_graph_to_csv(graph, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['start_node', 'end_node']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for u, v, attrs in graph.edges(data=True):
            start_node = u
            end_node = v

            writer.writerow({'start_node': start_node, 'end_node': end_node })

H=generate_n_neighbors(G,5)
# 5. 绘制原始图和二阶图
plt.figure(figsize=(12, 8))

# 绘制原始图
#nx.draw(G, pos=node_positions, with_labels=False, node_size=20, node_color='skyblue', font_size=10, font_color='black', edge_color='gray', width=0.5)
# 绘制二阶图，使用红色表示
edge_labels = {(u, v): round(d.get('weight', 1.0), 2) for u, v, d in H.edges(data=True)}
nx.draw_networkx_nodes(H,pos=node_positions, node_size=20,node_color='skyblue')
nx.draw_networkx_edges(H, pos=node_positions,node_size=20, edge_color='red')

subgraph = nx.Graph()
#生成最小邻居图
def generate_subgraph(road_id):
    neighbors = list(G.neighbors(road_id))
    subgraph.add_node(road_id)
    for neighbor in neighbors:
        if G.nodes[neighbor]['tpi'] > 0.5:
            subgraph.add_node(neighbor)
            subgraph.add_edge(road_id, neighbor)
            generate_subgraph(neighbor)


plt.show()
