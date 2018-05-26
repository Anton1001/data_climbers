# -*- coding: utf-8 -*-
"""
Created on Sat May 26 14:52:35 2018

@author: Sven
"""

import requests as rq
import argparse
import random

cnt_rnd = 0
cnt_lat = 0
cnt_lng = 0
cnt_both = 0
cnt_extreme = 0
cnt_close = 0

def make_req(name="sven@i", random_try = 'all', new_lng = 0, new_lat = 0 ):
    url = "http://pyapi.godatadriven.com"
    min_lat, max_lat = -90, 90
    min_lng, max_lng = -180, 180
    if random_try == 'all':
        payload = {"name": "sven@i",
                   "moonlat": random.random()*(max_lat-min_lat)+min_lat,
                   "moonlng": random.random()*(max_lng-min_lng)+min_lng}
    elif random_try == 'lat':
        payload = {"name": "sven@i",
                   "moonlat": random.random()*(max_lat-min_lat)+min_lat,
                   "moonlng": new_lng}
        #print("lat")
    elif random_try == 'lng':
        payload = {"name": "sven@i",
                   "moonlat": new_lat,
                   "moonlng": random.random()*(max_lng-min_lng)+min_lng}
        #print("lng")
    elif random_try == 'no':
        payload = {"name": "sven@i",
                   "moonlat": new_lat,
                   "moonlng": new_lng}
        #print('no')
    else:
        print('FAIL!')
    resp = rq.post(url, json=payload)
    return resp.json()

def log_try(dictionary, file_object):
    loggy = "- "
    for (key, value) in dictionary.items():
        loggy += key + ' ' + str(value) + '; '
    loggy += '\n'
    file_object.write(loggy)
        
#start the search:
#log_boek.close()
log_boek = open('C:\\Users\\Sven\\Desktop\\Repositories\\Go-data_challenge\\moon_log.txt', 'a')
    
largest = make_req(random_try = 'no', new_lat = 12.969331629915382, new_lng = -7.638264027398643)
second = make_req(random_try = 'no', new_lat = 13.675675586964573, new_lng = -7.784998737038539)
#check welke groter is
if largest['score'] < second['score']:
    middle = second
    second = largest
    largest = middle

index = 1
log_try(largest, log_boek)

for index_f in range(10000):
    index += 1
    
    if index > 250:
        new_score = make_req()
        if new_score['score'] > largest['score']:
            largest = new_score
            index = 1
            log_try(largest, log_boek)
            cnt_rnd += 1
        elif new_score['score'] > second['score']:
            second = new_score
        
    #adjust lat, lng is random
    new_coord_lat = (largest['moonlat'] + second['moonlat']) / 2
    
    new_score = make_req(random_try = 'lng', new_lat = new_coord_lat)
    if new_score['score'] > largest['score']:
        largest = new_score
        index = 1
        log_try(largest, log_boek)
        cnt_lat += 1
    elif new_score['score'] > second['score']:
        second = new_score
        
    #adjust lng, lat is random
    new_coord_lng = (largest['moonlng'] + second['moonlng']) / 2
    
    new_score = make_req(random_try = 'lat', new_lng = new_coord_lng)
    if new_score['score'] > largest['score']:
        largest = new_score
        index = 1
        log_try(largest, log_boek)
        cnt_lng += 1
    elif new_score['score'] > second['score']:
        second = new_score
        
    #adjust both
    new_coord_lng = (largest['moonlng'] + second['moonlng']) / 2
    new_coord_lat = (largest['moonlat'] + second['moonlat']) / 2
    
    new_score = make_req(random_try = 'no', new_lng = new_coord_lng, new_lat = new_coord_lat)
    if new_score['score'] > largest['score']:
        largest = new_score
        index = 1
        log_try(largest, log_boek)
        cnt_both += 1
    elif new_score['score'] > second['score']:
        second = new_score
    
    
    # try best with extreme
    factor = 1 - 1/(index + 1)
    for sign_lng in [-1,1]:
        for sign_lat in [-1,1]:
            new_coord_lng = (largest['moonlng'] + factor * sign_lng * 180) / 2
            new_coord_lat = (largest['moonlat'] + factor * sign_lat * 90) / 2
            if (abs(new_coord_lng) <= 180) and (abs(new_coord_lat) <= 90):
                new_score = make_req(random_try = 'no', new_lng = new_coord_lng, new_lat = new_coord_lat)
                if new_score['score'] > largest['score']:
                    largest = new_score
                    index = 1
                    log_try(largest, log_boek)
                    cnt_extreme += 1
                elif new_score['score'] > second['score']:
                    second = new_score
    # look close to the best
    factor = 1 + 1/(2**index)
    for sign_lng in [-1,1]:
        for sign_lat in [-1,1]:
            factor_lng = (1 + 1/(index + 1)) * sign_lng
            factor_lat = (1 + 1/(index + 1)) * sign_lat
            new_coord_lng = largest['moonlng'] * factor_lng
            new_coord_lat = largest['moonlat'] * factor_lat
            if (abs(new_coord_lng) <= 180) and (abs(new_coord_lat) <= 90):
                new_score = make_req(random_try = 'no', new_lng = new_coord_lng, new_lat = new_coord_lat)
                if new_score['score'] > largest['score']:
                    largest = new_score
                    index = 1
                    log_try(largest, log_boek)
                    cnt_close += 1
                elif new_score['score'] > second['score']:
                    second = new_score
    #best guess
    new_coord_lng = -7.395748800186613
    new_coord_lat = 12.991891807616344
    new_score = make_req(random_try = 'no', new_lng = new_coord_lng, new_lat = new_coord_lat)
    if new_score['score'] > largest['score']:
        largest = new_score
        index = 1
        log_try(largest, log_boek)
        cnt_close += 1
    elif new_score['score'] > second['score']:
        second = new_score

    
    print("Try number {0}: current score is {1}".format(index_f,largest['score']))
    print("long {0}, lat {1}".format(new_coord_lng,new_coord_lat))
    print("method-stats - rnd:{0} | lat:{1} | lng:{2} | both:{3} | extr:{4} | close:{5}".format(cnt_rnd, cnt_lat, cnt_lng, cnt_both, cnt_extreme, cnt_close))

