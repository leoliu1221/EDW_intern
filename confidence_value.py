# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 14:06:07 2015

@author: pwongcha
"""

from file_utilities import dict_add,getData3
from nltk.corpus import wordnet as wn
from collections import defaultdict
from confidence import keydb_marginal_load
import re
import numpy as np

def Syn_Ant(word):
    # get synonym and anytonym for an input word from wordnet 
    syn = []
    an = {}
    for i in wn.synsets(word):
        # i.lemmas() contain the synonym
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
    # add dbVal to the database dbName
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
    '''
    This function cleans the string key 
    Sample use:
        input : "(aaaa_)"
        output: []
        input : ""sere*sdf&sdf$sd#"
        output: ['sere sdf sdf sd']
    '''
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
    #now remove all non-alpha numeric values except _, replace by space. 
    key = re.sub('[^_/0-9a-zA-Z]+', ' ', key)
    key = key.split("_")[-1]
    
    # remove stopwords 
    words = key.split()
    no_stop_words = ""
    for word in words:
        if word not in stopwords.words():
            no_stop_words = no_stop_words + word + " "
    # remove last space
    pos = no_stop_words.rfind(' ')
    no_stop_words = no_stop_words[:pos]+no_stop_words[pos+1:]
    # return a string 
    return [no_stop_words]


def get_collection(data):
    # collect all data after extraction in order to be used as an input for calculating the value score
    from get_data_breast import checkAllcancer
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


def getScore(key,value,valdb = None,add=True):
    '''
    This function calculates the value score 
    # score_type : [0,1] among three types => (1) num, (2) text, (3) num_text
    # calculate proportion of a particular type of v with respect to the total frequency
    # The larger, the higher confidence
    #
    # score_length : only apply to num_text type (let score of other types to be 1)
    # calculate proportaion of long or short text with respect to total number of num_text type
    # The larger, the higher confidence
    #
    # score_wordcount : only apply to text type
    # calculate  absolute value of (word count for v - med of c and then divided by std.dev of c) where c is a vector of wordcount
    # The smaller, the higher confidence
    #
    # score_token : only apply to text type (Note: the value can be negative)
    # calculate the difference between frequency of particular token and equal portion (1/total number of tokens) where token is value
    # The larger, the higher confidence
    
    Sample use:
        input : key = 'tumor grade', value = '3'
        output: 'type 1.0 length 1 wordcount NA token NA'
    '''
    # load the "Valdb.data" database if the database is not specified 
    if valdb is None:
        valdb = keydb_marginal_load("Valdb.data")
    
    # add new data to the database
    # default is to add a new value to the database
    if add==True:
        dictInput = {key:[value]}
        valdb = valdb_add(dictInput)       
    
    score = {}
    dbVal = {}
    dbVal_wordcount = []
    
    # get frequency for current value 
    countdict = getCount(value)
    
    # get frequency for all value in valdb
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
    
    
    # Wordcount feature and Token feature : only apply to text type
    if countdict['text']==1:
        # Wordcount feature
        
        c = np.array(dbVal_wordcount) # c is a vector of word count
        dbVal_wordcount.sort()
        med = dbVal_wordcount[len(dbVal_wordcount)/2] # median of a vector containing word count
    # If std.dev(c) which is the denominator is not 0, calculate the score 
    # score = absolute value of (word count for value - med and then divided by std.dev of c)
        if c.std()!=0:
            score['Wordcount']=abs(float((len(value.split(" "))-med))/float(c.std()))
    # If std.dev(c) is 0: 
    #   check if word count of value is equal to med then set score to 0 (good case)
    #   otherwise, set score to be 100 (bad case)
        else: 
#            print 'value',value
            if len(value.split(" "))==med:
                score['Wordcount']=0
            else:
                score['Wordcount'] = 100
                
        # Token feature
        label = ['total','num','num_text','text','num_text_short','num_text_long']
        # token of value
        token = list(set(dbVal.keys())-set(label))
        token_combine = {}   # combine synonym and antonym with original word
        antonym = defaultdict(list)
        remove_item = {}
        
        for k in token:
            # if k has already included as synonym or antonym of other token, k is not get processed
            if k in remove_item.keys():
                continue
            flag = 0
            # collect synonym and antonym in syn and an, respectively
            syn,an = Syn_Ant(k)
            if an!={}:
                antonym[an.keys()[0]]=an.values()[0]\
                
            # If any item in token is synonym or antonym of k, combine frequency and remove that word from the token list.
            # Collect the new frequency in a token_combine dictionary
            for s in syn:            
                if str(s) in token and str(s)!=k :
                    remove_item[s]=k               
                    token_combine[k]=dbVal[k]+dbVal[str(s)]
                    flag = 1
          
            for key,val in an.iteritems():            
                if str(val) in token:
                    remove_item[val]=k               
                    token_combine[k]=dbVal[k]+dbVal[str(val)]  
                    flag = 1
     
            # If there is no synonym or antonym of k contained in token list, collect the frequency from dbVal
            if flag==0:
                token_combine[k]=dbVal[k]
          

        # Calculate the score for each element in the original token list
        for k in list(set(dbVal.keys())-set(label)): 
            #making sure k is always equal to v
            if k!=value:
                continue
            if token_combine.get(k) is not None:
                num_token = token_combine[k]
            else:
                num_token = token_combine[remove_item[k]]
    
            eq_portion = float(1)/float(len(token_combine))
            percentage = float(num_token)/float(dbVal['total'])
            score['Token'] = float(percentage-eq_portion)         
                
    # if value is not text type, Wordcount and Token features are "NA"           
    else:
        score['Wordcount'] = "NA"
        score['Token'] = "NA"

    # for a new data format (to be combined with Abstractor)   
    score_type = score['Type']      
    score_length = score['Length']
    score_wordcount = score['Wordcount']
    score_token = score['Token']
   
    #return {'type':score_type,'length':score_length,'wordcount':score_wordcount,'token':score_token}
    return ' '.join([str(item) for item in ['type',score_type,'length',score_length,'wordcount',score_wordcount,'token',score_token]])

def getCount(v,lenCutoff = 0.9):
    '''
    This function gets frequency of each label and each token
    Sample use:
        input : 'tumor'
        output: {'num': 0,
                 'num_text': 0,
                 'num_text_long': 0,
                 'num_text_short': 0,
                 'text': 1,
                 'total': 1,
                 'tumor': 1}
    '''
    
    label = ['total','num','num_text','text','num_text_short','num_text_long']  

    # if v is not already collected as token, consider it to be one of the token       
    if v not in label:
        label.append(v)
     
    # first initialize frequency of label to be 0
    countDict = dict.fromkeys(label, 0)
    # add 1 to 'total' label
    countDict['total']=1
    # add 1 to token v
    countDict[v]=1
    
    # process Type feature : num_text, num only or text only
    if bool(re.search(r'\d', v)):
        if bool(re.search(r'[a-z]',v.lower())): 
            countDict['num_text']=1
        else:
            countDict['num']=1
    else:
        countDict['text']=1
        
    # process Length feature (lenth of text in num_text)
    if countDict['num_text']==1:
        # s contains only a textual part in num_text 
        s = ''.join([i for i in v if not i.isdigit()])
        
        # consider proportion of length of textual part and total length
        # if the proportaion is greater than lenCutoff, count as long text. Otherwise, count it as short text
        if len(s)/len(v)>lenCutoff:
            countDict['num_text_long']=1
        else:
            countDict['num_text_short']=1
    return countDict


def baseDB(dbName = None):
    # create database valdb that collects historical data to be used as a base database 
    if dbName is None:
        dbName = 'Valdb.data'
    valdb_destroy(dbName)  
    from glob import glob
    files = glob('./data/*.csv')
    for f in files:
        data = getData3(f)   
        # create baseDB
        collection = get_collection(data)
        valdb = valdb_add(collection,dbName = dbName)
    return valdb

if __name__ == '__main__':
    pass
    '''
#    valdb = baseDB()
    # input : a key and value pair
    dictInput = {'tumor grade':['3']}
    
    # add new data to the database
    valdb = valdb_add(dictInput)
    
    # compute confidence score for value
    score = {}
    for k,v in dictInput.iteritems():
        score[k] = getScore(k,v[0],valdb,add=False)
    '''
    
