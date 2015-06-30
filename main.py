# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:07:04 2015

@author: sqltest
"""

'''
File name: main.py
Dependencies: file_utilities.py, stage_cancer.py

'''

from file_utilities import getData,update
from stage_cancer import get_stage_num,get_stage_from_pa,get_cancer_type
from matching import match_result


def get_result(fileName):
    result = {}
    data = getData(fileName)
    row=0
    for pid,fDate,pDate,pNote,paDate,paNote in data:
        if result.get(row)==None:
            result[row]= {}
            result[row]['p'] = [{},{}]
            result[row]['pa']=[{},{}]
            result[row]['pid'] = pid
        update(result[row]['p'][1],get_stage_num(pNote,'grade'))
        update(result[row]['p'][1],get_stage_num(pNote,'stage'))
        update(result[row]['pa'][1],get_stage_num(paNote,'stage'))
        update(result[row]['pa'][1],get_stage_num(paNote,'grade'))
        update(result[row]['pa'][1],get_stage_from_pa(paNote))
        update(result[row]['pa'][0],get_cancer_type(paNote))
        update(result[row]['p'][0],get_cancer_type(pNote))
        matchResult = update(match_result(result[row]['p'],'p'),match_result(result[row]['pa'],'pa'))
        result[row]['stage'] = matchResult
    return data,result

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
            result[row]['pid'] = pid
        update(result[row]['p'][1],get_stage_num(pNote,'grade'))
        update(result[row]['p'][1],get_stage_num(pNote,'stage'))
        update(result[row]['pa'][1],get_stage_num(paNote,'stage'))
        update(result[row]['pa'][1],get_stage_num(paNote,'grade'))
        update(result[row]['pa'][1],get_stage_from_pa(paNote))
        update(result[row]['pa'][0],get_cancer_type(paNote))
        update(result[row]['p'][0],get_cancer_type(pNote))
        matchResult = update(match_result(result[row]['p'],'p'),match_result(result[row]['pa'],'pa'))
        result[row]['stage'] = matchResult
        
        
        
        
        
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
                        
