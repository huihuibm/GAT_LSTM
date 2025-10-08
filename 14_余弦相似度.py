import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 从 CSV 文件加载节点数据
nodes_df = pd.read_csv("only_driven/filtered_points.csv")

# 从 CSV 文件加载边数据
edges_df = pd.read_csv("only_driven/driven_edges.csv")

# 从 CSV 文件加载特征向量数据
vectors_df = pd.read_csv("Fs-embedding.csv")

# 首先，根据边数据集创建一个字典，以每个节点作为键，相邻边的列表作为值
adjacent_edges_dict = {}

for index, row in edges_df.iterrows():
    u, v = row['u'], row['v']
    if u not in adjacent_edges_dict:
        adjacent_edges_dict[u] = []
    if v not in adjacent_edges_dict:
        adjacent_edges_dict[v] = []
    adjacent_edges_dict[u].append(row['road_id'])
    adjacent_edges_dict[v].append(row['road_id'])

# 然后，利用字典中的相邻边信息，创建一个包含相邻边的列表
adjacent_edges_list = []

for u, edge_ids in adjacent_edges_dict.items():
    for edge_id in edge_ids:
        for other_edge_id in edge_ids:
            if edge_id != other_edge_id:
                adjacent_edges_list.append((edge_id, other_edge_id))

# 去除重复的相邻边对
adjacent_edges_list = list(set(adjacent_edges_list))

# 首先，根据road_id将特征向量合并到edges_df中
edges_df = pd.merge(edges_df, vectors_df, on='road_id')

# 将特征向量的空格分隔字符串转换为numpy数组
def parse_feature_vector(feature_str):
    return np.array([float(x) for x in feature_str.split()])

# 然后，定义一个函数来计算余弦相似度
def calculate_cosine_similarity(feature1, feature2):
    return cosine_similarity([feature1], [feature2])[0][0]

# 接下来，对每对相邻边计算余弦相似度
for idx, (edge1_id, edge2_id) in enumerate(adjacent_edges_list):
    edge1_feature = parse_feature_vector(edges_df.loc[edges_df['road_id'] == edge1_id, 'feature'].values[0])
    edge2_feature = parse_feature_vector(edges_df.loc[edges_df['road_id'] == edge2_id, 'feature'].values[0])
    cosine_sim = calculate_cosine_similarity(edge1_feature, edge2_feature)
    adjacent_edges_list[idx] = (edge1_id, edge2_id, cosine_sim)

# 创建一个DataFrame来存储结果
result_df = pd.DataFrame(adjacent_edges_list, columns=['road_id_1', 'road_id_2', 'cosine_similarity'])
result_df.to_csv("adjacent_edges_similarity.csv", index=False)
# 将结果保存到CSV文件中



