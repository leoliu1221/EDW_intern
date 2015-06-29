# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:45:59 2015

@author: sqltest
"""

import re


surr_threshold = 500
count=0; 
def hasString(s,ss):
    '''
    This function checks if s has one of ss in it. 
    Args:
        s: a list of tokens of the input string
        ss: a list of strings to be checked. 
    Returns: 
        True if at least 1 word from ss is found in s
        False otherwise
    '''
    if len(ss)<=len(s):
        for word in ss:
            if word in s:
                return True
        return False
    else:
        for word in s:
            if word in ss:
                return True
        return False
def getString(s,ss):
    '''
    This function returns a list of words appear in s
    Args:
        s: a list of tokens of the input string
        ss: a list of strings to be checked. 
    Returns: 
        A list of words in ss thats in s
        empty list if none. 
        
    '''
    if len(ss)<=len(s):
        return [word for word in ss if word in s]
    else:
        return [word for word in s if word in ss]
def surround(text,index,threshold=500):
    '''
    This function cuts of the surrounding of the text, return appropriate surround text
    Args: 
        text String of text to be cutted
        threshold: integer of surroundings needed
    Returns: 
        result: text strings from text where it shows the surround text
    '''    
    if index-threshold<0:
        start = 0;
    else:
        start = index-threshold
    if index+threshold>len(text):
        stop = len(text)
    else:
        stop = index+threshold
    return text[start:stop]



def get_stage_num(text,stageKey):
    '''
    This function check whether cancer keyword is contained within the text
    If it does, return the stage of that cancer
    
    Args:
        text String of text to be captured (input)
        stageKey: regular expression used to capture, either 'grade' or 'stage'
    Returns:
        result: a dictionary of stage_num->[lineNum1, lineNum2 ...]
    '''
    #result is an empty dictionary 
    result = {}
    #just incase the text is not in lower case
    text = text.lower()
    #not sure if we need this
    index = text.find(stageKey)
    #surr_text= surround(text,surr_threshold)
    # regex used to capture colon cancer - for now we will do for particular "colon cancer" problem
    #regex_cancer = '((colon|rectal|rectosigmoid|colorectal) (cancer|carcinoma))|(cancer|enocarcinoma.*colon|sigmoid)|colon neoplasm'
    #get the sentenses that contains the keyword 
    #lines are a list of sentenses where the keyword is in
    lines = text.split('.')
    for lineNum in xrange(len(lines)):
        stage_text = lines[lineNum]
        if stageKey in stage_text:
            stage_text = stage_text[stage_text.find(stageKey)+len(stageKey):]
            stage_text = stage_text.replace("iv","4")  
            stage_text = stage_text.replace("iii","3")  
            stage_text = stage_text.replace("ii","2")  
            stage_text = stage_text.replace("i","1")  
            out = re.search(re.compile("\d"),stage_text)
            if out is None:
                print 'out is None for ',stageKey,stage_text
            else:
                stage_num = out.group()
                if result.get(stage_num)==None:
                    result[stage_num] = []
                result[stage_num].append(lineNum) 
    #print 'out is:',out.group()
    return result  

def meetReq(keys,reqs):
    '''
    Check if the given key meet the requirement from reqs list. 
    Args:
        keys: a list of keys generated from text. 
        reqs: a list of requirements to check for in text. 
        Note: reqs can be nested, however the nested array will satisfy as long as 1 is good
    Returns: 
        True if all reqs satisfied
        False otherwise
    '''
    for req in reqs:
        if type(req) == type([]):
            for i in xrange(len(req)):
                if req[i] in keys:
                    break
                if i == len(req)-1:
                    return False
        else:
            if req not in keys:
                return False
    return True
        
def getAllStages(text):
    '''
    Args: 
        Text : String of text input
    Returns:
        stages: a list of numbers as stages
    '''
    stages = findStages('stage',text)
    stages.extend(findStages('grade',text))
    return stages
    
def get_stage_from_pa(text,confFile = 'stageKeys.yaml'):
    '''
    Check if a pa note has a stage associate with colon cancer
    Args: 
        text: a string of input text
    Returns: 
        result: 
            a dictionary of stage -> line number
            '''
    #text = data[2009670][0][4]    
    import yaml
    with open(confFile,'r') as f:
        cfg = yaml.load(f)
    #loading the stage and keyword from file 'stageKeys.yaml'
    stages = cfg['stages']
    keywords = cfg['keys']
    
    #1. try to get the ajcc from the text
    lines = text.split('.')
    lineNum=0
    for line in lines:
        if 'ajcc' in line:
            text = line
            break
        lineNum+=1
    #find all the keywords available
    textKeys = []
    resultStages = []
    for key in keywords:
        if key in text:
            textKeys.append(key)
    
    for stage in stages.keys():
        req = stages[stage].values()
        #print testKeys,stages[stage].values()
        #print 'comparing',testKeys,req,meetReq(testKeys,req)
        if meetReq(testKeys,req):
            #print 'met req!'
            resultStages.append(stage)
    result = {}
    for stage in resultStages:
        result[stage] = lineNum
    return result
    
#the test data is data[852359][0][4]
#get_cancer_type(data[852359][0][4])
def get_cancer_type(text,organs=None,oName='organList.txt',cName='cancerList.txt'):
    '''
    Args:
        text: string of an input text
        organs:A list of strings containig all the organs
        oName: A string of filename from which you can read organs from
        cName: A string of filename from which you read cancers from
    Returns:
        Result: a dictionary of all organs found -> sentence# in the input
    '''
    if organs is None:
        try:
            
            #just to see if we already have organList in our memory
            organs = organList
        except NameError:
            
            from file_utilities import readLines
            organs = readLines(oName)
            
        else:
            print 'loaded existing organ list from organList'
    #now read in all words similar to cancer
    cancers = readLines(cName)
    #we look for the keywords in each sentence
    text = text.split('.')
    #print text
    result = {}
    #sNum is the line number for string. 
    sNum=0
    for s in text:
        if hasString(s.split(),cancers):
            
            for organ in getString(s.split(),organs):
                if result.get(organ)==None:
                    result[organ]=[]
                result[organ].append(sNum)
        sNum+=1
    for key in result.keys():
        result[key] = list(set(result[key]))
    return result
            
    #now we have a complete list of all organs
    #we look for cancer keyword
