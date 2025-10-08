
import modin.pandas as pd
import glob


def split_day(input_path, output_path):
    # 读取文件
    data = pd.read_csv(input_path, sep=',', names=['driver_id', 'order_id', 'timestamp', 'longitude', 'latitude'])
    # 排序
    data = data.sort_values(by=['driver_id', 'order_id', 'timestamp']).reset_index(drop=True)
    # 时间转换为datetime格式
    data['time'] = pd.to_datetime(data['timestamp'], unit='s',origin = "1970-01-01 08:00:00")
    # 存在天数的列表
    day = data.time.dt.day.unique()
    # 遍历每个日期
    for i in day:
        if i in list(range(1, 21)):
            # 保存数据
            data[data.time.dt.day == i][['order_id', 'timestamp', 'longitude', 'latitude']].to_csv(
                output_path + "/10_%d.csv" % i, mode='a', index=False, header=False)


def main():
    input_path = "/home/dell/PycharmProjects/CD_traffic/data/1_raw_data"
    output_path = "/home/dell/PycharmProjects/CD_traffic/data/2_day_data"
    files = glob.glob(input_path+"/*.csv")
    for file in files:
        print(file)
        split_day(file, output_path)


if __name__ == '__main__':
    main()
