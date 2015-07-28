# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:54:21 2015

@author: lliu5
"""

def create_key_db(result):
    '''
    Args: 
        Result is the previous result or stored result. 
        newKey: is the new key passed in.             
    '''
    db = {}
    #the result stores all keys for different cancers. 
    for record in result.values():
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
    db = create_key_db(result)