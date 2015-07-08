# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:45:59 2015

@author: sqltest
"""

import re


surr_threshold = 500
count=0; 
def get_all_occ(text,reg):
    '''
    get all occurences of reg. 
    Args:
        text: a string of input text
        reg: a string to find
    Returns:
        result: a list of (reg,index) pairs. index is the index of reg in the document
    '''
    
    matches = re.finditer(re.compile(reg),text)
    result = [(match.group(),(match.start()+match.end())/2) for match in matches]
    return result






def get_tnm(text,confFile = 'stageKeys.yaml'):
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
    result = {}
    for line in lines:
        textKeys = []
        for key in keywords:
            if key in text:
                textKeys.append(key)
        for stage in stages.keys():
           req = stages[stage].values()
           if meetReq(textKeys,req):
                if result.get(stage) == None:
                    result[str(stage)]=[]
                result[str(stage)].append(lineNum)
        lineNum+=1
    for key in result.keys():
        result[key] = list(set(result[key]))
    return result





def hasString(s,ss):
    '''
    This function checks if s has one of ss in it. 
    Args:
        s: a list of tokens of the input string
        ss: a list of list of strings to be checked. 
    Returns: 
        True if at least 1 word from ss is found in s
        False otherwise
    '''
    for wordl in ss:
        for word in wordl:
            if word in s:
                return True
    return False
def getString(s,ss):
    '''
    This function returns a list of words appear in s
    Args:
        s: a list of tokens of the input string
        ss: a list of list of strings to be checked. 
    Returns: 
        A list of word and number pair in ss thats in s
        empty list if none. 
        
    '''
    result = []
    for wordl in ss:
        for word in wordl:
            temp = get_all_occ(s,word)
            result.extend(temp)
    return result

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



def get_stage_num(text,stageKey,threshold=5):
    '''
    This function check whether cancer keyword is contained within the text
    If it does, return the stage of that cancer
    
    Args:
        text String of text to be captured (input)
        stageKey: regular expression used to capture, either 'grade' or 'stage'
    Returns:
        result: a dictionary of stage_num->[(lineNum1,position1) (lineNum2,position2) ...]
    '''
    #result is an empty dictionary 
    result = {}
    #just incase the text is not in lower case
    text = text.lower()
    #not sure if we need this
    #index = text.find(stageKey)
    #surr_text= surround(text,surr_threshold)
    # regex used to capture colon cancer - for now we will do for particular "colon cancer" problem
    #regex_cancer = '((colon|rectal|rectosigmoid|colorectal) (cancer|carcinoma))|(cancer|enocarcinoma.*colon|sigmoid)|colon neoplasm'
    #get the sentenses that contains the keyword 
    #lines are a list of sentenses where the keyword is in
    lines = text.split('.')
    stageKey = re.escape(stageKey)
    for lineNum in xrange(len(lines)):
        line_text = lines[lineNum]
        # using word boundary regex
#        stage_matches = re.finditer(re.compile(r'\b'+stageKey+r'\b'),line_text)
        # using pre-defined regex
        stage_matches = re.finditer(re.compile(r'[\s+.(]'+stageKey+'[\s+.:)]'),line_text)
        #in here stageKeys serve as a counter. 
        #It does not have anything to work on for later work
        for match in stage_matches:
            #stage_text = line_text[match.end():match.end()+5]
            stage_text = line_text
            stage_text = stage_text.replace("iv","4")  
            stage_text = stage_text.replace("iii","3")  
            stage_text = stage_text.replace("ii","2")  
            stage_text = stage_text.replace("i","1")  
            reObject = re.compile("\d")
            out = reObject.search(stage_text,match.start(),match.end()+threshold)
            #out = re.search(re.compile("\d"),stage_text)
            if out is None:
                print 'out is None for ',stageKey,'text: '+ stage_text
            else:
                stage_num = out.group()
                print 'match start:', match.start()
                print 'match end:',match.end()
                stage_index = ((out.start()+out.end())/2+(match.start()+match.end())/2)/2
                if result.get(stage_num)==None:
                    result[stage_num] = []
                result[stage_num].append((lineNum,stage_index))
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
    
def get_stage_from_pa(text,organ='colon',confFile = 'stageKeys.yaml',threshold=40):
    '''
    Check if a pa note has a stage associate with colon cancer
    Args:
        t: the string of staging to look at
        text: a string of input text
    Returns: 
        result: 
            a dictionary of stage -> line number
    '''
    import re
    #text = data[2009670][0][4]    
    if text.find('ajcc')==-1 and text.find('tnm')==-1:
        print 'cannot find keyword ajcc or tnm'
        return {}
    import yaml
    with open(confFile,'r') as f:
        cfg = yaml.load(f)
    #loading the stage and keyword from file 'stageKeys.yaml'
    try:
        stages = cfg[str(organ)+'stages']
    except:
        return {}
    keywords = cfg['keys']
    
    #1. try to get the ajcc from the text
    lines = text.split('.')
    lineNum=0
    
    for line in lines:
        #we are guessing tnm or ajcc is the keyword
        if 'tnm' in line or 'ajcc' in line:
            text = line
            break
        lineNum+=1
    tempKeys = get_all_occ(text,'tnm')
    tempKeys.extend(get_all_occ(text,'ajcc'))
    print tempKeys
    for tempKey in tempKeys:
        #text = surround(text,key[1],threshold=40)
      
        textKeys = []
        resultStages = []
        for key in keywords:
            pattern = re.compile(key)
            found_keys = pattern.finditer(text,int(tempKey[1])-threshold,int(tempKey[1])+threshold)
            found_keys = re.finditer(re.compile(key),text)
            for match in found_keys:
                textKeys.append((match.group(),(match.start()+match.end())/2))
        index=0
        for keypair in textKeys:
            index+=keypair[1]
        if len(textKeys)>0:
            index/=len(textKeys)
        #index/=len(textKeys)
        textKeys = [item[0] for item in textKeys]

        for stage in stages.keys():
            req = stages[stage].values()
            #print testKeys,stages[stage].values()
            #print 'comparing',testKeys,req,meetReq(testKeys,req)
            if meetReq(textKeys,req):
                #print 'met req!'
                resultStages.append(str(stage))
        result = {}
        for stage in resultStages:
            if result.get(stage)==None:
                result[stage]=[]
            result[stage].append((lineNum,index))
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
        Result: a dictionary of all organs found -> (sentence#,position) in the input
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
        if hasString(s,cancers):
            #organ is the organ name, 
            #num is the actual position in that line
            for organ,num in getString(s,organs):
                if result.get(organ)==None:
                    result[organ]=[]
                result[organ].append((sNum,num))
        sNum+=1
    for key in result.keys():
        result[key] = list(set(result[key]))
    return result
