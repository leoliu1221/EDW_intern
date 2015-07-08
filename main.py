# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:07:04 2015

@author: sqltest
"""

'''
File name: main.py
Dependencies: file_utilities.py, stage_cancer.py

'''

from file_utilities import getData,update,getData2
from stage_cancer import get_stage_num,get_stage_from_pa,get_cancer_type
from matching import match_result


def get_result(fileName='cancer_notes_lung.csv',data=None,t1=5,t2=40,t3=50):
    '''
    Args:
        fileName is the name of the file
        data is the data if we already read it in
        t1 is the threshold for finding number after keyword stage or grade
        t2 is the threshol for finding TNM system how close TNM sholud be together after ajcc or tnm keyword
        t3 is the matching on how close a stage number and cancer type should be in a sentence
    '''
    result = {}
    if data is None:
        print 'getting data from ',fileName
        data = getData2(fName = fileName)
    row=0
    for pid,fDate,pDate,pNote,paDate,paNote in data:
        if result.get(row)==None:
            result[row]= {}
            result[row]['p'] = [{},{}]
            result[row]['pa']=[{},{}]
            result[row]['pid'] = pid
        update(result[row]['p'][1],get_stage_num(pNote,'grade',threshold=t1))
        update(result[row]['p'][1],get_stage_num(pNote,'stage',threshold=t1))
        update(result[row]['pa'][1],get_stage_num(paNote,'stage',threshold=t1))
        update(result[row]['pa'][1],get_stage_num(paNote,'grade',threshold=t1))
        update(result[row]['pa'][1],get_stage_from_pa(paNote,threshold=t2))
        update(result[row]['pa'][0],get_cancer_type(paNote))
        update(result[row]['p'][0],get_cancer_type(pNote))
        matchResult = update(match_result(result[row]['p'],'p',threshold=t3),match_result(result[row]['pa'],'pa',threshold=t3))
        result[row]['stage'] = matchResult
        row+=1
        result2 = {}
    #result2 has patient as the key and all other things as values. 
        for key in result.keys():
            if result2.get(result[key]['pid'])==None:
                result2[result[key]['pid']]={}
            result2[result[key]['pid']][key] = None
    print 'finished getting result'
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
        update(result[row]['pa'][1],get_stage_num(paNote,'stage'))
        update(result[row]['pa'][1],get_stage_num(paNote,'grade'))
        update(result[row]['pa'][1],get_stage_from_pa(paNote))
        update(result[row]['pa'][0],get_cancer_type(paNote))
        update(result[row]['p'][0],get_cancer_type(pNote))
        matchResult = update(match_result(result[row]['p'],'p'),match_result(result[row]['pa'],'pa'))
        result[row]['stage'] = matchResult 
        row+=1
    count=0
    for pid in result.keys():
        if len(result[pid]['stage'].keys())==0:
            count+=1
    print count,len(result.keys())
    '''
    for pid in result.keys():
        result[pid] = set(result[pid].sort(reverse=True))
    '''
                        
