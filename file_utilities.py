# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 10:22:37 2015

@author: Liu and Papis
"""

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
    #print data.keys()   
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
                result.append(line.lower().strip().split(','))
    return result
def getData2(fName=None):
    '''
    Get data from file. 
    Args:
        fName: optional. Provides the filename to the csv data file. Format: each column is separated by "|"
    Returns:
        Data: a dictionary of [patientid,First_diagnosis_date,Physician_note_date,Physician_note,Pathology_note_date,Pathology_note]
    '''
    import re
    if fName is None:
        fName = 'cancer_notes_lung.csv'
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
        line = text[i+1].split('"|"')
        fDate = line[0].replace('|"','')
        pDate = line[1].replace('"','')
        pNote = line[2].replace('"','')
        paDate = line[3].replace('"','')
        paNote = line[4].replace('"','').replace('"\n','')

        data.append([int(pid[i]),fDate,pDate,pNote.lower(),paDate,paNote.lower()])
        i+=1
  
    return data    

def exportFile(fileName,data,result,pGroup):
    '''
    export the result into csv. 
    Args:
        fileName: string of the file
        data: the original data in list format
        result: the result dictionary 
        pGroup: the dictionary of pid-> {row numbers-> None}
    '''
    import csv
    c = csv.writer(open(fileName,'wb'))
    
    for line in xrange(len(data)):
        temp = [line]
        #print result[lineNum]['stage']
        organResults = []
        if len(result[line]['stage'].keys())>0:
            for organ in result[line]['stage'].keys():
                for tempResult in result[line]['stage'][organ]:
                    organResults.append((organ,tempResult[0]))
        temp.append(list(set(organResults)))
        c.writerow(temp)
    
#read tnm rule file. 
def get_tnm(fileName = 'tnm.txt'):
    '''
    read the tnm configuration file
    Args: 
        filename a string of the file name input
    Returns: 
        result:  a dictionary of rules read from the configuration file specified by input fileName
        NOTE: the data structure of result is: 
        result:dictionary:string -> dictionary: string -> list:sets
        plain english: result is a dictionary that has string dictionary pairs, for which dictionary is string list pairs, for which list contains sets
    '''
    result = {}
    current = None
    with open(fileName,'r') as f:        
        for line in f:
            line = line.strip().lower().split()
            #check if its a new catagory or not. 
            #skip empty line            
            if len(line)<1:
                continue
            if len(line) == 1:
                current = line[0]
                if result.get(current) == None:
                    result[current]={}
                continue
            #skip until it finds an organ/type
            if current is None:
                continue
            if len(line)==4:
                if result[current].get(line[0])==None:
                    result[current][line[0]] = []
                result[current][line[0]].append(set(line[1:]))
    return result
                
                

            
            

if __name__=='__main__':
    rules = read_tnm()

    

            
    
    