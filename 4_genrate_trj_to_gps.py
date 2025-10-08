"""

"""
import modin.pandas as pd
import glob

input_file = "/home/dell/PycharmProjects/CD_traffic/data/4_map_matching/2_result/"
files = glob.glob(input_file+"*.csv")
for file in files:
    data = pd.read_csv(file,sep=';')
    data[['id', 'pgeom']].rename(columns={'pgeom': 'geom'}).to_csv("/home/dell/PycharmProjects/CD_traffic/data/4_map_matching/3_trj_input/"+file[67:], index=False, sep=';')
    print(data)