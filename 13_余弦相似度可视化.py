import csv
import ast
import networkx as nx

import matplotlib.pyplot as plt

# 1. 解析边文件
edges = []
with open('D:\PycharmProjects\pythonProject\G\\road_network\\updated_graph_edges.csv', 'r') as f_edges:
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

# 3. 创建有向图
G = nx.MultiDiGraph()

# 4. 添加节点和边到图中，并计算每个节点的出边相似度之和
node_similarity_sum = {}  # 用于存储每个节点的出边相似度之和
for edge in edges:
    start_node, end_node, similarity = edge
    G.add_edge(start_node, end_node, similarity=similarity)
    if start_node in node_similarity_sum:
        node_similarity_sum[start_node] += similarity
    else:
        node_similarity_sum[start_node] = similarity

# 5. 将相似度之和作为节点属性
for node in G.nodes:
    if node in node_similarity_sum:
        G.nodes[node]['similarity_sum'] = node_similarity_sum[node]
    else:
        G.nodes[node]['similarity_sum'] = 0.2
        node_similarity_sum[node]=0.2# 如果没有出边，默认相似度之和为0
node_similarity_avg = {}  # 用于存储每个节点的出边相似度之和
for node in G.nodes:
    node_similarity_avg[node]=node_similarity_sum[node]/G.degree(node)


for node in G.nodes:
    if node in node_similarity_avg:
        G.nodes[node]['similarity_avg'] = node_similarity_avg[node]
    else:
        G.nodes[node]['similarity_avg'] = 0.2


# 6. 绘制图形，并根据节点的相似度之和调整节点的大小
plt.figure(figsize=(12, 8))
node_sizes = [G.nodes[node]['similarity_avg'] * 10 for node in G.nodes]
edge_widths = [e[2]  for e in G.edges(data='similarity')]
nx.draw(G, pos=node_positions, with_labels=False, node_size=node_sizes, node_color='red', font_size=10, font_color='black', edge_color='gray', width=edge_widths)
plt.title('Visualization of Directed Graph with Node Similarity Sums and Edge Thickness by Similarity')
plt.show()
