# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 13:58:30 2015

@author: lliu5
"""

import requests,json
uri = "http://bugs.python.org"
sample_data = {'@number': 12524, '@type': 'issue', '@action': 'show'}
r = requests.post(uri, data=json.dumps(sample_data))
#or ican use r = requests.post(uri, json=sample_data)
print(r.status_code, r.reason)
print(r.text[:300] + '...')