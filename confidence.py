# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:54:21 2015

@author: lliu5
"""
import time,re

from file_utilities import dict_add
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
                if db.get(key)==None:
                    db[key]=0
                db[key]+=1
            #now record sub keys
            else:
                keys = key.split('_')
                for tempKey in keys:
                    tempKey = tempKey.strip().lower()
                    if tempKey=='':
                        continue
                    if db.get(tempKey)==None:
                        db[tempKey]=0
                    db[tempKey]+=1
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
    from nltk.corpus import stopwords
    import itertools
    #remove parenthesis, and the text within. 
    regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
    m = regEx.match(key)
    while m:
        key = m.group(1) + m.group(2)
        m = regEx.match(key)
        #print key
    #now check if the key is empty
    key = key.strip()
    if key=='':
        return[]
    #now remove all non-alpha numeric values, replace by space. 
    key = re.sub('[^0-9a-zA-Z]+', ' ', key)
    #now we know the key does not have prethesis, and the key has some values. 
    words = key.split()
    no_stop_words = []
    for word in words:
        if word not in stopwords.words():
            no_stop_words.append(word)
    resultKeys = []
    if len(no_stop_words)>5:
        return []
    for i in xrange(len(no_stop_words)+1):
        if i==0:
            continue
        for combination in itertools.combinations(no_stop_words,i):
            resultKeys.append(tuple(sorted(list(combination))))
    return resultKeys

    
    
if __name__ == '__main__':
    start = time.time()
    from get_data_breast import get_format_data
    from file_utilities import getData3
    keydb_destroy()
    if 'data' not in locals():
        data = getData3('data/ovarian.csv')
    if 'result' not in locals():
        data,result = get_format_data(data)
    keydb_add_result(result)
    keydb = keydb_load()
    keydb_marginal_destroy()
    keydb_marginal_add_db(keydb)
    marginaldb = keydb_marginal_load()
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
    
    
    