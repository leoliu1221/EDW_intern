# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 16:54:21 2015

@author: lliu5
"""
import time,re

from file_utilities import dict_add,get_name
import numpy as np

from collections import defaultdict
#now comes the global variables

import nltk
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer

#see which languages are supported:
#print(" ".join(SnowballStemmer.languages))
LANGUAGE= 'english'
stemmer = SnowballStemmer(LANGUAGE)

#Uasage: top_dict(keydb_marginal_load('breast.data'),20)
def top_dict(dict,num):
    if num<=0:
        return []
    temp_arr = [[dict[key],key] for key in dict.keys()]
    return sorted(temp_arr,reverse=True)[0:num]
    
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
        #print key
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
    if returnString:
        return key
    if key=='':
        return[]
    #now remove all non-alpha numeric values, replace by space. 
    key = re.sub('[^0-9a-zA-Z]+', ' ', key)
    words = key.split()
    no_stop_words = []
    for word in words:
        #now do stemming
        word = stemmer.stem(word)
        if word not in stopwords.words():
            no_stop_words.append(word)
    return sorted(no_stop_words)

def keydb_init(dbName='keydb.data'):
    keydb = keydb_load(dbName = dbName)
    if len(keydb)==0:
        keydb_add({},dbName = dbName)
    return keydb
    

def keydb_load(dbName='keydb.data',keydb_folder = './keydb/'):
    '''
    this function looks for data files in keydbFolder or in current directory. 
    the default keydb_folder is './keydb/'    
    '''
    import os.path,cPickle as pickle
    db = {}
    if os.path.exists(dbName):
        db = pickle.load(open(dbName,'r'))
        #print 'db load',dbName,'successful'
    elif os.path.exists(keydb_folder+dbName):
        dbName = keydb_folder+dbName
        db = pickle.load(open(dbName,'r'))
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
    import os.path,cPickle as pickle
    if os.path.exists(dbName):
        db = pickle.load(open(dbName,'r'))
    else:
        db = {}
    db = dict_add(db,freqDict)
    pickle.dump(db,open(dbName,'w'))
    #print 'added to db: ',dbName
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
    #specimens are not important any more. 
    #record['content'] = get_section(note)
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
    dpcount=0
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
                dpcount+=1
            #now record sub keys
            else:
                dpcount+=1
                keys = key.split('_')
                for tempKey in keys:
                    tempKey = ' '.join(keydb_clean(tempKey))
                    if tempKey=='':
                        continue
                    if db.get(tempKey)==None:
                        db[tempKey]=0
                    db[tempKey]+=1
                    
    db['*****datapoint_count*****']=dpcount
    db['*****note_count*****']=1
    
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
    

def keydb_marginal_add(key=None,value=None,dbName='keydb_marginal.data',noteDict = None):
    if noteDict is None:
        #if a note dict does not present
        if key is None or value is None:
            return {}
        keys = keydb_marginal_core(key)
        marginal_dict = {}
        for k in keys:
            if marginal_dict.get(k) == None:
                marginal_dict[k]=0
            marginal_dict[k] += value
        
        return keydb_add(marginal_dict,dbName=dbName)
    else:
        #this is for adding a note dict. 
        
        marginal_dict = {}
        for key,value in noteDict.items():
            keys = keydb_marginal_core(key)
            for k in keys:
                if marginal_dict.get(k)==None:
                    marginal_dict[k]=0
                marginal_dict[k]+=value
        return keydb_add(marginal_dict,dbName = dbName)
        
        
def keydb_marginal_add_data(data,dbName='keydb_marginal.data'):
    for value in data.values():
        note = value[1]
        keydb_marginal_add_note(note,dbName=dbName)
    return keydb_marginal_load()
    
def keydb_marginal_add_note(note,dbName='keydb_marginal.data'):
    #first get the keydb from keydb_get_note 
    #now keydb stores all frequencies of keys
    keydb = keydb_get_note(note,dbName = dbName)
        
    
    return keydb_marginal_add_db(keydb,dbName = dbName)

def keydb_marginal_add_db(keydb,dbName='keydb_marginal.data'):
    keydb_marginal_add(noteDict=keydb,dbName=dbName)
    #############################
    # you can also do key value pairs for each
    #less efficiently:
    ##############################    
    #for key,value in keydb.items():
    #    keydb_marginal_add(key=key,value=value,dbName=dbName)
    ##############################
    return keydb_marginal_load(dbName = dbName)

def keydb_marginal_core(key):
    ###############################################
    #for single key
    ###############################################
    import itertools
    if key == '*****datapoint_count*****':
        return [(key)]
    if key=='*****note_count*****':
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
    ###########################
    #getting the marginal probability
    ##########################
    if '_' in key:
        key = key.split('_')[-1]
    if marginaldb is None:
        marginaldb = keydb_marginal_load()
    keys = keydb_clean(key)
    result = 1
    total = marginaldb['*****datapoint_count*****']
    for k in keys:
        if marginaldb.get(tuple([k]))==None:
            #print k,'is not found in marginal db'
            return 0
        if float(marginaldb[tuple([k])])>total:
            result*=1
        else:
            result*=(float(marginaldb[tuple([k])])/total)
    return result
    
def keydb_marginal_chained(key,marginaldb=None):
    ###########################
    #getting the chanied probability
    ##########################
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
        print chain, 'not found'
        return 0.0
    #print 'chain',chain
    return float(marginaldb.get(chain))/total

def keydb_marginal_newkey(key,marginaldb=None):
    ###########################
    #insertring a new key
    ##########################
    result = 0
    if '_' in key:
        key = key.split('_')[-1]
    if marginaldb is None:
        marginaldb = keydb_marginal_load()
    
    marginal = keydb_marginal_marginal(key,marginaldb=marginaldb)
    chained = keydb_marginal_chained(key,marginaldb=marginaldb)
       
    if marginal == 0:
        result = 0
    elif chained-marginal==0:
        if len(keydb_clean(key))==1:
            result= float("inf")
        else:
            result = 0
    else:
        result = round((chained-marginal)/marginal,4)
    
    #return {'chained':chained,'marginal':marginal,'chain-marg':result}
    return ' '.join([str(item) for item in ['chained',chained,'marginal',marginal,'chain-marg',result]])
######################################################################
# Below are value score calculations. 
######################################################################
def Syn_Ant(word):
    syn = []
    an = {}
    for i in wn.synsets(word):
        for j in i.lemmas():
            syn.append(j.name())
            if j.antonyms():
                an[j.name()]=j.antonyms()[0].name()
    syn = list(set(syn))
    return syn,an
    
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

def getCount(v,lenCutoff = 0.9):
    label = ['total','num','num_text','text','num_text_short','num_text_long']        
    if v not in label:
        label.append(v)
        
    countDict = dict.fromkeys(label, 0)
    countDict['total']=1
    countDict[v]=1
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
    score = {}
    # Type feature: calculate proportion of a particular type of v with respect to the total frequency
    score['Type'] = float((countdict['num']*dbVal['num'] + countdict['num_text']*dbVal['num_text'] + countdict['text']*dbVal['text']))/float(dbVal['total'])
  
    # Length feature: only apply to num_text type (let score of other types to be 1)
    # calculate proportaion of long or short text with respect to total number of num_text type
    if countdict['num_text']==1:
        score['Length'] = float((countdict['num_text_long']*dbVal['num_text_long'] + countdict['num_text_short']*dbVal['num_text_short']))/float(dbVal['num_text'])
    else:
        score['Length'] = 1
    
    if countdict['text']==1:
        # Wordcount feature
        c = np.array(dbVal_wordcount) # c is a vector of word count
        dbVal_wordcount.sort()
        med = dbVal_wordcount[len(dbVal_wordcount)/2] # median of a vector containing word count
    # If std.dev(c) which is the denominator is not 0, calculate the score 
    # score = absolute value of (word count for v - med and then divided by std.dev of c)
        if c.std()!=0:
            score['Wordcount']=abs(float((len(v.split(" "))-med))/float(c.std()))
    # If std.dev(c) is 0: 
    #   check if word count of v is equal to med then set score to 0 (good case)
    #   otherwise, set score to be 100 (bad case)
        else: 
            if len(v.split(" "))==med:
                score['Wordcount']=0
            else:
                score['Wordcount'] = 100
                
        # Token feature
        label = ['total','num','num_text','text','num_text_short','num_text_long']
        # token of v 
        token = list(set(dbVal.keys())-set(label))
        token_combine = {}   # combine synonym and antonym with original word
        antonym = defaultdict(list)
        remove_item = {}
        
        for k in token:
            if k in remove_item.keys():
                continue
            flag = 0
            syn,an = Syn_Ant(k)
            if an!={}:
                antonym[an.keys()[0]]=an.values()[0]
            # If any item in token is synonym or antonym of k, combine frequency and remove that word from the token list.
            # Collect the new frequency in a token_combine dictionary
            for s in syn:            
                if str(s) in token and str(s)!=k :
                    remove_item[s]=k               
                    token_combine[k]=dbVal[k]+dbVal[str(s)]
                    #token.remove(str(s))
                    flag = 1
          
            for key,val in an.iteritems():            
                if str(val) in token:
                    remove_item[val]=k               
                    token_combine[k]=dbVal[k]+dbVal[str(val)]  
                    #token.remove(str(val))
                    flag = 1
     
            # If there is no synonym or antonym of k contained in token list, collect the frequency from dbVal
            if flag==0:
                token_combine[k]=dbVal[k]
          
    #    print token_combine,"\nflag",flag
        # Calculate the score for each element in the original token list
        for k in list(set(dbVal.keys())-set(label)): 
            #making sure k is always equal to v
            if k!=v:
                continue
            if token_combine.get(k) is not None:
                num_token = token_combine[k]
            else:
                num_token = token_combine[remove_item[k]]
    
            eq_portion = float(1)/float(len(token_combine))
            percentage = float(num_token)/float(dbVal['total'])
            score['Token'] = float(percentage-eq_portion)         
                

    else:
        score['Wordcount'] = "NA"
        score['Token'] = "NA"

           
    return score    

def valdb_add_result(val):
    dbVal_local = {}
    dbVal_wordcount_local = []
    score = defaultdict(list)
      
    i=0
    while i<len(val):
        v = val[i]    
        # get frequency count (multiple values of them) for value v and add to database dbVal
        countdict = getCount(v)
        dbVal_local = valdb_add(countdict)
        # get wordcount for value v and add to database dbVal_wordcount
        dbVal_wordcount_local = valdb_wordcount_add(getWordcount(countdict,v))
        score[i] = getScore(v,dbVal_local,dbVal_wordcount_local,countdict)
        i+=1
      
    
    return dbVal_local,dbVal_wordcount_local,score
    
def score_fromdb(val):
    dbVal_local = {}
    dbVal_wordcount_local = []
    score = defaultdict(list)
      
    for v in val:   
        # get frequency count (multiple values of them) for value v and add to database dbVal
        countdict = getCount(v)
        dbVal_local = valdb_add(countdict)
        # get wordcount for value v and add to database dbVal_wordcount
        dbVal_wordcount_local = valdb_wordcount_add(getWordcount(countdict,v))
    i=0
    while i<len(val):
        v = val[i]
        countdict = getCount(v)
        score[i] = getScore(v,dbVal_local,dbVal_wordcount_local,countdict)
        i+=1
    
    return dbVal_local,dbVal_wordcount_local,score
    
    

def keydb_build():
    '''
    this function is for building all keydbs from all csvs from /data folder. 
    when the build finishes, you will have all *.data where * is the cancer name. 
    '''
    from get_data_breast import get_format_data
    from file_utilities import getData3
    start = time.time()
    start0 = start
    times = []
    #times is an array of 1 tuple, for each of the time there is an explanation. 

    '''
    #clean all databases
    keydb_destroy()    
    keydb_marginal_destroy()
    elapsed = time.time()-start
    print 'destroy keydb and marginal db finished. elapsed time=',elapsed,'s'
    times.append((['destroy keydb and marginal db',elapsed]))    
    start = time.time()    
    '''
    
    
    #get file list
    from glob import glob
    files = glob('./data/*.csv')
    
    #lengths = []
    for f in files:
        #destroy the keydb for each data
        keydb_marginal_destroy(get_name(f)+'.data')
        #continue
        #get data
        data = getData3(f)     
        data,result = get_format_data(data)
        #lengths.append([f,len(data)])
        #continue
        elapsed = time.time()-start
        print 'laoding data finished. elapsed time=',elapsed,'s'   
        times.append((['loading data '+get_name(f),elapsed]))
        start = time.time()
        
    
        
        ###################test
        #testNote = '\nUTERINE CANCER STAGING SUMMARY\nd0 d1:data1\nd0 d1 d3:data3\nd1 d2: data2\nd1 d2: data3\n\nAmerican Joint Committee on Cancer (2009) Tumor-Node-Metastasis (TNM) staging for endometrial cancer:\nTumor (T):\t\tpT1a\nNodes (N):\t\tpN0\nMetastasis (M):\tpMX\n\n'
        #testResult = keydb_get_note(testNote)
        #keydb_marginal_add_note(testNote)
        #realResult = testResult.copy()
        #for key in testResult.keys():
        #    realResult[key]= keydb_marginal_newkey(key)
        ###################test over
        

        #load value  
        i=0
        for value in data:
            i+=1
            tempStart = time.time()
            
            keydb_marginal_add_note(value[1])
            print i,'/',len(data), time.time() - tempStart            
            #valdb_add_note(value[1])
            
        
        
        elapsed = time.time()-start
        print 'add note to marginal db finished. elapsed time=',elapsed,'s'   
        times.append((['adding data ' +get_name(f),elapsed]))
        start = time.time()
        
        '''
        #detect keys, excluding those of content
        marginal_result=result.copy()
        marginaldb = keydb_marginal_load()
        valuedb = valuedb_load()
        for key1,value1 in result.items():
            for key2,value2 in value1.items():
                if key2 == 'content':
                    continue
                else:
                    for key in value2.keys():
                        marginal_result[key1][key2][key]['keyscore'] = keydb_marginal_newkey(key,marginaldb=marginaldb)
                        marginal_result[key1][key2][key]['valuescore'] = valuedb_newvalue(value2[key],valuedb = valuedb)
                        
        elapsed = time.time()-start
        print 'detecting key finished. elapsed time=',elapsed,'s'  
        times.append((['detecting data',elapsed]))
        start = time.time()                               
        '''
        
        
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
            
        
        
        
        elapsed = time.time()-start0
        print 'finished exectuing. elapsed time=',elapsed,'s'
        times.append(['total time '+get_name(f),elapsed])
    print(times)
    
if __name__ == '__main__':
    keydb_build()
        
    
    
    
