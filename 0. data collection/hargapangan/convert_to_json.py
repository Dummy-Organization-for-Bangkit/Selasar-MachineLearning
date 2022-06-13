import pandas as pd
import os
import json

def excel_to_json(excel_file):
    file_name = excel_file.split('/')[-1]
    region = file_name.split('.')[0]
    df = pd.read_excel(excel_file)
    df = df.drop('Unnamed: 0', axis=1).set_index('Komoditas(Rp)')
    df_json = df.copy().drop('No.', axis=1)
    
    price_array = {
    'komoditas': []
    }
    
    for i, index in enumerate(df.index):
        data = {
            'name': index,
            'average': True if type(df.iloc[i]['No.']) is str else False,
            'price_list': []
        }
        for date in df_json.iloc[i].index:
            desc = {
                'date': date,
                'price': int(df_json.iloc[i][date])
            }
            data['price_list'].append(desc)
        price_array['komoditas'].append(data)
    
    
    return price_array, region

def save_price(excel_file, destination):
    price_array, region = excel_to_json(excel_file)
    json_file_path = os.path.join(destination, f'{region}.json')
    
    with open(json_file_path, 'w') as f:
        json.dump(price_array, f, indent=2)
        f.close()
        
def process_files(source, destination):
    for excel_file in os.listdir(source):
        os.makedirs(destination, exist_ok=True)
        if excel_file.endswith('.xlsx'):
            excel_file = os.path.join(source, excel_file)
            save_price(excel_file, destination)