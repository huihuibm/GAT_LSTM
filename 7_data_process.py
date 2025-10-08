"""
输入：/home/dell/PycharmProjects/CD_traffic/data/4_map_matching/5_finall_data/*.csv
输出：/home/dell/PycharmProjects/CD_traffic/data/5_new_road_id_trj__data/*.csv
"""
import geopandas as gpd
import networkx as nx
import pandas as pd
import numpy as np
import osmnx as ox
import transbigdata as tbd
import glob

# 读取原始路网的边
edge_shp=gpd.read_file('/home/dell/PycharmProjects/CD_traffic/data/road_network/edges.shp')
edge_shp = edge_shp[['u','v','osmid','geometry']]
edge_shp = edge_shp.drop_duplicates(subset=['u','v','osmid'],keep='first').reset_index(drop=True)
G_1 = edge_shp.reset_index(drop=False).rename(columns={'index':'road_id'})
G_1.to_csv('/home/dell/PycharmProjects/CD_traffic/data/G_1_data.csv',index=False)

# 读取轨迹数据
def save_new_data(file):
    trj_data = pd.read_csv(file)
    trj_data=trj_data[['id','longitude','latitude','opath','timestamp','time','speed']]
    trj_data['geometry'] = gpd.points_from_xy(trj_data['longitude'],trj_data['latitude'])
    new_trj = tbd.ckdnearest_line(trj_data,G_1)
    new_trj = new_trj[['id','road_id','longitude','latitude','timestamp','time','speed']]
    new_trj.to_csv('/home/dell/PycharmProjects/CD_traffic/data/5_new_road_id_trj__data/'+file[72:],index=False)

files = glob.glob("/home/dell/PycharmProjects/CD_traffic/data/4_map_matching/5_finall_data/*.csv")
files = sorted(files,key=lambda x: (int(x[75:-4])))
for file in files:
    print(file[72:])
    save_new_data(file)