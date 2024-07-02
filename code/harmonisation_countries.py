import csv
from os import walk
import os
import pandas as pd
from pprint import pprint
import numpy as np
import pickle
from functools import partial
import unidecode
import string
import multiprocessing

pd.options.mode.chained_assignment = None  # default='warn'
global dem_counter
dem_counter = 0


# get the path for the data folder and the code folder (the code folder is the current directory)
# need to have two folders: one for the code and one for the data

current_dir = os.getcwd()
path_code = current_dir
path_data = '/'.join(current_dir.split('/')[:-1]+['data'])+'/'


def get_country(df_input):
    # function to remove punctuation
    translating = str.maketrans('', '', string.punctuation)

    # Load the data bases countaining all the cities, coutries, regions of the world:

    # all the coutries of the world
    df_countries = pd.read_csv(path_data+'/geonames_2022jun_dbo_country.csv', sep = ';')

    # all the regions of the world
    # ####### Regions
    df_admin1 = pd.read_csv(path_data+'/geonames_2022jun_dbo_state_admin1.csv', sep = ';')
    # all the departments of the world

    # ####### Districts
    df_admin2 = pd.read_csv(path_data+'/geonames_2022jun_dbo_state_admin2.csv', sep = ';')


    # all the cities of the world
    # citation: https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/table/?disjunctive.cou_name_en&sort=name
    df_cities = pd.read_csv(path_data+'/geonames-all-cities-with-a-population-1000.csv', sep = ';')

    # Load the data base of all the different notations for the countries (exemple: USA, the United States ...)
    # citation: https://github.com/aaronschiff/country-names
    df_correspondance_country = pd.read_csv(path_data+'/country-names-cross-ref.csv', sep = ',', names=['complex_name', 'standard_name'])

    df_demonyms_country = pd.read_csv(path_data+'/demonyms_v2.csv', sep = ';')

    # Load the data base of correspondance of the codes of the coutries (real names - 2 letters code - 3 letters code)
    # citation: https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes/blob/master/all/all.csv
    df_country_code = pd.read_csv(path_data+'/countries.csv', sep = ',')

    # creation of the lists of all possible coutries, cities, regions... with lower letters (to make it easy to compare) not punctuation
    list_countries = [unidecode.unidecode(k.lower()).translate(translating) for k in list(df_countries['name'])]
    list_admin1 = [unidecode.unidecode(k.lower()).translate(translating) for k in list(df_admin1['admin1_ascii_name'])]
    list_admin2 = [unidecode.unidecode(k.lower()).translate(translating) for k in list(df_admin2['admin2_ascii_name'])]
    list_cities = [unidecode.unidecode(k.lower()).translate(translating) if type(k) == str else np.nan for k in list(df_cities['ASCII Name'])]
    list_continents = ['asia', 'africa', 'europe', 'north america', 'south america', 'oceania', 'antartica']

    # creation of the list of all possible names of countries
    list_correspondance_country = [unidecode.unidecode(k.lower()).translate(translating) for k in list(df_correspondance_country['complex_name'])]

    # creation of list based on the demonyms file
    list_demo_country = [unidecode.unidecode(k.lower()).translate(translating) for k in list(df_demonyms_country['Demonym'])]


    # list of all possible countries' code
    list_codes = [unidecode.unidecode(k.lower()).translate(translating) if type(k) == str else k for k in list(df_countries['country_iso2_code'])]

    # cretion of the list of the coutries and type of locations
    list_clean_country = []
    list_type_location = []
    last_progress = 0
    # for every location of the data base
    for k in range(0, len(df_input)):

        if k % 100 == 0:
            progress = int(100*k/len(df_input))
            if progress % 5 ==0 and last_progress != progress:
                last_progress = progress
                print('{0} of {1} words encountered ({2}%)'.format(k, len(df_input), progress))

        x = df_input.iloc[k] # this is the raw corresponding to the location

        if (type(x.text)!=str) : # if the text of the location is not a string, we put a nan as the corresponding coutry
            clean_country = np.nan
            type_location = np.nan

        else:
            # we write the location in lower case without punctuation, for comparison
            raw_country = unidecode.unidecode(x.text.lower()).translate(translating)

            # if it is a country with the official name
            if (raw_country in list_countries):
                clean_country = df_countries.iloc[list_countries.index(raw_country)]['country_iso2_code']
                type_location = 'country'
            # otherwise we look if it is a country without the official name
            elif (raw_country in list_correspondance_country):
                official_name = df_correspondance_country.iloc[list_correspondance_country.index(raw_country)]['standard_name']

                ###### TODO: use the official name without changing it?
                if ',' in official_name: # this happens when it's written as 'Congo, the republic of', we keep 'congo'
                    official_name = official_name.split(',')[0]

                official_name = unidecode.unidecode(official_name.lower()).translate(translating)

                if (official_name in list_countries):
                    clean_country = df_countries.iloc[list_countries.index(official_name)]['country_iso2_code']
                    type_location = 'correnspondace_country'
                else:
                    clean_country = np.nan
                    type_location = np.nan
            # otherwise we look if it is a region admin1
            elif (raw_country in list_admin1):
                clean_country = df_admin1.iloc[list_admin1.index(raw_country)]['admin1_code'][:2]
                type_location = 'admin1'
            # otherwise we look if it is a district admin2
            elif (raw_country in list_admin2):
                clean_country = df_admin2.iloc[list_admin2.index(raw_country)]['admin2_code'][:2]
                type_location = 'admin2'

            # otherwise we look if it is a city
            elif (raw_country in list_cities):
                clean_country = df_cities.iloc[list_cities.index(raw_country)]['Country Code']
                type_location = 'city'

            # otherwise we look if it is already a code
            elif (raw_country in list_codes):
                clean_country = raw_country.upper()
                type_location = 'code'
            # if the country is hidden in a sentence, we cut it through the spaces and look at each word
            elif (len(raw_country.split(' '))>1):
                clean_country = 0
                for word in raw_country.split(' '):
                    if (len(word)!=0):
                        if (word in list_countries):
                            clean_country = df_countries.iloc[list_countries.index(word)]['country_iso2_code']
                            type_location = 'country'
                        elif (word in list_correspondance_country):
                            official_name = df_correspondance_country.iloc[list_correspondance_country.index(word)]['standard_name']
                            if ',' in official_name: # this happens when it's written as 'Congo, the republic of'
                                official_name = official_name.split(',')[0]
                            official_name = unidecode.unidecode(official_name.lower()).translate(translating)
                            if (official_name in list_countries):
                                clean_country = df_countries.iloc[list_countries.index(official_name)]['country_iso2_code']
                                type_location = 'country'
                            else:
                                clean_country = np.nan
                                type_location = np.nan
                        elif (word in list_admin1):
                            clean_country = df_admin1.iloc[list_admin1.index(word)]['admin1_code'][:2]
                            type_location = 'admin1'
                        elif (word in list_admin2):
                            clean_country = df_admin2.iloc[list_admin2.index(word)]['admin2_code'][:2]
                            type_location = 'admin2'
                        elif (word in list_cities):
                            clean_country = df_cities.iloc[list_cities.index(word)]['Country Code']
                            type_location = 'city'
                        elif (word in list_codes):
                            clean_country = word.upper()
                            type_location = 'code'
                        elif (word in list_continents):
                            clean_country = word
                            type_location = 'continent'
                    if (clean_country == 0):
                        clean_country = np.nan
                        type_location = np.nan

            # if we don't find any country, we look for a continent
            elif (raw_country in list_continents):
                clean_country = raw_country
                type_location = 'continent'
            # NEW: lets see if it is a demonym
            elif (raw_country in list_demo_country):
                # lookup from demonym country name to ISO country code
                official_name = df_demonyms_country.iloc[list_demo_country.index(raw_country)]['Country']
                ##### TODO: use the official name without changing it?
                if ',' in official_name: # this happens when it's written as 'Congo, the republic of', we keep 'congo'
                    official_name = official_name.split(',')[0]

                official_name = unidecode.unidecode(official_name.lower()).translate(translating)
                #print('     raw: {0}  match: {1}'.format(raw_country, official_name))
                global dem_counter 
                dem_counter +=  1
                if (official_name in list_countries):
                    clean_country = df_countries.iloc[list_countries.index(official_name)]['country_iso2_code']
                    type_location = 'demonym'
                else:
                    print('    Encountered raw: {0}  match: {1} but not no ISO-2 code'.format(raw_country, official_name))
                    clean_country = np.nan
                    type_location = 'demonym'


            else:
                clean_country = np.nan # I think those locations should be explored
                type_location = np.nan

        list_clean_country.append(clean_country)
        list_type_location.append(type_location)
        if len(list_clean_country) != len(list_type_location):
            print("Danger!")

    df_input['country'] = list_clean_country
    df_input['type_location'] = list_type_location
    print('######### File finished. Encountered {0} demonyms.'.format(dem_counter))
    return(df_input)


