# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:54:21 2015

@author: lliu5
"""
import time,re

from file_utilities import dict_add

    
def keydb_clean(key,returnString=False):
    key = key.lower()
    from nltk.corpus import stopwords
    #clean parenthesis
    #clean space
    #clean non-alpha
    #remove parenthesis, and the text within. 
    regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
    m = regEx.match(key)
    while m:
        key = m.group(1) + m.group(2)
        m = regEx.match(key)
        #print key
    #remove left parenthesis and the text within (till the end
    regEx = re.compile(r'([^\(]*) *(\(.*)')
    m = regEx.match(key)
    while m:
        #print key
        key = m.group(1)
        m=regEx.match(key)
    #now check if the key is empty
    key = key.strip()
    if key=='':
        return[]
    #now remove all non-alpha numeric values, replace by space. 
    key = re.sub('[^0-9a-zA-Z]+', ' ', key)
    words = key.split()
    no_stop_words = []
    for word in words:
        if word not in stopwords.words():
            no_stop_words.append(word)
    return sorted(no_stop_words)

def keydb_init(dbName='keydb.data'):
    keydb = keydb_load(dbName = dbName)
    if len(keydb)==0:
        keydb_add({},dbName = dbName)
    return keydb
    

def keydb_load(dbName='keydb.data'):
    import os.path,pickle
    db = {}
    if os.path.exists(dbName):
        db = pickle.load(open(dbName,'r'))
        print 'db load',dbName,'successful'
    else:
        print 'db load',dbName,'unsuccessful -- db not found'
    return db
    
    
def keydb_destroy(dbName='keydb.data'):
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

def keydb_add_result(result,dbName='keydb.data'):
    '''
    Args: 
        Result is the previous result or stored result. 
        newKey: is the new key passed in.   
    Returns:
        the db dictionary for all key frequencies          
    '''
    db = {}
    #the result stores all keys for different cancers. 
    for record in result.values():
       db = dict_add(db,keydb_core(record))
    db = keydb_add(db)
    return db

def keydb_add(freqDict,dbName='keydb.data'):
    '''
    Args:
        freqDict: the processed frequency dictinoary 
        dbName: The physical storage for the database
    Returns:
        None
    '''
    import os.path,pickle
    if os.path.exists(dbName):
        db = pickle.load(open(dbName,'r'))
    else:
        db = {}
    db = dict_add(db,freqDict)
    pickle.dump(db,open(dbName,'w'))
    print 'added to db: ',dbName
    return db
    #return db

def keydb_get_note(note,dbName='keydb.data'):
    '''
    Args:
        note: an actual pathology note from raw data. 
        dbName: The physical storage for the database
    Returns:
        Dictinoary of key frequencies
    '''
    from get_data_breast import checkAllcancer,get_section
    record = checkAllcancer(note)
    record['content'] = get_section(note)
    return keydb_core(record)    
    
def keydb_core(record):
    '''
    Args: 
        record: a result dictionary for 1 note. NOTE: it is not an actual note. 
        To use actual note, please use add_note_db instead
    Returns:
        db: a dictionary of key frequency from the given note result. 
    '''
    db = {}
    dbcount=0
    #db['*****dataponit_count*****']=0
    for cancer in record.keys():
        if cancer == 'content':
            continue
        #we dont need the nice looking cancer now. We only need key-number pairs for our database. 
        #nice_looking_cancer = (' ').join(cancer.strip().lower().split())
        #if db.get(nice_looking_cancer)==None:
        #    db[nice_looking_cancer] = {}
        for key in record[cancer].keys():
            key = key.strip().lower()
            if key.strip()=='':
                continue
            #record actual big keys. 
            if '_' not in key:
                key = ' '.join(keydb_clean(key))
                if key.strip()=='':
                    continue
                if db.get(key)==None:
                    db[key]=0
                db[key]+=1
                dbcount+=1
            #now record sub keys
            else:
                dbcount+=1
                keys = key.split('_')
                for tempKey in keys:
                    tempKey = ' '.join(keydb_clean(tempKey))
                    if tempKey=='':
                        continue
                    if db.get(tempKey)==None:
                        db[tempKey]=0
                    db[tempKey]+=1
                    
    db['*****datapoint_count*****']=dbcount
    return db
    
def keydb_marginal_destroy(dbName = 'keydb_marginal.data'):
    '''
    ^^ reusing keydb_destroy
    '''
    keydb_destroy(dbName=dbName)
    
    
def keydb_marginal_load(dbName='keydb_marginal.data'):
    '''
    ^^ reusing keydb_load
    '''
    return keydb_load(dbName = dbName)
    
    
def keydb_marginal_add(key,value,dbName='keydb_marginal.data'):
    keys = keydb_marginal_core(key)
    marginal_dict = {}
    for k in keys:
        marginal_dict[k] = value
    return keydb_add(marginal_dict,dbName=dbName)
def keydb_marginal_add_data(data,dbName='keydb_marginal.data'):
    for value in data.values():
        note = value[1]
        keydb_marginal_add_note(note,dbName=dbName)
    return keydb_marginal_load()
    
def keydb_marginal_add_note(note,dbName='keydb_marginal.data'):
    keydb = keydb_get_note(note)
    return keydb_marginal_add_db(keydb)

def keydb_marginal_add_db(keydb,dbName='keydb_marginal.data'):
    for key,value in keydb.items():
        keydb_marginal_add(key,value)
    return keydb_marginal_load()

def keydb_marginal_core(key):
    ###############################################
    #for single key
    ###############################################
    import itertools
    if key == '*****datapoint_count*****':
        return [(key)]
    no_stop_words = keydb_clean(key)
    resultKeys = []
    if len(no_stop_words)>6:
        return []
    for i in xrange(len(no_stop_words)+1):
        if i==0:
            continue
        for combination in itertools.combinations(no_stop_words,i):
            resultKeys.append(tuple(sorted(list(combination))))
    return resultKeys
    
def keydb_marginal_marginal(key,marginaldb = None):
    if '_' in key:
        key = key.split('_')[-1]
    if marginaldb is None:
        marginaldb = keydb_marginal_load()
    keys = keydb_clean(key)
    result = 1
    total = marginaldb['*****datapoint_count*****']
    for k in keys:
        if marginaldb.get(tuple([k]))==None:
            print k,'is not found in marginal db'
            return 0
        if float(marginaldb[tuple([k])])>total:
            result*=1
        else:
            result*=(float(marginaldb[tuple([k])])/total)
    return result
    
def keydb_marginal_chained(key,marginaldb=None):
    if '_' in key:
        key = key.split('_')[-1]
    if marginaldb is None:
        marginaldb = keydb_marginal_load()
    total = marginaldb['*****datapoint_count*****']
    keys = keydb_clean(key)
    if len(keys)==0:
        return 0.0
    chain = tuple(sorted(keys))
    if marginaldb.get(chain)==None:
        return 0
    #print 'chain',chain
    return float(marginaldb.get(chain))/total

def keydb_marginal_newkey(key,marginaldb=None):
    if '_' in key:
        key = key.split('_')[-1]
    if marginaldb is None:
        marginaldb = keydb_marginal_load()
    
    marginal = keydb_marginal_marginal(key,marginaldb=marginaldb)
    chained = keydb_marginal_chained(key,marginaldb=marginaldb)
    '''    
    if marginal == 0:
        return 0
    if chained-marginal==0:
        if len(keydb_clean(key))==1:
            return float("inf")
    '''
    return {'chained':chained,'marginal':marginal}
    
    
    
if __name__ == '__main__':
    start = time.time()
    from get_data_breast import get_format_data
    from file_utilities import getData3
    
    data = getData3('data/ovarian.csv')     
    data,result = get_format_data(data)
    keydb_destroy()    
    keydb_marginal_destroy()
    testNote = '\nUTERINE CANCER STAGING SUMMARY\nd0 d1:data1\nd0 d1 d3:data3\nd1 d2: data2\nd1 d2: data3\n\nAmerican Joint Committee on Cancer (2009) Tumor-Node-Metastasis (TNM) staging for endometrial cancer:\nTumor (T):\t\tpT1a\nNodes (N):\t\tpN0\nMetastasis (M):\tpMX\n\n'
    testResult = keydb_get_note(testNote)
    marginal_result = result
    i=-1
    for value in data:
        i+=1
        keydb_marginal_add_note(value[1])
    
    marginaldb = keydb_marginal_load()
    for key1,value1 in result.items():
        for key2,value2 in value1.items():
            if key2 == 'content':
                continue
            else:
                for key in value2.keys():
                    marginal_result[key1][key2][key] = keydb_marginal_newkey(key,marginaldb=marginaldb)
                                        

    
    
    '''
    keydb_add_result(result)
    keydb = keydb_load()
    keydb_marginal_destroy()
    keydb_marginal_add_db(keydb)
    marginaldb = keydb_marginal_load()
    cResult = {}
    test = result[1][result[1].keys()[1]].keys()[0]
    
    marginal = keydb_marginal_marginal(test)
    chained = keydb_marginal_chained(test)
    
    '''
    
    ''' ALTERNATIVE WAYS TO GET DB'''
    ''' USING GET_KEY_FREQ ROUTINE
    db = {}
    for record in result.values():
        db=dict_add(db,get_key_freq(record))
    keydb_add(db)
    ### USING ADD_NOTE_KEYDB ROUTINE
    db = {}
    for value[1] in data.values() as record:
        db=dict_add(db,keydb_get_note(record))
    keydb_add(db)
    '''
        
    
    
    
    elapsed = time.time()-start
    print 'finished exectuing. elapsed time=',elapsed,'s'
    
    
    