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


def cancer_capture(text,regex,threshold=30):
    '''
    This function check whether cancer keyword is contained within the text
    If it does, return the stage of that cancer
    
    Args:
        text String of text to be captured (input)
        regex: regular expression used to capture
        threshold: int of distance for the surrounding text to search for number after keyword appears
            Defaults to 15
    Returns:
        out.group(): an integer representing stage of the cancer
        out.end()-1: the index at which the stage number was found
    '''
    index = text.find(regex)
    surr_text= surround(text,surr_threshold)
    # regex used to capture colon cancer - for now we will do for particular "colon cancer" problem
    regex_cancer = '((colon|rectal|rectosigmoid|colorectal) (cancer|carcinoma))|(cancer|enocarcinoma.*colon|sigmoid)|colon neoplasm'
    out_cancer = re.findall(re.compile(regex_cancer),surr_text)
    if len(out_cancer)<=0:
        return None,index+len(regex)

    stage_text = text[index:index+threshold].replace("iv","4")
    stage_text = stage_text.replace("iii","3")
    stage_text = stage_text.replace("ii","2")
    stage_text = stage_text.replace("i","1")
    out = re.search(re.compile("\d"),stage_text)

    if out is None:
        #print 'out is None for ',regex
        return None,index+threshold
    #print 'out is:',out.group()
    return out.group(),int(out.end())-1  

def findStages(reg,text):
    '''
    find the stage and its number in the text based on the regex. 
    The regex can be stage or grade. 
    Args:
        reg: 'stage' or 'grade' it is the keyword we look for. 
        text: string of text we want to find reg in. 
    Returns:
        output: a list of stage number found in the given text.
    Note: 
        if there is no match, then output is a empty list
    '''
    if text is None:
        return []
    if reg!='stage' and reg!='grade':
        return []
    if len(text)==0:
        return []
    output = []
    regex=reg
    text = text.lower()
    pattern=re.compile(regex)
    out=re.findall(pattern,text)
    current_text = text
    if len(out)>0:
        for t in out:
            stage,ind = cancer_capture(current_text,'stage')
            if stage is not None:
                output.append(stage)
            #print 'stage is:',stage
            #print 'index is :',ind
            current_text = current_text[ind+1:]
        return output
    else:
        return []
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
    
def getStageFromPa(text,confFile = 'stageKeys.yaml'):
    '''
    Check if a pa note has a stage associate with colon cancer
    Args: 
        text: a string of input text
    Returns: 
        resultStage: 
            a list containing all identified stages in string
            If not found, return emptry list of string
    '''
    #text = data[2009670][0][4]    
    import yaml
    with open(confFile,'r') as f:
        cfg = yaml.load(f)
    #loading the stage and keyword from file 'stageKeys.yaml'
    stages = cfg['stages']
    keywords = cfg['keys']
    
    #1. try to get the ajcc from the text
    ind = text.find('ajcc')
    text = text[ind:]
    text = text[:text.find('.')]
    #find all the keywords available
    testKeys = []
    resultStages = []
    for key in keywords:
        if key in text:
            testKeys.append(key)
    
    for stage in stages.keys():
        req = stages[stage].values()
        #print testKeys,stages[stage].values()
        #print 'comparing',testKeys,req,meetReq(testKeys,req)
        if meetReq(testKeys,req):
            #print 'met req!'
            resultStages.append(stage)
    return resultStages 
    
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

    
    
       
    
    
    

'''
Example main usage
from collections import defaultdict
output_stage = defaultdict(list)
output_grade = defaultdict(list)
check = defaultdict(list)
inputfile = open("input_test.txt")
input = inputfile.read()

text_in = input.split("\n")

import os
os.system('del outfile.txt')
os.system('del outfile_err.txt')

outfile=open("outfile.txt","a")
outfile_err=open("outfile_err.txt","a")
#i is the number of document we currently working on
i=0
while i<len(text_in):
    stageResult = findStages('stage',text_in[i])
    gradeResult = findStages('grade',text_in[i])
    for stage in stageResult:    
        output_stage[i].append(stage)
        check[i].append(text_in[i])
    for stage in gradeResult:    
        output_grade[i].append(stage)
    i+=1
'''

