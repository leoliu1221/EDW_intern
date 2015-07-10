# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 11:07:04 2015

@author: sqltest
"""

'''
File name: main.py
Dependencies: file_utilities.py, stage_cancer.py

'''

from file_utilities import update,getData2,getData3
from stage_cancer import get_stage_num,get_stage_from_pa,get_cancer_type
from matching import match_result
from extractTimedate import compareTime,dateToObject

def get_result(fileName='breast_cancer_notes.csv',data=None,organ='colon',oName = 'organList.txt',cName = 'cancerList.txt',confFile = 'stageKeys.yaml',organs=None,keywords=None,cancers = None,stages=None,t1=5,t2=40,t3=50):
    '''
    Args:
        fileName is the name of the file
        data is the data if we already read it in
        organs is the organ list read in from file
        keywords is the tnm keyword list read in from file
        stages is the stage rules read in from file
        t1 is the threshold for finding number after keyword stage or grade
        t2 is the threshol for finding TNM system how close TNM sholud be together after ajcc or tnm keyword
        t3 is the matching on how close a stage number and cancer type should be in a sentence
    '''
    result = {}
    if data is None:
        print 'getting data from ',fileName
        data = getData2(fName = fileName)
                
    if organs is None:
        from file_utilities import readLines
        organs = readLines(oName)
    if cancers is None:
        from file_utilities import readLines
        cancers = readLines(cName)
    if keywords == None: 
        import yaml
        with open(confFile,'r') as f:
            cfg = yaml.load(f)
        keywords = cfg['keys']
    #loading the stage and keyword from file 'stageKeys.yaml'
    if stages == None:
        try:
            from file_utilities import get_tnm
            stages = get_tnm()[organ]
        except:
            return {}
    row=0
    for pid,fDate,pDate,pNote,paDate,paNote in data:
        print row
        if result.get(row)==None:
            result[row]= {}
            result[row]['p'] = [{},{}]
            result[row]['pa']=[{},{}]
            result[row]['pid'] = pid
        update(result[row]['p'][1],get_stage_num(pNote,'grade',threshold=t1))
        update(result[row]['p'][1],get_stage_num(pNote,'stage',threshold=t1))
        update(result[row]['pa'][1],get_stage_num(paNote,'stage',threshold=t1))
        update(result[row]['pa'][1],get_stage_num(paNote,'grade',threshold=t1))
        update(result[row]['pa'][1],get_stage_from_pa(paNote,threshold=t2,organ=organ,stages = stages))
        update(result[row]['pa'][0],get_cancer_type(paNote,organs = organs,cancers = cancers))
        update(result[row]['p'][0],get_cancer_type(pNote,organs = organs,cancers = cancers))
        matchResult = update(match_result(result[row]['p'],'p',threshold=t3),match_result(result[row]['pa'],'pa',threshold=t3))
        result[row]['stage'] = matchResult
        row+=1
        
        result2 = {}
    #result2 has patient as the key and all other things as values. 
        for key in result.keys():
            if result2.get(result[key]['pid'])==None:
                result2[result[key]['pid']]={}
            result2[result[key]['pid']][key] = None
            
    #sort each value in result2 for each key based on the actual date. 
        for pid in result2.keys():
            rows = result2[pid]
            dateList = {}
            for rowNum in rows.keys():
                if data[rowNum][2]!='':
                    datetime = data[rowNum][2]
                else:
                    datetime=data[rowNum][4]
                datetime = dateToObject(datetime)
                dateList[rowNum] = datetime
            dateItems = dateList.items()
            dateItems.sort(compareTime,reverse=True)
            result2[pid] = [item[0] for item in dateItems]
            
            
    print 'finished getting result'
    count = 0
    for key in result.keys():
        if result[key]['stage']!={}:
            count+=1
    print 'count:',count,'total:',len(result.keys())
    return data,result,result2
def get_result2(fileName='breast_cancer_notes.csv',data=None,organ='colon',oName = 'organList.txt',cName = 'cancerList.txt',confFile = 'stageKeys.yaml',organs=None,keywords=None,cancers = None,stages=None,t1=5,t2=40,t3=50):
    '''
    Args:
        fileName is the name of the file
        data is the data if we already read it in
        organs is the organ list read in from file
        keywords is the tnm keyword list read in from file
        stages is the stage rules read in from file
        t1 is the threshold for finding number after keyword stage or grade
        t2 is the threshol for finding TNM system how close TNM sholud be together after ajcc or tnm keyword
        t3 is the matching on how close a stage number and cancer type should be in a sentence
    '''
    result = {}
    if data is None:
        print 'getting data from ',fileName
        data = getData3(fName = fileName)
                
    if organs is None:
        from file_utilities import readLines
        organs = readLines(oName)
    if cancers is None:
        from file_utilities import readLines
        cancers = readLines(cName)
    if keywords == None: 
        import yaml
        with open(confFile,'r') as f:
            cfg = yaml.load(f)
        keywords = cfg['keys']
    #loading the stage and keyword from file 'stageKeys.yaml'
    if stages == None:
        try:
            from file_utilities import get_tnm
            stages = get_tnm()[organ]
        except:
            return {}
    row=0
    for pid,fDate,paNote in data:
        print row
        if result.get(row)==None:
            result[row]['note']= [{},{}]
        update(result[row]['note'][1],get_stage_num(paNote,'stage',threshold=t1))
        update(result[row]['note'][1],get_stage_num(paNote,'grade',threshold=t1))
        update(result[row]['note'][1],get_stage_from_pa(paNote,threshold=t2,organ=organ,stages = stages))
        update(result[row]['note'][0],get_cancer_type(paNote,organs = organs,cancers = cancers))
        matchResult = update(match_result(result[row],'pa',threshold=t3))
        result[row]['stage'] = matchResult
        row+=1    
    print 'finished getting result'
    count = 0
    for key in result.keys():
        if result[key]['stage']!={}:
            count+=1
    print 'count:',count,'total:',len(result.keys())
    return data,result

#('stage',text_in[i])
if __name__ == '__main__':
    data,result,result2 = get_result()