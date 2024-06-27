import pandas as pd
import numpy as np

def clean_data_frame(auto_df: pd.DataFrame):
    num_of_rows=auto_df.shape[0]
    num_of_column=auto_df.shape[1]
    for i in range(num_of_rows):
        y = auto_df["year"][i]
        auto_df["year"][i]= 0 if '-' in y else y


    engine_type_list = ['בנזין','היברידי', 'בנזין היברידי']
    for i in range(num_of_rows):
        y = auto_df["engine_type"][i]
        auto_df["engine_type"][i] = y if y in engine_type_list else 0

    for i in range(num_of_rows):
        y = auto_df['test_consumption'][i]
        x=''
        for char in y:
            if char.isnumeric() or char=='.':
                x+=char
        
        if x == '':
            auto_df['test_consumption'][i] = 0
        else:
            auto_df['test_consumption'][i]=x

    for i in range(num_of_rows):
        y = auto_df['factory_consumption'][i]
        x = ''
        for char in y:
            if char.isnumeric() or char == '.':
                x += char
        if x == '':
            auto_df['factory_consumption'][i] = 0
        else:
            auto_df['factory_consumption'][i] = x


    ## filtering the DB
    auto_df.drop(auto_df[auto_df['year']==0].index, inplace=True)
    auto_df.drop(auto_df[auto_df['engine_type']==0].index, inplace=True)
    auto_df.drop(auto_df[(auto_df['test_consumption']==0) & (auto_df['factory_consumption']==0)].index, inplace=True)
    num_of_rows=auto_df.shape[0]

    ## computing consumption average
    test_fact_average=[]
    auto_df.reset_index(inplace=True)

    for i in range(num_of_rows):
        y = float(auto_df['test_consumption'][i])
        x = float(auto_df['factory_consumption'][i])

        if x!=0 and y!=0:
            test_fact_average.append((x+y)/2)
        else:
            test_fact_average.append(max(x,y))
    auto_df['average_consumption']=test_fact_average
    return auto_df

def encode_data_frame(df : pd.DataFrame):
    num_of_rows = df.shape[0]
    num_of_bits = [7, 4, 5, 2, 2]
    columns = df.columns
    i = 0
    for i in range(columns.shape[0] - 3):
        new_col = df.groupby(columns[i], sort=False).ngroup() + 1
        df.insert(2*i + 1, columns[i]+'_code', new_col)

    return df

# Clean Data Procedure
filename="autocom_full_data.csv"
auto_df=pd.read_csv(filename)
newdf = clean_data_frame(auto_df)
newdf.drop(columns='index', inplace=True)
newdf.to_csv('cleanedDB.csv', index=False, encoding='utf-8-sig')

# Encoding procedure
filename="cleanedDB.csv"
auto_df=pd.read_csv(filename)
newdf = encode_data_frame(auto_df)
newdf.to_csv('cleanedDB_encoded.csv', index=False, encoding='utf-8-sig')
