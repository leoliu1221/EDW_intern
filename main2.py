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


def get_result(fileName):
    result = {}
    data = getData(fileNae)
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
                        
def getData2(fName=None):
    '''
    Get data from file. 
    Args:
        fName: optional. Provides the filename to the csv data file. Format: each column is separated by "|"
    Returns:
        Data: a dictionary of [patientid,First_diagnosis_date,Physician_note_date,Physician_note,Pathology_note_date,Pathology_note]
    '''

    fName = None
    if fName is None:
        fName = 'cancer_notes.csv'
    f = open(fName,'r')
    #burn the first line
    header = f.readline();
    print "header:",header
    raw = f.read()
    # find pid 
    pid = re.findall(re.compile('"\d{7}"'),raw)
    # split between each row by capturing "pid" where pid is 7 digit number
    text = re.split('"\d{7}"',raw)
    data=[]
    i=0
    while i<len(pid):
        pid[i] = pid[i].replace('"','')
        print pid[i]
        line = text[i+1].split("|")
        fDate = line[1].replace('"','')
        pDate = line[2].replace('"','')
        pNote = line[3].replace('"','')
        paDate = line[4].replace('"','')
        paNote = line[5].replace('"','').replace('\n','')

        data.append([int(pid[i]),fDate,pDate,pNote.lower(),paDate,paNote.lower()])
        i+=1
  
    return data    
    