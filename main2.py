# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:07:04 2015

@author: sqltest
"""

'''
File name: main.py
Dependencies: file_utilities.py, stage_cancer.py

'''

from file_utilities import update,getData2
from stage_cancer import get_stage_num,get_stage_from_pa,get_cancer_type,get_tnm
from matching import match_result


def get_result2(fileName):
    result = {}
    data = getData2(fileName)
    row=0
    for pid,fDate,pDate,pNote,paDate,paNote in data:
        if result.get(row)==None:
            result[row]= {}
            result[row]['p'] = [{},{}]
            result[row]['pa']=[{},{}]
            result[row]['pid'] = pid
        update(result[row]['p'][1],get_stage_num(pNote,'grade'))
        update(result[row]['p'][1],get_stage_num(pNote,'stage'))
        update(result[row]['p'][1],get_tnm(pNote))
        update(result[row]['pa'][1],get_stage_num(paNote,'stage'))
        update(result[row]['pa'][1],get_stage_num(paNote,'grade'))
        update(result[row]['pa'][1],get_stage_from_pa(paNote))
        update(result[row]['pa'][0],get_cancer_type(paNote))
        update(result[row]['p'][0],get_cancer_type(pNote))
        matchResult = update(match_result(result[row]['p']),match_result(result[row]['pa']))
        result[row]['stage'] = matchResult
        result2 = {}
    #result2 has patient as the key and all other things as values. 
        for key in result.keys():
            if result2.get(result[key]['pid'])==None:
                result2[result[key]['pid']]={}
            result2[result[key]['pid']][key] = None
    return data,result,result2

#('stage',text_in[i])
if __name__ == '__main__':
    result = {}
    data = getData2()
    row=0
    for pid,fDate,pDate,pNote,paDate,paNote in data:
        if result.get(row)==None:
            result[row]= {}
            result[row]['p'] = [{},{}]
            result[row]['pa']=[{},{}]
            result[row]['pid'] = pid
        update(result[row]['p'][1],get_stage_num(pNote,'grade'))
        update(result[row]['p'][1],get_stage_num(pNote,'stage'))
        update(result[row]['p'][1],get_tnm(pNote))
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
        #if len(result[pid]['pa'][0].keys())==0:
        if len(result[pid]['stage'])==0:
            count+=1
    print count,len(result.keys())
    '''
    for pid in result.keys():
        result[pid] = set(result[pid].sort(reverse=True))
    '''
    
