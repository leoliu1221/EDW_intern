# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from collections import defaultdict
import re
import numpy as np
from file_utilities import dict_add
#
#def collectValue(inputDict):
#    value = defaultdict(list)
#    for k,v in inputDict.iteritems():
#        for k2,v2 in v.iteritems():
#            if k2!='content':
#                for k3,v3 in v2.iteritems():
#                    value[k3].append(v3[0])
#    return value
#
#    
#val = collectValue(result)

def valdb_destroy(dbName):
    '''
    This function destroys the given file. 
    Args:
        dbName: string of db file location
    Returns: 
        None
    '''
    import os,os.path
    if os.path.exists(dbName):
        os.remove(dbName)
        print 'db destroy',dbName,'succesful'
    else:
        print 'db destroy',dbName,'unsuccessful -- db not found'
        

def valdb_add(dbVal,dbName = 'Valdb.data'):
    import os.path,pickle
    if os.path.exists(dbName):
        db = pickle.load(open(dbName,'r'))
    else:
        db = {}
       
   
    db = dict_add(db,dbVal)

    pickle.dump(db,open(dbName,'w'))
#    print 'added to db: ',dbName
    return db

def valdb_wordcount_add(dbVal_wordcount,dbName = 'Valdb_wordcount.data'):
    import os.path,pickle
    if os.path.exists(dbName):
        db = pickle.load(open(dbName,'r'))
    else:
        db = []
       
   
    db = db + dbVal_wordcount

    pickle.dump(db,open(dbName,'w'))
#    print 'added to db: ',dbName
    return db

def getCount(v,lenCutoff = 0.8):
    label = ['total','num','num_text','text','num_text_short','num_text_long']
    countDict = dict.fromkeys(label, 0)
    countDict['total']=1
    # process Type feature
    if bool(re.search(r'\d', v)):
        if bool(re.search(r'[a-z]',v.lower())): 
            countDict['num_text']=1
        else:
            countDict['num']=1
    else:
        countDict['text']=1
        
    # process Length feature (lenth of text in num_text)
    if countDict['num_text']==1:
        s = ''.join([i for i in v if not i.isdigit()])
        if len(s)/len(v)>lenCutoff:
            countDict['num_text_long']=1
        else:
            countDict['num_text_short']=1
    return countDict
    
def getWordcount(countdict,v):
    # process Wordcount feature
    wordcount = []
    if countdict['text']==1:
        v = v.split(" ")  
        wordcount.append(len(v))         
        
    return wordcount      

def getScore(v,dbVal,dbVal_wordcount,countdict):
#    print dbVal,dbVal_wordcount
    score = {}
    score['Type'] = float((countdict['num']*dbVal['num'] + countdict['num_text']*dbVal['num_text'] + countdict['text']*dbVal['text']))/float(dbVal['total'])
  
    if countdict['num_text']==1:
        score['Length'] = float((countdict['num_text_long']*dbVal['num_text_long'] + countdict['num_text_short']*dbVal['num_text_short']))/float(dbVal['num_text'])
    else:
        score['Length'] = 1
    c = np.array(dbVal_wordcount)
    dbVal_wordcount.sort()
    med = dbVal_wordcount[len(dbVal_wordcount)/2]
    if c.std()!=0:
        score['Wordcount']=float((len(v.split(" "))-med))/float(c.std())
    else: 
        if len(v.split(" "))==med:
            score['Wordcount']=0
        else:
            score['Wordcount'] = 100
#    print score
    return score    

def valdb_add_result(val):
    dbVal = {}
    dbVal_wordcount = []
    score = defaultdict(list)
    i=0
    while i<len(val):
        v = val[i]
        countdict = getCount(v)
        dbVal = valdb_add(countdict)
        dbVal_wordcount = valdb_wordcount_add(getWordcount(countdict,v))
        score[i] = getScore(v,dbVal,dbVal_wordcount,countdict)

        i+=1
      
    
    return dbVal,dbVal_wordcount,score
            
if __name__ == '__main__':
    # val is a list of value corresponding to each key
    valdb_destroy('Valdb.data')    
    valdb_destroy('Valdb_wordcount.data')
    val = ['yes','no','yes','no','accept2','not accept'] #just for testing
    dbVal,dbVal_wordcount,score = valdb_add_result(val)
    
    
    
        