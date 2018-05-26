# -*- coding: utf-8 -*-
"""
Created on Sat May 26 18:53:07 2018

@author: Sven & Anton
"""
import pandas as pd
import requests as rq
import argparse
import random


user_name = 'data_climbers'

def make_req(name = user_name, lng = 0, lat = 0 ):
    url = "http://pyapi.godatadriven.com"
    payload = {"name": name,
               "moonlat": lat,
               "moonlng": lng}
    resp = rq.post(url, json=payload)
    return resp.json()


columns_name = ['lat','lng','score']
noise_dist = pd.DataFrame(data = None,columns = columns_name)

noise_dist.head()

for points in range(30):
    
    min_lat, max_lat = -90, 90
    min_lng, max_lng = -180, 180
    latitude = random.random()*(max_lat-min_lat)+min_lat
    longitude = random.random()*(max_lng-min_lng)+min_lng
    
    for number_of_tests in range(10):
        nice_try = make_req(name = user_name, lng = longitude, lat = latitude)
        noise_dist.append([latitude, longitude, nice_try['score']])
        print(nice_try)
        
nice_try.to_csv("Check_Distribution", sep = ';')