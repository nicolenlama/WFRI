# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 15:31:17 2020

Employment
https://api.bls.gov/publicAPI/v2/timeseries/data/LAUCN370090000000005?registrationkey=os.getenvREG_KEY_USCENBUREAU&latest=true

Unemployment
https://api.bls.gov/publicAPI/v2/timeseries/data/LAUCN370090000000003?registrationkey=os.getenvREG_KEY_USCENBUREAU&latest=true

Labor Force
https://api.bls.gov/publicAPI/v2/timeseries/data/LAUCN370090000000006?registrationkey=os.getenvREG_KEY_USCENBUREAU&latest=true

@author: nlama
"""


import requests
import pandas as pd
import pickle
import json

data = pd.read_csv("D:/DHIT/CwC/Data/counties_NC.csv")

csvOut = open('all_NC_county_unemployment_stats.csv', 'w')
csvOut.write("County,Month,Year,Labor_Force\n")

for county,s_id in zip(data["Name"],data["Area_Code_for_Series_ID"]):
    url_employment = "https://api.bls.gov/publicAPI/v2/timeseries/data/LAU{0}03?registrationkey=os.getenvREG_KEY_USCENBUREAU".format(s_id)
    c = county.replace("County","")
    print(c)
    response = requests.request("GET", url_employment)
    if response.status_code != 200:
        print(response.status_code)
    
    js = json.loads(response.text)
    try:
        for row in js['Results']["series"]:
            for d_row in row['data']:
                year = d_row['year']
                value = d_row['value']
                month = d_row['periodName']
                csvOut.write("{0},{1},{2},{3}\n".format(c,month,year,value))
    except:
        continue
            

csvOut.close()
