#!/usr/bin/env python3
import os
import requests
import xlrd
import pandas as pd
from datetime import date, timedelta

def retrieveData():
    regency_list = [
        {
            "name": "Tangerang",
            "pid": 11,
            "rid": 26,
        },
        {
            "name": "Bekasi",
            "pid": 12,
            "rid": 30,
        },
        {
            "name": "Bogor",
            "pid": 12,
            "rid": 31,
        },
        {
            "name": "Depok",
            "pid": 12,
            "rid": 32,
        },
        {
            "name": "Jakarta",
            "pid": 13,
            "rid": 35,
        },
    ]

    end_date = date.today()
    start_date = (end_date - timedelta(days=7)).strftime("%d-%m-%Y")
    end_date = end_date.strftime("%d-%m-%Y")
    
    for regency in regency_list:
        data = {
            'format': 'xls',
            'price_type_id': 1,
            # 'filter_commodity_ids[]': 0,
            'filter_province_ids[]': regency["pid"],
            'filter_regency_ids[]': regency["rid"],
            # 'filter_market_ids[]': 0,
            'filter_layout': 'default',
            'filter_start_date': start_date,
            'filter_end_date': end_date,
        }

        filename = regency["name"]

        response = requests.post('https://hargapangan.id/tabel-harga/pasar-tradisional/daerah', data=data)
        with open(filename + '.xls', 'wb') as f:
            f.write(response.content)

        # Process Files and Convert to CSV
        wb = xlrd.open_workbook(filename + '.xls', ignore_workbook_corruption=True)
        df = pd.read_excel(wb, skiprows=8)
        df = df.replace(r'\n', '', regex=True)
        os.remove(filename + '.xls')
        df.to_csv(filename + '.csv', index=False)


retrieveData()
