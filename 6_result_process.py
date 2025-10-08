"""
输入：/home/dell/PycharmProjects/CD_traffic/data/4_map_matching/4_gps/*.csv
    获取道路id、时间差信息：/home/dell/PycharmProjects/CD_traffic/data/4_map_matching/2_result/
    获取时间戳：/home/dell/PycharmProjects/CD_traffic/data/3_pre_process_data/

输出：/home/dell/PycharmProjects/CD_traffic/data/4_map_matching/5_finall_data/*.csv
"""

import modin.pandas as pd
import osmnx as ox
import matplotlib.pyplot as plt
import glob
import gc
import time
import transbigdata as tbd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def get_opath(data):
    opath = data['opath'].str.split(',').to_list()
    del data
    gc.collect()
    opath = [i for j in range(len(opath)) for i in opath[j]]
    a = pd.DataFrame(opath)
    del opath
    gc.collect()
    print('get opath')
    return a


def get_duration(a):
    duration = a['duration'].str.split(',').to_list()
    del a
    gc.collect()

    for i in duration:
        i.insert(0, 0)
    duration = [i for j in range(len(duration)) for i in duration[j]]
    b = pd.DataFrame(duration)
    del duration
    gc.collect()
    print('get duration')
    return b


def get_timestamp(data, raw_data):
    data = data.sort_values(["id", 'point_idx']).reset_index(drop=True)
    data['time'] = raw_data.timestamp
    return data


def get_road_network(min_lat, max_lat, min_lon, max_lon):
    start_time = time.time()
    # 下载路网
    cd_road = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='drive')
    print("--- 获取路网数据完毕 ---！")

    print("--- 耗时 %ss ---" % (time.time() - start_time))
    return cd_road


# 读取路网和轨迹数据并可视化
def gps_visualize(cd_road, data, save_path):
    start_time = time.time()

    lat = data.latitude.to_list()
    lon = data.longitude.to_list()
    fig, ax = ox.plot_graph(cd_road, figsize=(15, 15), show=False, close=False, node_size=4, bgcolor='white',
                            node_color='black', edge_color='grey')
    ax.scatter(lon, lat, s=0.5, alpha=0.8, c='red')
    plt.savefig("/home/dell/PycharmProjects/CD_traffic/data/0_visualization_data/" + save_path, dpi=300)
    print("可视化完成")
    print("--- 耗时 %ss ---" % (time.time() - start_time))
    return


def pre_caluate(data):
    start_time = time.time()

    timestamps = pd.to_datetime(data['time'])
    data['timestamp'] = (timestamps.astype(int) / 1000000000)-28800
    data['timestamp'] = data.timestamp.astype(int).to_list()

    data['time_diff'] = data.timestamp.diff().fillna(0)

    end_lon = pd.DataFrame(np.insert(data.longitude.values, 0, values=data.longitude.loc[0], axis=0))[:-1]
    end_lat = pd.DataFrame(np.insert(data.latitude.values, 0, values=data.latitude.loc[0], axis=0))[:-1]
    data['distance'] = tbd.getdistance(data['longitude'], data['latitude'], end_lon[0], end_lat[0])

    data['speed'] = (data.distance / data.time_diff.astype(float)) * 3.6
    data.speed = data.speed.fillna(0)



    idx = data.groupby('id').head(1).index
    data.time_diff.loc[idx] = 0
    data.distance.loc[idx] = 0
    data.speed.loc[idx] = 0

    print("--- 预计算完成！---")
    print("--- 耗时 %ss ---" % (time.time() - start_time))
    return data


def drop_dup(data):
    start_time = time.time()
    data = data.drop_duplicates(subset=['id', 'time', 'longitude', 'latitude']).reset_index(drop=True)
    new_id = dict(zip(data.id.unique(), range(1, len(data.id.unique()) + 1)))
    new_trj_id = data.id.map(new_id).reset_index(drop=True)
    data.id = new_trj_id
    idx = data.groupby('id').head(1).index
    data.time_diff.loc[idx] = 0
    data.distance.loc[idx] = 0
    data.speed.loc[idx] = 0
    print("--- 完成清除重复的数据！---")
    print("--- 耗时 %ss ---" % (time.time() - start_time))
    return data

