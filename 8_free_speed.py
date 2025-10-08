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

    label_10 = pd.date_range('2016-10-%s 00:00:00' % day, '2016-10-%s 00:00:00' % str(int(day)+1), freq='10T')
    bins_10 = []
    for i in range(145):
        bins_10.append(times - 1 + i * 600)
    t_list_10 = pd.DataFrame(label_10, columns=['aa']).aa.astype(str).to_list()
    label_10 = []
    for i in range(len(t_list_10) - 1):
        label_10.append(t_list_10[i][8:-3] + '-' + t_list_10[i + 1][11:-3])

    print(label_10)
    print(bins_10)

    data['group_10'] = pd.cut(data.timestamp, bins=bins_10, labels=label_10)

    data_10 = data[['id', 'road_id', 'speed', 'group_10']]

    def cacluate_free_speed(trj_data):

        trj_speed = trj_data.groupby(['group_10', 'id']).speed.mean().dropna().reset_index(drop=False)[['group_10', 'speed']]

        free_speed = trj_speed.speed.quantile(0.85) #按85百分位的速度作为自由流速度

        if free_speed  == 0:
            free_speed = 40
        elif free_speed > 80:
            free_speed = 80
        elif free_speed < 20 and free_speed > 0:
            free_speed = 20

        return free_speed



    # 计算每条道路自由流速度
    opath_list = data.road_id.unique()
    free_speed_data = []
    for i in list(opath_list):
        data_1 = data_10[data_10.road_id == i][['id', 'speed', 'group_10']] # 每天每个路段i的所有轨迹数据
        cur_free_speed = cacluate_free_speed(data_1)
        free_speed_data.append(cur_free_speed)
        print(free_speed_data)


    free_speed = pd.DataFrame(columns=['road_id','free_speed'])
    free_speed['road_id'] = opath_list
    free_speed['free_speed'] = free_speed_data

    free_speed.to_csv("/home/dell/PycharmProjects/CD_traffic/data/7_free_speed/10_%s" % day + ".csv",
                              index=False)



files = glob.glob("/home/dell/PycharmProjects/CD_traffic/data/5_new_road_id_trj__data/*.csv")
files = sorted(files,key=lambda x: (int(x[70:-4])))
print(files)
for file in files:
    print(file)
    every_trj_road_speed(file)