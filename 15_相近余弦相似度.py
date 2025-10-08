import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 读取CSV文件
df = pd.read_csv('result_dataset.csv')

# 假设标签列名为 'Label'，即你的数据中有一列包含这些标签
labels = df['road_id'].values

# 提取数据，假设数据在CSV文件的第一列到倒数第二列
data = df.iloc[:, 1:].values
float_data = [[float(num_str) for num_str in sublist[0].split()] for sublist in data]

pca = PCA(n_components=2)
data_pca = pca.fit_transform(float_data)

# 找到特定数据点的索引
special_indices = []
for i, label in enumerate(labels):
    if label == 836 or label == 2786 or label == 2217  or label == 2654 or label == 3548 or label == 3979 or label == 3978:  # 假设这些是特殊点的标签
        special_indices.append(i)

# 可视化PCA降维后的数据
plt.figure(figsize=(8, 6))

# 绘制非特殊点
plt.scatter(data_pca[:, 0], data_pca[:, 1], label='Other Data')

# 绘制特殊点
plt.scatter(data_pca[special_indices, 0], data_pca[special_indices, 1], color='red', label='Special Data')

# 标记特殊点
for index in special_indices:
    plt.text(data_pca[index, 0], data_pca[index, 1], str(labels[index]), fontsize=12, ha='center', va='bottom')

plt.title('PCA Visualization of Data')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.grid(True)
plt.show()
