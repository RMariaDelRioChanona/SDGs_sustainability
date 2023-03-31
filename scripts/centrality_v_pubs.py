import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from scipy.stats.stats import pearsonr

# Import network and publication data

cntry_cntry_nw = pd.read_csv("cntry_cntry_nw.csv", index_col = [0])
cntry_cntry_nw = cntry_cntry_nw[cntry_cntry_nw["geographical_subdivision"]!="continent"]

cntry_total_pubs_df = pd.read_csv("cntry_total_pubs.csv", index_col = [0]) # import country publication counts

# Create the network of affiliations and countries of study

cntry_cntry = nx.MultiGraph()

cntry_cntry.add_nodes_from(cntry_cntry_nw["country_author"], bipartite=0)
cntry_cntry.add_nodes_from(cntry_cntry_nw["country_studied"], bipartite=1)

cntry_cntry.add_edges_from(cntry_cntry_nw[["country_author","country_studied"]].to_numpy())

cntry_cntry_w = nx.Graph()
for u,v,data in cntry_cntry.edges(data=True):
    w = data['weight'] if 'weight' in data else 1.0
    if cntry_cntry_w.has_edge(u,v):
        cntry_cntry_w[u][v]['weight'] += w
    else:
        cntry_cntry_w.add_edge(u, v, weight=w)


# Get eigenvector centralities of nodes

centrality_eig = nx.eigenvector_centrality(cntry_cntry_w)
centrality_eig_df = pd.DataFrame(centrality_eig.items(), columns=['node_id', 'eig_v_centrality'])


# Merge df on centrality measures and publication counts

cntry_total_pubs_df = pd.merge(centrality_eig_df, cntry_total_pubs_df)

# Get correlations between measures

np.corrcoef(cntry_total_pubs_df["pub_count"], cntry_total_pubs_df["eig_v_centrality"])

pearsonr(cntry_total_pubs_df["pub_count"], cntry_total_pubs_df["eig_v_centrality"]) # corr not significant
