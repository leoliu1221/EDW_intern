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
from stage_cancer import getAllStages,getStageFromPa,get_cancer_type
#('stage',text_in[i])
def hasColon2(note):
    '''
    check if the note says colon cancer II or not. 
    Args: 
        Note:A string represnetation of note. 
    Returns:
        True if colon cancer II
        False otherwise. 
    '''
    maxStage=0;
    stageResult = findStages('stage',note)
    gradeResult = findStages('grade',note)
    if len(stageResult)==0 and len(gradeResult)==0:
        return False
    for stage in stageResult:
        stage = int(stage)
        if stage>2:
            return False
        if stage>maxStage:
            maxStage = stage;
    return maxStage == 2


if __name__ == '__main__':
    result = []
    data = getData()
    row=0
    for pid,fDate,pDate,pNote,paDate,paNote in data:
        
        
            if result.get(pid)==None:
                result[pid]= {}
                
                result[pid]['pNote'] = {}
                result[pid]['paNote']={}
            result[pid]['stage'].extend(getAllStages(pNote))
            result[pid]['stage'].extend(getAllStages(paNote))
            result[pid]['stage'].extend(getStageFromPa(paNote))
            result[pid]['type'].update(get_cancer_type(pNote))
            result[pid]['type'].update(get_cancer_type(paNote))
        row+=1
    count=0;
    for pid in result.keys():
        if len(result[pid]['type'])==0:
            count+=1
    print count,len(result.keys())
    '''
    for pid in result.keys():
        result[pid] = set(result[pid].sort(reverse=True))
    '''
                        