
#%%
import numpy as np
import pandas as pd
import os
from pyproj.transformer import Transformer # nur import Transformer

ch_LV95_nach_WGS84 = Transformer.from_crs(2056, 4326) # EPSG-Codes als Argumente: EPSG 2056 = CH1903+ / LV95 ~ 4326 = WGS84
wgs_nach_ch_LV95 = Transformer.from_crs(4326, 2056)
wgs_nach_utm = Transformer.from_crs(4326, 4647)
WGS84_nach_ch_LV95 = Transformer.from_crs(4326, 2056)
#%%


#%%

# filepath off current file
file_dir, _ = os.path.split(os.path.realpath(__file__))

# # filepath of file/-s in this directory
# path_join = os.path.join(file_dir, XXX)

items = os.listdir(".") # in this current directory

# newlist = []
# for names in items:
#     if names.endswith(".zip"):
#         newlist.append(names)
# print(newlist)

# print(newlist[0])

# items = ["/home/empit/Nextcloud/EMPIT_shared/EWL_Auswertung_2021/EWL_gw/Brandgaessli_0.csv"]
for names in items:
    if names.endswith(".csv"):
        path_join = os.path.join(file_dir, names)
        try:
            df = pd.read_csv(path_join, header = 0, sep=",")      
            df.columns = df.columns.str.strip()
            pj_ch_wgs = ch_LV95_nach_WGS84.transform(df.rw, df.hw)
            pj_ch_wgs = np.array(pj_ch_wgs).T
            df['Latitude'] = pj_ch_wgs[:,0]
            df['Longitude'] = pj_ch_wgs[:,1]
            
        except:            
            df = pd.read_csv(path_join, header = 0, sep="/") 
            df.columns = df.columns.str.strip()     
            pj_ch_wgs = ch_LV95_nach_WGS84.transform(df.rw, df.hw)
            pj_ch_wgs = np.array(pj_ch_wgs).T
            df['Latitude'] = pj_ch_wgs[:,0]
            df['Longitude'] = pj_ch_wgs[:,1]
        
        pj_wgs_utm = wgs_nach_utm.transform(df.Latitude, df.Longitude)
        pj_wgs_utm = np.array(pj_wgs_utm).T
        df['X_UTM [m]'] = pj_wgs_utm[:,0]
        df['Y_UTM [m]'] = pj_wgs_utm[:,1]
        df.to_csv(path_join, index=False, sep=",")
     

# %%
