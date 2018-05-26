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
noise_dist = pd.DataFrame(data = None, columns = columns_name)

for points in range(30):
    
    min_lat, max_lat = -90, 90
    min_lng, max_lng = -180, 180
    latitude = random.random()*(max_lat-min_lat)+min_lat
    longitude = random.random()*(max_lng-min_lng)+min_lng
    
    for number_of_tests in range(10):
        nice_try = make_req(name = user_name, lng = longitude, lat = latitude)
        noise_dist.loc[-1] = [latitude, longitude, nice_try['score']]
        noise_dist.index += 1
        print(nice_try)

    
noise_dist = noise_dist.sort_index()        
noise_dist.to_csv("Check_Distribution", sep = ';')

noise_mean = noise_dist.groupby(['lng','lat']).mean()

noise_distribution = noise_dist.join(noise_mean.set_index(['lng','lat']), on = ['lng','lat'])