"""
输入：划分日期后的文件 ：/home/dell/PycharmProjects/CD_traffic/data/2_day_data
输出：初步预处理后的文件 ： /home/dell/PycharmProjects/CD_traffic/data/3_preliminary_handle
"""
import time
import modin.pandas as pd
import glob
import osmnx as ox
import matplotlib.pyplot as plt
import transbigdata as tbd
import numpy as np
import warnings
warnings.filterwarnings("ignore")



# 获取路网并下载
def get_road_network(min_lat, max_lat, min_lon, max_lon, save_path):
    start_time = time.time()
    # 下载路网
    cd_road = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='drive')
    print("--- 获取路网数据完毕 ---！")
    # 保存路网
    #ox.save_graph_shapefile(cd_road, save_path)
    print("--- 路网数据保存完毕！---")
    print("--- 耗时 %ss ---"%(time.time() - start_time))
    return cd_road


# 读取路网和轨迹数据并可视化
def gps_visualize(cd_road, data,save_path):
    start_time = time.time()

    lat = data.latitude.to_list()
    lon = data.longitude.to_list()
    fig, ax = ox.plot_graph(cd_road, figsize=(15, 15), show=False, close=False, node_size=4, bgcolor='white',
                            node_color='black', edge_color='grey')
    ax.scatter(lon, lat, s=0.5, alpha=0.8, c='red')
    plt.savefig("/home/dell/PycharmProjects/CD_traffic/data/0_visualization_data/"+save_path, dpi=300)
    print("可视化完成")
    print("--- 耗时 %ss ---" % (time.time() - start_time))
    return

# 计算时间差、距离、速度，并将轨迹的第一个第初始化为0
def pre_caluate(data):
    start_time = time.time()
    data['time_diff'] = data.timestamp.diff().fillna(0)

    end_lon = pd.DataFrame(np.insert(data.longitude.values, 0, values=data.longitude.loc[0], axis=0))[:-1]
    end_lat = pd.DataFrame(np.insert(data.latitude.values, 0, values=data.latitude.loc[0], axis=0))[:-1]
    data['distance'] = tbd.getdistance(data['longitude'], data['latitude'], end_lon[0], end_lat[0])

    data['speed'] = (data.distance / data.time_diff.astype(float)) * 3.6
    data.speed = data.speed.fillna(0)

    idx = data.groupby('trj_id').head(1).index
    data.time_diff.loc[idx] = 0
    data.distance.loc[idx] = 0
    data.speed.loc[idx] = 0
    print("预计算结束")
    print("--- 耗时 %ss ---" % (time.time() - start_time))
    return data

# 删除异常点并将轨迹分段（速度大于120）
def drop_exception_and_split_trj_id(data):
    start_time = time.time()
    trj_id = data.trj_id.to_list()
    exception_index = data[data.speed>120].index.tolist()
    for i in range(len(exception_index)-1):
        trj_id[exception_index[i]:exception_index[i+1]] = [x+i+1 for x in trj_id[exception_index[i]:exception_index[i+1]]]
    trj_id[exception_index[len(exception_index)-1]:] = [x + exception_index[len(exception_index)-1] + 1 for x in trj_id[exception_index[len(exception_index)-1]:]]
    new_trj_id = pd.DataFrame(trj_id,columns=['trj_id'])
    new_trj_id = new_trj_id.drop(exception_index)
    new_id  = dict(zip(new_trj_id.trj_id.unique(),range(1,len(new_trj_id.trj_id.unique()) + 1)))
    new_trj_id = new_trj_id.trj_id.map(new_id).reset_index(drop=True)
    data = data[~data.index.isin(exception_index)].reset_index(drop=True)
    data['trj_id'] = new_trj_id
    print("完成异常的采样的的清除")
    print("--- 耗时 %ss ---" % (time.time() - start_time))
    return data



