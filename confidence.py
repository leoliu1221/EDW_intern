# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:54:21 2015

@author: lliu5
"""
def keydb_destroy(dbName='db.data'):
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

def keydb_create(result,dbName='db.data'):
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
        db.update(get_key_freq(record))
    keydb_add(db)
    return db
    
def keydb_add(freqDict,dbName='db.data'):
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
    db.update(freqDict)
    pickle.dump(db,open(dbName,'w'))
    print 'added to db: ',dbName
    return db

def keydb_get_note(note,dbName='db.data'):
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
    return get_key_freq(record)

def get_key_freq(record):
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
        nice_looking_cancer = (' ').join(cancer.strip().lower().split())
        if db.get(nice_looking_cancer)==None:
            db[nice_looking_cancer] = {}
        for key in record[cancer].keys():
            key = key.strip().lower()
            #record actual big keys. 
            if '_' not in key:
                if db[nice_looking_cancer].get(key)==None:
                    db[nice_looking_cancer][key]=0
                db[nice_looking_cancer][key]+=1
            #now record sub keys
            else:
                keys = key.split('_')
                for tempKey in keys:
                    tempKey = tempKey.strip().lower()
                    if db[nice_looking_cancer].get(tempKey)==None:
                        db[nice_looking_cancer][tempKey]=0
                db[nice_looking_cancer][tempKey]+=1
    return db
     
    
if __name__ == '__main__':
    from get_data_breast import get_format_data
    from file_utilities import getData3
    data = getData3('data/ovarian.csv')
    data,result = get_format_data(data)
    db = keydb_create(result)
    ''' ALTERNATIVE WAYS TO GET DB'''
    ''' USING GET_KEY_FREQ ROUTINE
    db = {}
    for record in result.values():
        db.update(get_key_freq(record))
    keydb_add(db)
    ### USING ADD_NOTE_KEYDB ROUTINE
    db = {}
    for value[1] in data.values() as record:
        db.update(keydb_get_note(record))
    keydb_add(db)
    '''
        
    
    
    
    
    