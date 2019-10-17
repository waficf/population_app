import json
import requests
import os

import numpy as np
import pandas as pd

def api_query(indicator_code, params):
    link = 'https://api.worldbank.org/v2/countries/all/indicators/'
    indicator = link + indicator_code

    r= requests.get(indicator, params=params)
    return r.json()



def full_query(indicator_code, params):
    pages = api_query(indicator_code, params)[0]['pages']
    data = pd.DataFrame()
    
    folder_name = '/Users/wafic/Documents/population_app/Data' 
    
    for page in range(pages):
        file_name = indicator_code+'_'+str(page)+'.txt'
        file_path = os.path.join(folder_name, file_name)
        params['page'] = page+1
        
        
        data_chunks = api_query(indicator_code, params)
        with open(file_path, 'w') as file:
            json.dump(data_chunks, file)



def extract_data(folder_name):
    df_list = []

    for file in os.listdir(folder_name):
        
        if file.endswith('.txt'):
            
            try: 
                file_name = os.path.join(folder_name, file)

                with open(file_name) as json_file:
                    data = json.load(json_file)
                    for entry in data[1]:
                        df_list.append({
                            'country': entry['country']['value'],
                            'code': entry['country']['id'],
                            'year': entry['date'],
                            'value': entry['value']
#                             'indic':entry['indicator']['id']
                        })
            except:
                continue
                

    df = pd.DataFrame(df_list, columns=['country', 'code', 'year', 'value'])
    return df


def country_data(df):
	country_code = pd.read_csv('/Users/wafic/Documents/population_app/Data/country_map.txt', sep='\t', dtype={'3let':str, '2let':str})
	country_pop = df.merge(country_code, left_on='code', right_on='2let')
	return country_pop


def income_classification(df):
    # This takes advantage of the calssifications available in the extracted data
    wb_class = df[(df.country.str.contains('income')) & ~(df.country.str.contains('excluding'))].country.unique().tolist()

    income_df = df[df.country.isin(wb_class)] 
    return income_df
