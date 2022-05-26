import os
import glob
import xlrd
import pandas as pd
from datetime import datetime
import csv
import json


def load_xls(xls_path):
    workbook = xlrd.open_workbook(xls_path, ignore_workbook_corruption=True)
    excel = pd.read_excel(workbook, skiprows=range(8))
    return excel

def get_latest_file(directory):
    list_of_files = glob.glob(os.path.join(directory, '*')) # * means all if need specific format then *.csv
    latest_file_name = max(list_of_files, key=os.path.getctime)
    time_created = os.path.getctime(latest_file_name)
    date_created = datetime.fromtimestamp(time_created).strftime('%Y-%m-%d')

    return latest_file_name, date_created

def save_json(file_path, data):
    with open(file_path, 'w') as fp:
        json.dump(data, fp)
