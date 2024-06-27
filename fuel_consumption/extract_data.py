from array import array
import pandas as pd

def extract_fuel_price(df : pd.DataFrame, param: array):
    ret_dict = dict()
    for para in param:
        ret_dict[para] = df[para][0]
    return ret_dict

def extract_auto_data(df : pd.DataFrame, param : dict, cols : array):
    '''
        df: a Dataframe which contains the encoded data of fuel consumption
        param: a dictionary which contains the conditional values for some columns
        cols: an array which contains the name of columns to get the data from  
    '''
    for para in param.keys():
        df = df[df[para].isin(param[para])]
    return df[cols].drop_duplicates()

filename="cleanedDB_encoded.csv"
param = {
    'manufacturer_code':[2],
    'model_code' : [9],
}
cols = ['year', 'year_code']

param2 = {'manufacturer_code': [4]}
cols2 = ['model', 'model_code']
auto_df = pd.read_csv(filename)
ret_df = extract_auto_data(auto_df, param2, cols2)
print(ret_df)


filename = 'fuel_prices_db.csv'
fuels_types_to_extract = ['gasoline']
fuel_df = pd.read_csv(filename)
print(extract_fuel_price(fuel_df, fuels_types_to_extract))