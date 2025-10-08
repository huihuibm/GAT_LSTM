import pandas as pd

# 读取自由流速度数据
free_speed_data = pd.read_csv('road_free_speed.csv')

# 读取交通道路的平均速度数据
traffic_data = pd.read_csv('road_speed.csv')

# 合并两份数据
merged_data = traffic_data.merge(free_speed_data, on='road_id')

# 计算TPI值
merged_data['TPI'] = ((merged_data['free_speed'] - merged_data['average_speed']) / merged_data['free_speed'])

filtered_data = merged_data[merged_data['TPI'] > 0.5]

# 根据时间进行排序
merged_data = merged_data.sort_values(by=['road_id', 'minute'])

# 计算每个road_id的连续十分钟TPI均值
merged_data['TPI_mean'] = merged_data.groupby('road_id')['TPI'].rolling(window=10, min_periods=10).mean().reset_index(0, drop=True)

# 筛选出连续十分钟TPI均值都大于0.5的road_id
filtered_data = merged_data[merged_data['TPI_mean'] > 0.5]['road_id'].unique()

print("连续十分钟TPI均值都大于0.5的road_id：", filtered_data)


