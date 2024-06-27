import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

autocom_table_url = 'https://www.autocom.co.il/consumption-table/'
autocom_form_url = 'https://www.autocom.co.il/fuel-consumption/'
def fuel_consumption_create_db():
    return

def create_csvfile_fuel_consump_from_autocom_requests(parameters='', file_name='defualt.csv'):
    csv_data = []

    response = requests.get(autocom_form_url)
    soup = BeautifulSoup(response.text, "lxml")
    select_obj = soup.find_all('select', {'class':'parent_tax'})[0]
    
    manufacturer_name_dict = dict()        # {'id' : 'name'}
    for ele in select_obj.find_all('option')[2:]:
        manufacturer_name_dict[ele['value']] = ele.text.strip()
    
    url_post='https://www.autocom.co.il/wp-admin/admin-ajax.php'
    i = 1
    errors = []

    for manufac in manufacturer_name_dict:
        post_request_data = {'action' : 'lpk_children', 'parent' : manufac}
        response = requests.post(url=url_post, data=post_request_data)
        try:
            models_jsn=response.json()
        except Exception:
            errors.append([manufacturer_name_dict[manufac]])
            continue
        for model in models_jsn:
            post_request_data = {'action': 'lpk_children', 'parent': model['id']}
            response = requests.post(url=url_post, data=post_request_data)
            try:
                year_jsn = response.json()
            except Exception:
                errors.append([manufacturer_name_dict[manufac]+'/'+model['name']])
                continue
            for year_model in year_jsn:
                post_request_data = {'action': 'lpk_children', 'parent': year_model['id']}
                response = requests.post(url=url_post, data=post_request_data)
                try:
                    engineType_jsn = response.json()
                except Exception:
                    errors.append([manufacturer_name_dict[manufac] + '/' + model['name']+'/'+year_model['name']])
                    continue
                for engine in engineType_jsn:
                    post_request_data = {'action': 'lpk_children', 'parent': engine['id']}
                    response = requests.post(url=url_post, data=post_request_data)
                    try:
                        engineVol_jsn = response.json()
                    except Exception:
                        errors.append([manufacturer_name_dict[manufac] + '/' + model['name'] + '/' + year_model['name']+'/'+engine['name']])
                        continue
                    for engineVol in engineVol_jsn:
                        post_request_data = {'action': 'lpk_get_results', 'id': engineVol['id']}
                        #print(post_request_data)
                        response = requests.post(url=url_post, data=post_request_data)
                        try:
                            fuelConsump = response.json()
                        except Exception:
                            errors.append([manufacturer_name_dict[manufac] + '/' + model['name'] + '/' + year_model['name'] + '/' +engine['name']+'/search'])
                            continue
                        #print('Run no.', i, ': ', fuelConsump)
                        factory_lpk = fuelConsump['factory_lpk']
                        test_lpk = fuelConsump['test_lpk']
                        car_data = [manufacturer_name_dict[manufac], model['name'], year_model['name'], engine['name'], engineVol['name'], factory_lpk, test_lpk]
                        csv_data.append(car_data)
                        print(i)
                        #print(car_data)
                        i+=1
                        #if i > k:
                        #    break
                    #if i > k:
                    #    break
                #if i > k:
                #    break
            #if i > k:
            #    break
        #if i > k:
        #    break

    print("END")
    print(csv_data)
    print(errors)
    data_columns = ['manufacturer', 'model', 'year', 'engine_type', 'engine_volume', 'test_consumption', 'factory_consumption']
    df_table = pd.DataFrame(data=np.asarray(csv_data), columns=data_columns)
    df_table.to_csv(file_name, index=False, encoding='utf-8-sig')

    df_table2 = pd.DataFrame(data=np.asarray(errors))
    df_table2.to_csv('errors.csv', index=False, encoding='utf-8-sig')

    
    return

def recursive_request(i, data_dict, post_url):
    if i == 5:
        for ele in data_dict:
            post_request_data = {'action' : 'lpk_get_results', 'id' : ele}
            response = requests.post(url=post_url, data=post_request_data) 
            jsn_rsp = response.json()
    
    for ele in data_dict:
        post_request_data = {'action' : 'lpk_children', 'parent' : ele}
        response = requests.post(url=post_url, data=post_request_data)
        jsn_rsp = response.json()
        new_dict = dict()
        for jsn_ele in jsn_rsp:
            new_dict[jsn_ele['id']] = jsn_ele['name']
        
        return recursive_request(i+1, new_dict, post_url)

def create_csvfile_fuel_consump_from_autocom_table(parameters='', file_name='defualt.csv'):
    response = requests.get(autocom_table_url)
    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find_all('table', {'class':'fuel-tbl'})[0]
    table_body = table.find('tbody')
    data = []
    table_columns = [ele.text.strip() for ele in table.find('thead').find_all('th')]
    
    table_rows = table_body.find_all('tr')
    for row in table_rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    
    df_table = pd.DataFrame(data=np.asarray(data), columns=table_columns)
    df_table.to_csv(file_name, index=False, encoding = 'utf-8-sig')
    
    #print(pd_table)

    return

#create_csvfile_fuel_consump_from_autocom_table(file_name='autocom_table.csv')
#create_csvfile_fuel_consump_from_autocom_requests(file_name='autocom_full_data.csv')
