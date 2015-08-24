# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 13:58:30 2015

@author: lliu5
"""

import requests,json
#universe_id = integer, about_type = string, about_id = integer, result = hash

def post_json(universe_id,about_type,about_id,result,uri=None):
    if uri is None:
        uri = "http://127.0.0.1:5000/cleaner_result"
    data = {}
    data['universe_id'] = universe_id
    data['about_type'] = about_type
    data['about_id'] = about_id
    data['result'] = result    
    r = requests.post(uri, data=(data))
#or ican use r = requests.post(uri, json=sample_data)
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')
post_json()
'''
parser.add_argument('text')
parser.add_argument('key')
parser.add_argument('about_type')
parser.add_argument('value')
parser.add_argument('universe_id')
parser.add_argument('suggestions_uri')
parser.add_argument('universe_name')
parser.add_argument('universe_name_variants')
'''