def drop_exception_and_split_trj_id(data):
    start_time = time.time()
    trj_id = data.id.to_list()
    exception_index = data[data.speed>120].index.tolist()
    for i in range(len(exception_index)-1):
        trj_id[exception_index[i]:exception_index[i+1]] = [x+i+1 for x in trj_id[exception_index[i]:exception_index[i+1]]]
    trj_id[exception_index[len(exception_index)-1]:] = [x + exception_index[len(exception_index)-1] + 1 for x in trj_id[exception_index[len(exception_index)-1]:]]
    new_trj_id = pd.DataFrame(trj_id,columns=['trj_id'])
    new_trj_id = new_trj_id.drop(exception_index)
    new_id  = dict(zip(new_trj_id.trj_id.unique(),range(1,len(new_trj_id.trj_id.unique()) + 1)))
    new_trj_id = new_trj_id.trj_id.map(new_id).reset_index(drop=True)
    data = data[~data.index.isin(exception_index)].reset_index(drop=True)
    data['id'] = new_trj_id
    print("完成异常的采样的的清除")
    print("--- 耗时 %ss ---" % (time.time() - start_time))
    return data

# 去除轨迹点数小于5的和轨迹长度小于500m
def drop_tiny_trj(gps_data_reset):
    start_time = time.time()
    counts = gps_data_reset.id.value_counts()
    mask = gps_data_reset.id.isin(list(counts[counts < 5].index))
    gps_drop_tinyTrj = gps_data_reset[~mask].reset_index(drop=True)

    counts_1 = gps_drop_tinyTrj.groupby('id').distance.sum()
    mask_1 = gps_drop_tinyTrj.id.isin(list(counts_1[counts_1 < 500].index))
    gps_drop_tinyTrj = gps_drop_tinyTrj[~mask_1].reset_index(drop=True)

    new_id = dict(zip(gps_drop_tinyTrj.id.unique(), range(1, len(gps_drop_tinyTrj.id.unique()) + 1)))
    gps_drop_tinyTrj['id'] = gps_drop_tinyTrj['id'].map(new_id)
    print("--- 完成清除微小轨迹！---")
    print("--- 耗时 %ss ---" % (time.time() - start_time))
    return gps_drop_tinyTrj

def process(file_path):
    day = file_path[67:-4]
    print(day)
    data = pd.read_csv(file_path, sep=';')
    data = data.rename(columns={'x': 'longitude', 'y': 'latitude'})
    map_result = pd.read_csv('/home/dell/PycharmProjects/CD_traffic/data/4_map_matching/2_result/10_%s.csv' % day, sep=';')
    raw_data = pd.read_csv('/home/dell/PycharmProjects/CD_traffic/data/3_pre_process_data/10_%s.csv' % day)
    data['opath'] = get_opath(map_result)
    data['time_diff'] = get_duration(map_result)
    data = get_timestamp(data, raw_data)
    data = pre_caluate(data)
    data = drop_exception_and_split_trj_id(data)
    data = pre_caluate(data)
    data = drop_tiny_trj(data)
    data = data.drop(columns='point_idx')
    data.to_csv("/home/dell/PycharmProjects/map_matching/data/4_map_matching/5_finall_data/10_%s.csv" % day,index=False)
    #gps_visualize(cd_road, data, "3_after_map_matching" + "/10_%s.png" % day)

min_lat = 30.6500
max_lat = 30.73100
min_lon = 104.03900
max_lon = 104.12800
#cd_road = get_road_network(min_lat, max_lat, min_lon, max_lon)

files = glob.glob("/home/dell/PycharmProjects/CD_traffic/data/4_map_matching/4_gps/*.csv")
for file in files:

    process(file)