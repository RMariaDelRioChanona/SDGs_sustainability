import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pub_meta = pd.read_csv('publication_metadata.txt', sep='\t', header=None,
                       names=["pub_id", "title", "pub_year", "pub_type_id", "pub_type", "source_id", "source_title", "n_cites"])

pub_author_org = pd.read_csv('pub_author_organization.txt', sep='\t', header=None,
                            names=["pub_id", "researcher_id", "organization_id"])

org_geo = pd.read_csv('organization_geo_names.txt', sep='\t', header=None,
                      names=["organization_id", "organization_name", "country_code", "geonames_city_id", "latitude", "longitude"])

pub_field = pd.read_csv('pub_for_field.txt', sep='\t', header=None,
                        names=["pub_id", "two_digit_field_id", "two_digit_field_label"])

full_df = pd.merge(pub_meta[["pub_id","n_cites"]], pub_author_org, on=["pub_id"])
full_df = pd.merge(full_df, org_geo[["country_code","organization_id"]], on=["organization_id"])
full_df = pd.merge(full_df, pub_field[["pub_id","two_digit_field_id"]], on=["pub_id"])


## Country statistics

cntry_df = full_df[~full_df["country_code"].isnull()] # for this analysis, keep publications that have country affiliations

# Plot total number of publications per country
cntry_total_pubs = cntry_df.groupby('country_code')['pub_id'].count()
cntry_total_pubs = cntry_total_pubs.sort_values(ascending=False)
# plot a bar chart of the result
cntry_total_pubs.plot(kind='bar', figsize=(26,8))
# set the chart title and axis labels
plt.title('Total publications per country')
plt.xlabel('Country')
plt.xticks(fontsize=6, rotation='vertical')
plt.ylabel('total publications')
plt.savefig("total_publications_cntry.png" ,bbox_inches='tight')
plt.show()

# Plot total number of researchers per country
cntry_total_researchers = cntry_df.groupby('country_code')['researcher_id'].count()
cntry_total_researchers = cntry_total_researchers.sort_values(ascending=False)
# plot a bar chart of the result
cntry_total_researchers.plot(kind='bar', figsize=(26,8))
# set the chart title and axis labels
plt.title('Total researchers per country')
plt.xlabel('Country')
plt.xticks(fontsize=6, rotation='vertical')
plt.ylabel('total researchers')
plt.savefig("total_researchers_cntry.png")
plt.show()

# Plot mean citations per country
cntry_mean_cites = cntry_df.groupby('country_code')['n_cites'].mean()
cntry_mean_cites = cntry_mean_cites.sort_values(ascending=False)
# plot a bar chart of the result
cntry_mean_cites.plot(kind='bar', figsize=(26,8))
# set the chart title and axis labels
plt.title('Mean citations per paper')
plt.xlabel('Country')
plt.xticks(fontsize=6, rotation='vertical')
plt.ylabel('mean citations')
plt.savefig("mean_citations_cntry.png")
plt.show()

# Plot total citations per country
cntry_total_cites = cntry_df.groupby('country_code')['n_cites'].sum()
cntry_total_cites = cntry_total_cites.sort_values(ascending=False)
# plot a bar chart of the result
cntry_total_cites.plot(kind='bar', figsize=(26,8))
# set the chart title and axis labels
plt.title('Total citations')
plt.xlabel('Country')
plt.xticks(fontsize=6, rotation='vertical')
plt.ylabel('total citations')
plt.savefig("total_citations_cntry.png")
plt.show()


## Publication field statistics

field_df = full_df[~full_df["two_digit_field_id"].isnull()] # for this analysis, keep publications that have field info

# Plot total number of publications per country
field_total_pubs = field_df.groupby('two_digit_field_id')['pub_id'].count()
field_total_pubs = field_total_pubs.sort_values(ascending=False)
# plot a bar chart of the result
field_total_pubs.plot(kind='bar', figsize=(26,8))
# set the chart title and axis labels
plt.title('Total publications per field')
plt.xlabel('Field')
plt.xticks(fontsize=6, rotation='vertical')
plt.ylabel('total publications')
plt.savefig("total_publications_field.png")
plt.show()

# Plot total number of researchers per country
field_total_researchers = field_df.groupby('two_digit_field_id')['researcher_id'].count()
field_total_researchers = field_total_researchers.sort_values(ascending=False)
# plot a bar chart of the result
field_total_researchers.plot(kind='bar', figsize=(26,8))
# set the chart title and axis labels
plt.title('Total researchers per field')
plt.xlabel('Field')
plt.xticks(fontsize=6, rotation='vertical')
plt.ylabel('total researchers')
plt.savefig("total_researchers_field.png")
plt.show()

# Plot mean citations per country
field_mean_cites = field_df.groupby('two_digit_field_id')['n_cites'].mean()
field_mean_cites = field_mean_cites.sort_values(ascending=False)
# plot a bar chart of the result
field_mean_cites.plot(kind='bar', figsize=(26,8))
# set the chart title and axis labels
plt.title('Mean citations per paper')
plt.xlabel('Field')
plt.xticks(fontsize=6, rotation='vertical')
plt.ylabel('mean citations')
plt.savefig("mean_citations_field.png")
plt.show()

# Plot total citations per country
field_total_cites = field_df.groupby('two_digit_field_id')['n_cites'].sum()
field_total_cites = field_total_cites.sort_values(ascending=False)
# plot a bar chart of the result
field_total_cites.plot(kind='bar', figsize=(26,8))
# set the chart title and axis labels
plt.title('Total citations')
plt.xlabel('Field')
plt.xticks(fontsize=6, rotation='vertical')
plt.ylabel('total citations')
plt.savefig("total_citations_field.png")
plt.show()
