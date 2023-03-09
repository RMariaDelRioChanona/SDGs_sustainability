import numpy as np 
import pandas as pd
import sqlite3 
import matplotlib.pyplot as plt

data_meta_path = '../../SDGs Metadata/'
data_country_path = "../../Publications with Countries (Small Pipeline)/"
file_metadata = "publication_metadata.txt"
file_sdg = "named_entities_sm_test.db"
path_export_fig = "../results/fig/"


file_root = 'output_with_country_part_'
# NOTE ask Elsa about rest of the files
n_files = 23


df = pd.read_csv(data_country_path + file_root + str(1) + '.csv')
df = df[df['geographical_subdivision'].notna()]
for i in range(2,n_files + 1):
    print(i)
    df_ = pd.read_csv(data_country_path + file_root + str(i) + '.csv')
    df_ = df_[df_['geographical_subdivision'].notna()]
    df = pd.concat([df, df_])

df.to_csv(data_meta_path + "output_with_country_nonna_merge.csv")

len(df)