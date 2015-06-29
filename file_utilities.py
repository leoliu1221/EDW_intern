# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:22:37 2015

@author: Liu and Papis
"""


def readNote(s,d=None):
    '''
    Read from the begining of note to the end of the note
    Args:
        s a string of remaining text
        d a string representation shows the start and end of the coloumn
    Returns: 
        Note: String of note that it recognized. If not then return None Starting from the first """ to the last of """
        remain: the remaining of the text after stripping off the comma and current note. 
          '''
    if len(s)==0:
        return '',''
    if s[0]==',':
        return '',s[1:]
    if s[0].isdigit():
        return '',s
    try:
        if d is None:
            d = '\"\"\"'
    #get the first position of """
            start = s.find(d)+len(d)
            #print 'start: ',start
            stop = s[start:].find(d)+start
            #print 'stop:',stop
            #print s[stop:stop+len(d)]
            if start==-1:
                print 'no """ found'
                return '',stripComma(s) #eat up the comma
            #if start is there however there is no stop, then there must be a problem. 
            return s[start:stop],stripComma(s[stop+len(d):])
    except:
        print "exception in readNote"
        print s
        import sys
        sys.exit(1)
def stripComma(s):
    '''
    If there is immediate comma strip it, othewise remain the same
    '''
    if s[0]==',':
        return s[1:]
    else:
        return s
def readId(s):
    '''
    read the first field until the first comma. Presumably it is supposed to be the patient id.
    Returns:
        Id: a string of id
        Remain: a string of remaing to process. 
    '''
    #clean the string until the first letter is a number
    if len(s)==0:
        return '',''
    if s[0]==',':
        return '',s[1:]
        
    s = cleanTillNum(s)
    if len(s)==0:
        return '',''
    i = 0
    while(s[i]!=','):
        i+=1
        if(i>=len(s)):
            return None
    return s[0:i],s[i+1:]
    
def cleanTillNum(s):
    '''
    Args:
        s -- input string 
    Returns:
        s -- output string, with a number at the beginning
    '''
    i=0
    if len(s)==0:
        return s
    while(not s[i].isdigit()):
        if s[i]!=',':
            print 'cleaned',s[i]
        i+=1
        if(i>=len(s)):
            return '';
    return s[i:]
def getData(fName=None):
    '''
    Get data from file. 
    Args:
        fName: optional. Provides the filename to the csv data file. Must use the same formating as before. 
    Returns:
        Data: a dictionary of patientid -> array of array[First_diagnosis_date,Physician_note_date,Physician_note,Pathology_note_date,Pathology_note]
    '''
    fName = None
    if fName is None:
        fName = 'data.csv'
    f = open(fName,'r')
    #burn the first line
    header = f.readline();
    print "header:",header
    raw = f.read().replace('\n','')
    data = []
    while len(raw)>0:
        #try:
        pid,raw = readId(raw)
        while(not pid.isdigit()):
            print 'pid is not digit',pid
            pid,raw = readId(raw)
    
        #print pid
        fDate,raw = readId(raw)
        pDate,raw = readId(raw)
        pNote,raw = readNote(raw)
        paDate,raw = readId(raw)
        paNote,raw = readNote(raw)
        data.append([int(pid),fDate,pDate,pNote.lower(),paDate,paNote.lower()])
        
    return data
    
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
                result.append(line.lower().strip())
    return result
    
    
    
    
    
'''
if __name__=='__main__':
    #GETS THE DATA
    data = getData()
    total = 0
    for pid in data.keys():
        total+=len(data[pid])
    print 'total records loaded:',total
'''
    

            
    
    