# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:07:04 2015

@author: sqltest
"""

'''
File name: main.py
Dependencies: file_utilities.py, stage_cancer.py

'''

from file_utilities import getData
from stage_cancer import get_stage_num,getStageFromPa,get_cancer_type
#('stage',text_in[i])
if __name__ == '__main__':
    result = {}
    data = getData()
    row=0
    for pid,fDate,pDate,pNote,paDate,paNote in data:
        if result.get(row)==None:
            result[row]= {}
            result[row]['p'] = [{},{}]
            result[row]['pa']=[{},{}]
            result[row]['stage'] = []
            result[row]['pid'] = pid
        result[row]['p'][1].update(get_stage_num(pNote,'grade'))
        result[row]['p'][1].update(get_stage_num(pNote,'stage'))
        result[row]['pa'][1].update(get_stage_num(paNote,'stage'))
        result[row]['pa'][1].update(get_stage_num(paNote,'grade'))
        result[row]['pa'][0].update(get_cancer_type(pNote))
        result[row]['p'][0].update(get_cancer_type(paNote))
        row+=1
    count=0;
    for pid in result.keys():
        if len(result[pid]['pa'][0].keys())==0:
            count+=1
    print count,len(result.keys())
    '''
    for pid in result.keys():
        result[pid] = set(result[pid].sort(reverse=True))
    '''
                        
