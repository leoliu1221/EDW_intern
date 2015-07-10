# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 13:41:52 2015

@author: sqltest
"""
import re 

def getData3(fName=None):
    '''
    Get data from file. 
    Args:
        fName: optional. Provides the filename to the csv data file. Format: each column is separated by "|"
    Returns:
        Data: a dictionary of [...]
    '''
    
    if fName is None:
        fName = 'breast_cancer_notes.csv'
    f = open(fName,'r')
    #burn the first line
    header = f.readline();
    print "header:",header
    rawText = f.read()
    rawText = rawText.split("|")
    raw = ''
    data = []
    note = {}    
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
        first_eightthousand = raw[i+5]
        second_eightthousand = raw[i+6]
        data.append([rowNum,first_eightthousand+second_eightthousand])
                
        i = i+7
        rowNum+=1
    return data   
    
data3 = getData3()
    
    