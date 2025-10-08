import pandas as pd

data = pd.read_csv("filtered_data.csv")


data['time'] = data['time'].str[-8:-3]

# 计算车辆经过每个路段的平均车速
data['speed'] = data['speed'].astype(float)  # 确保速度列是数值类型
data['hour'] = data['time'].str[:2].astype(int)
data['minute'] = data['time'].str[3:].astype(int)
# 计算车辆经过每个路段的平均车速
data['speed'] = data['speed'].astype(float)  # 确保速度列是数值类型
data = data[data['speed'] > 0]
road_hour_minute_speed = data.groupby(['road_id', 'hour', 'minute'])['speed'].mean().reset_index(name='average_speed')
data_unique = data.drop_duplicates(['road_id', 'hour', 'minute', 'id'])
# 按照道路、小时和分钟进行分组，并计算每个小时每条道路的车辆数量
road_hour_minute_count = data.groupby(['road_id', 'hour', 'minute']).size().reset_index(name='vehicle_count')



result = pd.merge(road_hour_minute_count, road_hour_minute_speed, on=['road_id', 'hour', 'minute'], how='left')
# 输出结果
result.to_csv('road_speed.csv', index=False)





