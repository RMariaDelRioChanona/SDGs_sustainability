import pandas as pd

cntry_of_study = pd.read_csv("cntry_cntry_nw.csv", index_col = [0])
cntry_of_study = cntry_of_study[cntry_of_study["geographical_subdivision"]!="continent"]

import networkx as nx

# Create the bipartite network of affiliations and countries of study

cntry_cntry = nx.MultiGraph() # make sure the graph has weights

# Add nodes with the node attribute "bipartite"
cntry_cntry.add_nodes_from(cntry_of_study["country_author"], bipartite=0)
cntry_cntry.add_nodes_from(cntry_of_study["country_studied"], bipartite=1)

# Add edges only between nodes of opposite node sets
cntry_cntry.add_edges_from(cntry_of_study[["country_author","country_studied"]].to_numpy())

# Create graph
cntry_cntry_w = nx.Graph()
for u,v,data in cntry_cntry.edges(data=True):
    w = data['weight'] if 'weight' in data else 1.0
    if cntry_cntry_w.has_edge(u,v):
        cntry_cntry_w[u][v]['weight'] += w
    else:
        cntry_cntry_w.add_edge(u, v, weight=w)


# Get communities
import networkx.algorithms.community as nx_comm
from networkx.algorithms.community.centrality import girvan_newman

comms_louv = nx_comm.louvain_communities(cntry_cntry_w, seed=123)
