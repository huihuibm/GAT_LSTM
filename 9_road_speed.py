import pandas as pd
import glob
import time

def date_to_timestamp(date):
    t = date
    s_t = time.strptime(t, "%Y-%m-%d %H:%M:%S")  # 返回元祖
    mkt = int(time.mktime(s_t))
    return mkt

def every_trj_road_speed(file_path):
    day = file_path[70:-4]
    print(day)
    data = pd.read_csv(file_path)

    data.time = pd.to_datetime(data.time)
    date = '2016-10-' + day + ' 00:00:00'
    times = date_to_timestamp(date)

    label_60 = pd.date_range('2016-10-%s 00:00:00' % day, '2016-10-%s 00:00:00' % str(int(day) + 1), freq='60T')
    bins_60 = []
    for i in range(25):
        bins_60.append(times - 1 + i * 3600)
    t_list_60 = pd.DataFrame(label_60, columns=['aa']).aa.astype(str).to_list()
    label_60 = []
    for i in range(len(t_list_60) - 1):
       label_60.append(t_list_60[i][8:-3] + '-' + t_list_60[i + 1][11:-3])

    data['group_60'] = pd.cut(data.timestamp, bins=bins_60, labels=label_60)

    data_60 = data[['id', 'road_id', 'speed', 'group_60']]

    def cacluate_road_speed(trj_data_2):
        trj_speed_2= trj_data_2.groupby(['group_60', 'id']).speed.mean().dropna().reset_index(drop=False)[['group_60', 'speed']]

        road_speed_60 = trj_speed_2.groupby('group_60').speed.mean().reset_index(drop=False).rename(
           columns={'speed': "road_speed"})
        road_speed_60['road_id'] = i
        flow_60 = trj_speed_2.groupby('group_60').count().reset_index(drop=False)
        road_speed_60 = pd.merge(road_speed_60, flow_60, how='left').rename(columns={'speed': 'flow'})

        return road_speed_60

    # 计算每条道路道路速度
    opath_list = data.road_id.unique()
    road_speed_data_60 = pd.DataFrame(columns=['group_60', 'road_speed', 'road_id','flow'])
    for i in list(opath_list):
        data_2 = data_60[data_60.road_id == i][['id', 'speed', 'group_60']]  # 每天每个路段i的所有轨迹数据

        b = cacluate_road_speed(data_2)
        road_speed_data_60 = road_speed_data_60.append(b, ignore_index=True)
        print(road_speed_data_60)
    road_speed_data_60.to_csv("/home/dell/PycharmProjects/CD_traffic/data/8_road_speed/60/10_%s" % day + ".csv", index=False)




files = glob.glob("/home/dell/PycharmProjects/CD_traffic/data/5_new_road_id_trj__data/*.csv")
files = sorted(files,key=lambda x: (int(x[70:-4])))
print(files)
for file in files:
    print(file)
    every_trj_road_speed(file)