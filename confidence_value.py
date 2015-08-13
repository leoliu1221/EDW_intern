# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 14:06:07 2015

@author: pwongcha
"""

from file_utilities import dict_add,getData3
from nltk.corpus import wordnet as wn
from get_data_breast import checkAllcancer
from collections import defaultdict
import re
import numpy as np

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


def keydb_clean_string(key,returnString=False):
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
    key = re.sub('[^_/0-9a-zA-Z]+', ' ', key)
    key = key.split("_")[-1]
    
    words = key.split()
    no_stop_words = ""
    for word in words:
        if word not in stopwords.words():
            no_stop_words = no_stop_words + word + " "
    pos = no_stop_words.rfind(' ')
    no_stop_words = no_stop_words[:pos]+no_stop_words[pos+1:]
    return [no_stop_words]


def get_collection(data):
    collection = {}
    i=0
    while i<len(data):
        input_dict = checkAllcancer(data[i][1])
        for item in input_dict.values():
            for k in item.keys():
                k_clean = keydb_clean_string(k)
                if len(k_clean)==0:
                    break
                k_clean = k_clean[0]
#                k_clean = k                          
                value = item[k][0]
                if value!='' and value!="_":
                    if collection.get(k_clean)==None:
                        collection[k_clean]=[]
                    value = value.replace("_","")
                    collection[k_clean].append(value.lower())
        i+=1
    return collection


def getScore(key,value,valdb):
    score = {}
    dbVal = {}
    dbVal_wordcount = []
    countdict = getCount(value)
    for k,v in valdb.iteritems():
        if k==key:
            for v2 in valdb[k]:              
                countdict_current = getCount(v2)
                dbVal = dict_add(countdict_current,dbVal)
                if countdict_current['text']==1:
                    dbVal_wordcount.append(len(v2.split(" ")))
                
    
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


def baseDB(dbName = None):
    if dbName is None:
        dbName = 'Valdb.data'
    valdb_destroy(dbName)  
    data = getData3()   
    # create baseDB
    collection = get_collection(data)
    valdb = valdb_add(collection,dbName = dbName)
    return valdb

if __name__ == '__main__':
    
    valdb = baseDB()
    # input : a key and value pair
    dictInput = {'tumor grade':['3']}
    
    # add new data to the database
    valdb = valdb_add(dictInput)
    
    # compute confidence score for value
    score = {}
    for k,v in dictInput.iteritems():
        score[k] = getScore(k,v[0],valdb)
    
