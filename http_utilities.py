# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 13:58:30 2015

@author: lliu5
"""

import requests,json
from jsonweb import dumper
from jsonweb import encode
#for testing
from models import Datapoint
#universe_id = integer, about_type = string, about_id = integer, result = hash

def post_json(universe_id,about_type,about_id,result,uri=None):
    if uri is None:
        uri = "http://127.0.0.1:5000/note"
    data = {}
    data['universe_id'] = universe_id
    data['about_type'] = about_type
    data['about_id'] = about_id
    data['source'] = 'liu_papis_nlp'
    data['result'] = result    
    headers = {'content-type':'application/json'}
    r = requests.post(uri, data=dumper(data),headers = headers)
#or ican use r = requests.post(uri, json=sample_data)
    print(r.status_code, r.reason)
    print(r.text[:300] + '...')
    print '*'*100
    print dumper(data)
    return dumper(data)
    
if __name__ == '__main__':
    universe_id = 0
    about_type = 'some type'
    about_id = 0
    s2 = 'Breast Tumor Markers: (combined with report of S-12-11788)\t_\t\n\tER:\t>95%, strong positive\t\n\tPR:\t  95%, strong positive\t\n\tHER2:\t     0%, score 0, negative\t\n\tKi-67\t10-15%, intermediate\t\n\tp53:\t     0%, negative\t'
    test = Datapoint(s2) 
    result = [test,test,test]
    post_json(universe_id,about_type,about_id,result)
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
