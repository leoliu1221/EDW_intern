# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:22:37 2015

@author: Liu and Papis
"""
import re,json

def update(dic1, dic2):
    '''
    Args:
        dic1: first dictionary  1-> [2,3,4]  2-> [3,4,5]
        dic2: second dictionary   1-> [5,6,7] 2-> [9]
    Returns: 
        dic1: first and second dictionary with key and value combined.  
        e.g. 1-> [2,3,4,5,6,7] 2-> [3,4,5,9]
    '''
    for key in dic2.keys():
        if dic1.get(key)==None:
            dic1[key] = []
        dic1[key].extend(dic2[key])
    for key in dic1.keys():
        dic1[key] = list(set(dic1[key]))
    return dic1
def in_variants(check,variants):
    for item in variants:
        if item.lower() in check.lower():
            return True
    return False
    
    
def dict_add(d1,d2):
    '''
    



    '''
    if d1==None:
        return d2
    if d2==None:
        return d1
    result = {}
    for cancer in d1.keys():
        if d2.get(cancer)==None:
            result[cancer] = d1[cancer]
        else:
            result[cancer] = d1[cancer]+d2[cancer]
    for key in d2.keys():
        if key in result.keys():
            continue
        result[key] = d2[key]
    return result

    
def readLines(file = 'organList.txt',threshold=2):
    '''
    Args: 
        file: a string of file. Default: organList.txt
        threshold: a integer of minimum word length to filter out if not met. Default:2
    Returns: 
        A list of all lines, removed all words lower than threshold
    '''
    result = []
    #read file
    with open(file,'r') as f:
        for line in f:
            #some of the words are less than length of 2 and we dont care about those
            if(len(line)>threshold):
                result.append(line.lower().strip().split(','))
    return result

def exportFile(fileName,data,result):
    '''
    export the result into csv. 
    Args:
        fileName: string of the file
        data: the original data in list format
        result: the result dictionary 
        pGroup: the dictionary of pid-> {row numbers-> None}
    '''
    #import csv
    for key,value in result.items():
        for k1,v1 in value.items():
            if k1.startswith('content'):
                continue
            for k2, v2 in v1.items():
                if type(v2) == type([]):
                    result[key][k1][k2]=v2[0]
    with open(fileName,'w') as fp:
        json.dump(result,fp)
                
def getData3(fName=None):
    '''
    Get data from file. 
    Args:
        fName: optional. Provides the filename to the csv data file. Format: each column is separated by "|"
    Returns:
        Data: a dictionary of [...]
    '''
    
    if fName is None:
        fName = 'data/ovarian.csv'
    f = open(fName,'r')
    #burn the first line
    header = f.readline();
    print "header:",header
    rawText = f.read()
    rawText = rawText.split("|")
    raw = ''
    data = []
    i=0
    while i<len(rawText):
        
        if i%6 != 0 :
            raw = raw + rawText[i] + "|"
        else:
            pid = re.findall(re.compile('\d{8}'),rawText[i])
            text = re.split('"\d{8}"',rawText[i])
            if len(pid)>0:
                raw = raw + text[0] + "|" + pid[0] + "|"
            else:
                print i
                break

        i+=1
    
    raw = raw.split("|")      
    
    i=1
    rowNum = 0
    while i<len(raw)-1:
        '''
        encntr_id = int(raw[i].replace('"',''))
        event_id = int(raw[i+1].replace('"',''))
        event_end_dt_tm = raw[i+2]
        event_cd = int(raw[i+3].replace('"',''))
        event_dsc = raw[i+4]
        '''
        encounterid = raw[i]
        first_eightthousand = raw[i+5]
        second_eightthousand = raw[i+6]
        data.append([rowNum,first_eightthousand+second_eightthousand,encounterid])
                
        i = i+7
        rowNum+=1
        print rowNum
    return data                  

            
def match_encounter_id(data, result):
    '''
    '''
    for key in result.keys():
        result[key]['encounterid'] = data[key][2]
    return result
  
def get_name(filePath):
    '''
    e.g. if the filepath is 'C:\\data\\breast.csv
    then return breast. 
    '''
    result = []
    for c in filePath:
        if c.isalnum():
            result.append(c)
        else:
            result.append(' ')
    result= ''.join(result)
    if len(result.split())<2:
        return 'NOVALUE'
    else:
        return result.split()[-2]
def dic_to_list(result):
    '''
    result should be a dictionary
        -  cancertype : k-v
        -  cancertype : k-v
        ...
        -  content : k-v
    '''
    list_result = []
    for cancertype in result.keys():
        for item in result[cancertype]:
            pass
            
    
if __name__=='__main__':
    
    '''
    if not 'data' in locals():    
        data = getData3()

    s = data[9][1]
    '''  
    from models import Datapoint,dumper
    s2 = 'Breast Tumor Markers: (combined with report of S-12-11788)\t_\t\n\tER:\t>95%, strong positive\t\n\tPR:\t  95%, strong positive\t\n\tHER2:\t     0%, score 0, negative\t\n\tKi-67\t10-15%, intermediate\t\n\tp53:\t     0%, negative\t'
    test = Datapoint(s2)
    print dumper([test,test,test])
    pass

            
    
    
