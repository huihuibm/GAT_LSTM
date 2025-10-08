# encoding:utf-8
from fmm import Network,NetworkGraph,STMATCH,STMATCHConfig,GPSConfig,ResultConfig


import glob
network = Network("/fmm/projects/CD_traffic/data/road_network/edges.shp","osmid", "u", "v")
graph = NetworkGraph(network)
model = STMATCH(network,graph)

config = STMATCHConfig()
config.k = 8##搜索范围内备选点
config.gps_error = 0.5##gps误差
config.radius = 0.8##搜索半径
config.factor =1.5##速度的考察权重

input_config = GPSConfig()

input_config.id = "id"

result_config = ResultConfig()
result_config.output_config.write_ogeom =False
result_config.output_config.write_opath =False
result_config.output_config.write_pgeom = True
result_config.output_config.write_cpath = False
result_config.output_config.write_mgeom = False
result_config.output_config.write_tpath =False



files = glob.glob(r"/fmm/projects/CD_traffic/data/4_map_matching/1_trj/*.csv")

files_sorted = sorted(files,
                          key=lambda x: (int(x[54:-4])))

for file in files_sorted:

    input_config.file = file
    result_config.file = "/fmm/projects/map_matching/data/4_map_matching/2_result/"+file[51:-4]+".csv"
    status = model.match_gps_file(input_config, result_config,config)
    print(status)

        