def from_list_location_to_list_publication(df):

    # get the list of publications
    list_publications = list(set(list(df['abstract_id'])))
    list_publications.sort()

    list_countries = []

    # for every publication
    for pub in list_publications:

        # get the data relative to the publication and remove the nan values
        df_pub = df[(df['abstract_id'] == pub) & (df['type_location']!='continent')]
        df_pub = df_pub.dropna(subset=['country'])

        # extract the countries of the pub
        list_countries_pub= list(set(list(df_pub['country'])))

        list_countries.append(list_countries_pub)

    df_output = pd.DataFrame(list(zip(list_publications, list_countries)),columns =['abstract_id', 'country'])

    return(df_output)

def process_file(k):
    file_number = k + 1  # Adjust indexing to start at 1
    # Load the database


    ################### Reading input files ###################

    # TODO: NEW INPUT REQUIRED HERE
    df_input = pd.read_csv(path_data + 'new_NER_input/output_part_' + str(file_number) + '.csv', sep=',')
    print('####   File {0}'.format(file_number))
    # Make the column 'country'
    df_output = get_country(df_input)
    df_output2 = df_output.copy()

    # Save the detailed table to disk
    #output_file_path_1 = path_data + 'output_small_pipeline/output_with_country_detailed_part_' + str(file_number) + '.csv'
    #df_output.to_csv(output_file_path_1, sep=',', mode='w')
    #print('####   Written output file 1 for file {0}'.format(file_number))
    # Sort by publication
    ## TODO:       !!!!!!!!!!!     Function above is buggy    !!!!!!!!!



    ################### Writing output files ###################

    df_output2 = from_list_location_to_list_publication(df_output2)
    output_file_path_2 = path_data + 'latest_output/output_with_country_part_' + str(file_number) + '.csv'
    df_output2.to_csv(output_file_path_2, sep=',', mode='w')
    print('####   Written output file for file {0}'.format(file_number))



if __name__ == '__main__':
    # to test with a single file(output_part_1.csv)
    #process_file(0)

    processes = 4
    no_of_files = 36

    chunk_size = no_of_files // processes
    chunks = [i for i in range(0, no_of_files)]
    print("working…")

    pool = multiprocessing.Pool(processes=processes)
    pool.map_async(process_file, chunks, chunksize=chunk_size)
    pool.close()
    pool.join()