# 删除超出范围的轨迹
def drop_out_of_scope(gps_data_1,lat1,lon1,lat2,lon2):
    start_time = time.time()
    # 统计超出范围的轨迹id
    out_id=gps_data_1[((gps_data_1['latitude']>lat1)&(gps_data_1['latitude']<lat2)&(gps_data_1['longitude']>lon1)&(gps_data_1['longitude']<lon2))]
    # 将超出范围内的轨迹点及其所在的轨迹进行删除
    gps_data_2 = gps_data_1[gps_data_1.trj_id.isin(list(out_id.trj_id.unique()))].reset_index(drop=True)
    # 重置轨迹
    new_id = dict(zip(gps_data_2.trj_id.unique(),range(1,len(gps_data_2.trj_id.unique()) + 1)))
    gps_data_2['trj_id'] = gps_data_2['trj_id'].map(new_id)
    print("完成超出范围轨迹的清除")
    print("--- 耗时 %ss ---" % (time.time() - start_time))
    return gps_data_2

# 删除微小轨迹
def drop_tiny_trj(gps_data_reset):
    start_time = time.time()
    counts = gps_data_reset.trj_id.value_counts()
    mask = gps_data_reset.trj_id.isin(list(counts[counts < 5].index))
    gps_drop_tinyTrj = gps_data_reset[~mask].reset_index(drop=True)
    new_id = dict(zip(gps_drop_tinyTrj.trj_id.unique(),range(1,len(gps_drop_tinyTrj.trj_id.unique()) + 1)))
    gps_drop_tinyTrj['trj_id'] = gps_drop_tinyTrj['trj_id'].map(new_id)
    print("完成微小轨迹的清除")
    print("--- 耗时 %ss---" % (time.time() - start_time))
    return gps_drop_tinyTrj


def process(file_path):
    day = file_path[57:-4]
    print(day)
    # 读取数据
    data = pd.read_csv(file_path, names=['trj_id', 'timestamp', 'longitude', 'latitude'])
    # 用数字代替订单号，首先认为一个订单号为一条轨迹
    order = dict(zip(data.trj_id.unique(), range(1, len(data.trj_id.unique()) + 1)))
    data['trj_id'] = data['trj_id'].map(order)
    print("—————————— 数据读取完成 ——————————")
    # 可视化原始数据并保存
    #gps_visualize(cd_road, data, "1_raw_data_visualize"+"/10_%s.png" %day)
    print("—————————— ——————————")
    # 进行坐标转换
    data['longitude'], data['latitude'] = tbd.gcj02towgs84(data['longitude'], data['latitude'])
    print("—————————— 坐标转换完成 ——————————")
    # 进行预先计算
    data = pre_caluate(data)
    print("—————————— ——————————")
    # 清除异常点
    data = drop_exception_and_split_trj_id(data)
    print("—————————— ——————————")
    # 重新计算
    data = pre_caluate(data)
    print("—————————— ——————————")
    # 数据去重
    data = data.drop_duplicates(subset=['trj_id', 'timestamp']).reset_index(drop=True)
    print("—————————— ——————————")
    # 去除超出范围的轨迹
    data = drop_out_of_scope(data, min_lat, min_lon, max_lat, max_lon)
    print("—————————— ——————————")
    # 去除微小轨迹
    data = drop_tiny_trj(data)
    print("—————————— ——————————")
    # 保存数据
    data = data[['trj_id', 'timestamp', 'longitude', 'latitude']]
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s',origin = "1970-01-01 08:00:00")
    data = data.rename(columns={'trj_id': "id"})
    data.to_csv(file_path[:43] + "3_pre_process_data/10_%s.csv" % day, index=False)
    print("—————————— 数据保存成功 ——————————")
    #gps_visualize(cd_road, data, "2_after_pre_process_visualize"+"/10_%s.png" % day)


start_time_all = time.time()
min_lat = 30.6500
max_lat = 30.73100
min_lon = 104.03900
max_lon = 104.12800
road_network_path = "/home/dell/PycharmProjects/CD_traffic/data/road_network"
input_file = "/home/dell/PycharmProjects/CD_traffic/data/2_day_data/"
#cd_road = get_road_network(min_lat, max_lat, min_lon, max_lon, road_network_path)

files = glob.glob("/home/dell/PycharmProjects/CD_traffic/data/2_day_data/*.csv")
for file in files:
    process(file)
print("###################总耗时%ss#####################"%(time.time() - start_time_all))


