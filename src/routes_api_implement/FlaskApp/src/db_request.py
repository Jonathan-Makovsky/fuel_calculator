import pandas as pd

class DB_Requests:
    # CHABGE PATH - NOT WORKING IN GENERAL PATH
    def __init__(self, cars_db_path='C:\\Users\\liadi\\Documents\\all-grades-shortest-path\\routes_api_implement\\FlaskApp\\static\\db\\cleanedDB_encoded.csv', prices_db_path='C:\\Users\\liadi\\Documents\\all-grades-shortest-path\\routes_api_implement\\FlaskApp\\static\\db\\fuel_prices_db.csv'):
        self.cars_db = pd.read_csv(cars_db_path)
        self.prices_db = pd.read_csv(prices_db_path)
    
    def extract_auto_data(self, df : pd.DataFrame, param : dict, cols):
        '''
            df: a Dataframe which contains the encoded data of fuel consumption
            param: a dictionary which contains the conditional values for some columns
            cols: an array which contains the name of columns to get the data from  
        '''
        for para in param.keys():
            df = df[df[para].isin(param[para])]
        return df[cols].drop_duplicates()
    
    def car_request(self, request : dict):
        cols = request['cols']
        param = dict()
        for key in request.keys():
            if key != 'cols':
                param[key] = request[key]
        
        ext_df = self.extract_auto_data(self.cars_db, param, cols)

        # make the return extract data to be dictinary from dataframe object
        rsp = ''
        if len(cols) == 2:
            # next car's property request
            rsp = ext_df.set_index(cols[1]).to_dict()[cols[0]]
        elif len(cols) == 1:
            # get avrage consumption
            rsp = ext_df[cols[0]].iloc[0]
        
        return rsp

    def fuelPrice_request(self,  fuel_type):
        return self.extract_fuel_price(self.prices_db, fuel_type)


    def extract_fuel_price(self, df : pd.DataFrame, fuel_type):
        #ret_dict = dict()
        #for para in param:
        #    ret_dict[para] = df[para][0]
        return df[fuel_type][0]
