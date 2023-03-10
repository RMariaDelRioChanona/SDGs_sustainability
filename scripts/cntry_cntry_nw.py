import pandas as pd
import networkx as nx

# Read in files

cntry_of_study = pd.read_csv("output_with_country_nonna_merge.csv", usecols = [2,3,4]) # only read in cols with relevant info
pub_author_org = pd.read_csv('pub_author_organization.txt', sep='\t', header=None,
                             names=["pub_id", "researcher_id", "organization_id"])
org_geo = pd.read_csv('organization_geo_names.txt', sep='\t', header=None,
                     names=["organization_id", "organization_name", "country_code", "geonames_city_id", "latitude", "longitude"])


def cntry_to_cntry_nw_creator(cntry_of_study, pub_author_org, org_geo):

    # Adjust and merge dataframes to end up with a network
    pub_author_org = pub_author_org[pub_author_org['researcher_id'].notna() & pub_author_org['organization_id'].notna()] # exclude rows with missing author or org ID    
    pub_author_org = pub_author_org[pub_author_org["pub_id"].isin(cntry_of_study["abstract_id"])][["pub_id","organization_id"]]
    cntry_of_study = cntry_of_study.rename(columns={"abstract_id": "pub_id"})
    cntry_of_study = pd.merge(cntry_of_study, pub_author_org, on=["pub_id"])
    org_geo = org_geo[org_geo["organization_id"].isin(cntry_of_study["organization_id"])][["organization_id","country_code"]]

    cntry_of_study = pd.merge(cntry_of_study, org_geo, on=["organization_id"])
    cntry_of_study = cntry_of_study[["pub_id","country_code","location","geographical_subdivision"]]
    cntry_of_study = cntry_of_study.rename(columns={"country_code": "country_author", "location": "country_studied"})
    cntry_of_study = cntry_of_study.apply(lambda x: x.str.split(',').explode())
    cntry_of_study['country_studied'] =  cntry_of_study['country_studied'].apply(lambda x: x.replace('[','').replace(']','').replace("'",''))

    cntry_of_study.to_csv("cntry_cntry_nw.csv") # save file


    # Create the bipartite network of affiliations and countries of study

    cntry_cntry = nx.MultiGraph() # make sure the graph has weights

    # Add nodes with the node attribute "bipartite"
    cntry_cntry.add_nodes_from(cntry_of_study["country_author"], bipartite=0)
    cntry_cntry.add_nodes_from(cntry_of_study["country_studied"], bipartite=1)

    # Add edges only between nodes of opposite node sets
    cntry_cntry.add_edges_from(cntry_of_study[["country_author","country_studied"]].to_numpy())

    cntry_cntry_w = nx.Graph()
    for u,v,data in cntry_cntry.edges(data=True):
        w = data['weight'] if 'weight' in data else 1.0
        if cntry_cntry_w.has_edge(u,v):
            cntry_cntry_w[u][v]['weight'] += w
        else:
            cntry_cntry_w.add_edge(u, v, weight=w)

    return(cntry_cntry_w.edges(data=True))

cntry_to_cntry_nw_creator(cntry_of_study, pub_author_org, org_geo)
