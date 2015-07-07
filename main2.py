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
from extractTimedate import dateToObject


def compare(x,y):
    '''
    Args:
        x,y: items to be compared
    return:
        1 : if x > y
        -1: if x < y
        0 : otherwise
    '''
    if x[1] > y[1]:
        return 1
    if x[1] < y[1]:
        return -1
    return 0
    
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
    return data,result
    

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
        #update(result[row]['p'][1],get_stage_from_pa(pNote))
        update(result[row]['pa'][1],get_stage_num(paNote,'stage'))
        update(result[row]['pa'][1],get_stage_num(paNote,'grade'))
        update(result[row]['pa'][1],get_stage_from_pa(paNote))
        update(result[row]['pa'][0],get_cancer_type(paNote))
        update(result[row]['p'][0],get_cancer_type(pNote))
        
        matchResult = update(match_result(result[row]['p'],'p'),match_result(result[row]['pa'],'pa'))
        result[row]['stage'] = matchResult
        row+=1
    
    result_pid = {}
    for key in result.keys():
        if result_pid.get(result[key]['pid'])==None:
            result_pid[result[key]['pid']]={}
        result_pid[result[key]['pid']][key] = result[key]
    
    resultOrder_pid = {}
    # rearrage record for each patient based on date and time
    for key in result_pid.keys(): 
        pid_record = result_pid[key]
        dateList = {}
        pid_record2 = {}
        for key2 in pid_record.keys():
            if data[key2][2]!='':
                datetime = data[key2][2] # datetime from p note
            else:
                datetime = data[key2][4] # datetime from pa note

            datetime = dateToObject(datetime)
            dateList[key2] = datetime
                    
        array = dateList.items()
        array.sort(compare,reverse=True)
       
        for item in array:
           pid_record2[item[0]] = pid_record[item[0]]

        resultOrder_pid[key] = pid_record2
        
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
    