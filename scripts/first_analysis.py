import numpy as np 
import pandas as pd
import sqlite3 
import matplotlib.pyplot as plt

data_meta_path = '../../SDGs Metadata/'
data_country_path = "../../Publications with Countries (Small Pipeline)/"
file_metadata = "publication_metadata.txt"
file_sdg = "named_entities_sm_test.db"
path_export_fig = "../results/fig/"

# read dataframe from sql
cnx = sqlite3.connect(data_country_path + file_sdg)
df_study = pd.read_sql_query("SELECT * FROM named_entities", cnx)
cnx.close()

# getting SDG from each publication
dict_pub_sdg = dict(zip(df_study['pub_id'], df_study['category']))
# getting the list of sdgs
sdg_list = df_study['category'].unique().tolist()

df_meta = pd.read_csv(data_path + file_metadata, sep= "\t"\
    ,header=None)

df_meta.columns = ['pub_id', 'title', 'pub_year', 'pub_type_id', 'pub_type', 
              'source_id', 'source_title', 'n_cites']

npub_study = len(df_study['pub_id'].unique())
npub_meta = len(df_meta['pub_id'].unique())
print("number of pubs in named_entity_df {}, in metadata {}"\
    .format(npub_study, npub_meta ))

# drop nan's
df_meta = df_meta[df_meta['category'].notna()]


# Plot mean citations per SDG
sdg_mean_cites = df_meta.groupby('category')['n_cites'].mean()
sdg_mean_cites = sdg_mean_cites.sort_values(ascending=False)
# plot a bar chart of the result
sdg_mean_cites.plot(kind='bar')
# set the chart title and axis labels
plt.title('Mean citations per paper')
plt.xlabel('SDG')
plt.ylabel('mean citations')
plt.savefig(path_export_fig + "mean_citations_sdg.png")
plt.show()

# Plot total citations per SDG
sdg_total_cites = df_meta.groupby('category')['n_cites'].sum()
sdg_total_cites = sdg_total_cites.sort_values(ascending=False)
# plot a bar chart of the result
sdg_total_cites.plot(kind='bar')
# set the chart title and axis labels
plt.title('Total citations per paper')
plt.xlabel('SDG')
plt.ylabel('Total citations')
plt.savefig(path_export_fig + "total_citations_sdg.png")
plt.show()

# Plot total citations per SDG
sdg_total_papers = df_meta.groupby('category').size()
sdg_total_papers = sdg_total_papers.sort_values(ascending=False)
# plot a bar chart of the result
sdg_total_papers.plot(kind='bar')
# set the chart title and axis labels
plt.title('Total citations per paper')
plt.xlabel('SDG')
plt.ylabel('Total citations')
plt.savefig(path_export_fig + "total_paper_sdg.png")
plt.show()
