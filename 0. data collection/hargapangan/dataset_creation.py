import os
import glob
from datetime import datetime
import pandas as pd
import numpy as np
from hargapangan_utils import load_xls, get_latest_file, save_json

BASE_DIRECTORY = 'C:\\Users\\WINDOWS 10\\Downloads\\hargapangan\\raw'
DESTINATION = 'C:\\Users\\WINDOWS 10\\Downloads\\hargapangan\\clean'
CENTRAL_DIR = 'C:\\Users\\WINDOWS 10\\Downloads\\hargapangan\\central'
JSON_DIR = 'C:\\Users\\WINDOWS 10\\Downloads\\hargapangan\\JSON'

#def get_commodity_column(excel_file):
temp_file = 'C:\\Users\WINDOWS 10\\bangkit_capstone\\Selasar-MachineLearning\\Kota Bogor-2022-05-26.xlsx'

def create_initial_spreadsheet(base_dir=BASE_DIRECTORY, base_file=temp_file, destination=CENTRAL_DIR):
    for city in os.listdir(base_dir):
        city_dir = os.path.join(destination, city)
        os.makedirs(city_dir, exist_ok=True)

        base_excel = pd.read_excel(temp_file)
        new_excel = base_excel[['No.', 'Komoditas(Rp)']].copy()
        file_path = os.path.join(city_dir, '{}.xlsx'.format(city))
        new_excel.to_excel(file_path, index=False)
        

def process_raw_excel(base_directory=BASE_DIRECTORY, destination=DESTINATION):
    for city in os.listdir(BASE_DIRECTORY):
        city_dir = os.path.join(BASE_DIRECTORY, city)

        file_name, date_created = get_latest_file(city_dir)
    
        excel = load_xls(file_name)
        os.makedirs(destination, exist_ok=True)
        new_file_dir = os.path.join(destination, city)
        os.makedirs(new_file_dir, exist_ok=True)
        new_file_name = '{}-{}.xlsx'.format(city, date_created)
        new_file_path = os.path.join(new_file_dir, new_file_name)
        excel.to_excel(new_file_path, index=False)

def dataframe_to_dict(dataframe):
    df = dataframe.copy().drop(['No.'], axis=1).set_index('Komoditas(Rp)')
    df = df.to_dict('index')
    return df

def append_new_price(central_dir=CENTRAL_DIR, clean_dir=DESTINATION):
        central_city_dir = os.path.join(central_dir, city)
        clean_city_dir = os.path.join(clean_dir, city)

        central_file, central_date = get_latest_file(central_city_dir)
        clean_file, clean_date = get_latest_file(clean_city_dir)

        central_excel = pd.read_excel(central_file)
        clean_excel = pd.read_excel(clean_file)
        price_data = clean_excel.copy().drop(['No.', 'Komoditas(Rp)'], axis=1)
        central_excel_new = pd.concat([central_excel, price_data], axis=1)
        central_excel_new.to_excel(central_file, index=False)
        #stack_dataframe(central_excel_new)
        #central_excel_new.to_csv(updated_file_path)

def create_json(central_dir=CENTRAL_DIR, json_dir=JSON_DIR):
    os.makedirs(json_dir, exist_ok=True)
    for i, city in enumerate(os.listdir(central_dir)):
        city_dir = os.path.join(central_dir, city)
        excel_file, date = get_latest_file(city_dir)
        df = pd.read_excel(excel_file)
        df = dataframe_to_dict(df)
        destination = os.path.join(json_dir, '{}.json'.format(city))
        save_json(destination, df)
        
#create_initial_spreadsheet()
#process_raw_excel()
#append_new_price()
#df = pd.read_excel('C:\\Users\\WINDOWS 10\\Downloads\\hargapangan\\central\\Kota Bekasi\\Kota Bekasi.xlsx')
#stack_dataframe(df)

create_json()