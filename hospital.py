import numpy as np
import pandas as pd
from datetime import *
import math
import json
import urllib.parse as urlparse
import warnings
import requests
import os
from selenium import webdriver

def parse(url):
        parsed = urlparse.urlparse(url)
        lat = float(urlparse.parse_qs(parsed.query)['lat'][0])
        long = float(urlparse.parse_qs(parsed.query)['long'][0])
        #spec = urlparse.parse_qs(parsed.query)['spec'][0]
        return(lat, long)

def predict(url, spec):
        lat, long = parse(url)

        warnings.filterwarnings("ignore")

        data = pd.read_csv("doctors.csv")

        tim = datetime.now().time().strftime('%H:%M')
        tim = datetime.strptime(tim, "%H:%M").time()

        id = data[data['specialization'] == spec][['free_from', 'doctor_to', 'doctor_id', 'latitude', 'longitude']]

        temp = id[['free_from', 'doctor_to']].apply(lambda x: [datetime.strptime(i, '%H:%M').time() for i in x])

        result = pd.concat([id[['doctor_id', 'latitude', 'longitude']], temp], axis = 1, join_axes = [id.index])

        result2 = result[tim > result['free_from']]
        result2 = result2[tim < result['doctor_to']]

        Min = 99999999999999999
        for index, i in result2.iterrows():
                dist = math.sqrt((i[1] - lat)**2 + (i[2] - long)**2)
        if dist < Min:
                min_index = i[0]
                Min = dist


        def format(a):
                a = a[a.find("  "):a.find("\n")]
                return a

        x = {
                'doctor_id' : format(str(data[data['doctor_id'] == min_index]['doctor_id'])),
                'doctor_name' : format(str(data[data['doctor_id'] == min_index]['doctor_name'])),
                'hosp_id' : format(str(data[data['doctor_id'] == min_index]['hosp_id']))
        }

        y = json.dumps(x)
        return(y)