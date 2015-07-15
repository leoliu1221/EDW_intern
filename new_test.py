# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:25:01 2015

@author: sqltest
"""

from file_utilities import getData3
import re
#find the first A. in the text
#read to the start of 'Invasive Breast Cancer Staging Summary'
def get_section(text):
    '''
    Find the sections such as A: B: C: ... 
    Args: text a stirng a text to fimd section in. 
    Returns:
        Result:  result['A']['content'], result['A']['title'],result['B']['content'].....
                 'content' -> ['a','b','c']
                 'title' -> 'title'
    '''
    matchA = re.compile('A\.')
    indStart = None
    for match in matchA.finditer(text):
        if text[match.start()+2]!='\n':
            indStart = match.start()
            break
    if indStart==None:
        matchA = re.compile('A\t')
        for match in matchA.finditer(text):
            if text[match.start()+2]!='\n':
                indStart = match.start()
                break
    if indStart is None:
        return {},{}
    
    
    #indStart = text.find('A.')
    #print 'indStart is working good'
    if indStart=='-1':return {}
    indEnd = text.lower().rfind('staging summary')
    if indEnd == -1 or indEnd<=indStart:
        section = text[indStart:]
    else:
        section = text[indStart:indEnd]
    alpha = re.compile('[A-Z][\t\\.]')
    matches = []
    prev = None
    for match in alpha.finditer(section):
        if prev is None:
            if match.group()[0]!='A':
                continue
            #added check for if the next character is line break then this [A-Z]\. is definately not what we wanted
            if section[match.end()]=='\n':
                continue
            prev = match.group()[0]
        elif ord(match.group()[0])-ord(prev)!=1:
            continue
        if section[match.end()]=='\n':
            continue
        matches.append([match.group(),match.start(),match.end()])
        prev = match.group()[0]
    
    result = {}
    for i in xrange(len(matches)):
        if i == len(matches)-1:
            result[matches[i][0]] = section[matches[i][2]:]
        else:
            result[matches[i][0]] = section[matches[i][2]:matches[i+1][1]]
    #now do some more data cleaning. Starting from the second line of result for last member. 
    
    if len(result.keys())>0:
        processTexts = result[sorted(result.keys())[-1]].split('\n')
        for i in xrange(len(processTexts)):
                if i ==0: continue
                #print processTexts[i]
                #print '[',processTexts[i].strip(),']'
                if len(processTexts[i].strip())<1:
                    textOut = '\n'.join(processTexts[0:i])
                    result[sorted(result.keys())[-1]] = textOut
                    break
                if processTexts[i].strip()[0]=='-':
                    continue
                if processTexts[i].strip()[0]=='?':
                    continue
                textOut = '\n'.join(processTexts[0:i])
                result[sorted(result.keys())[-1]] = textOut
                break
    
    return result,matches
            
            
def qa(result):
    '''
    checking for code quality. 
    How many \t were recognized, and how many did not find. Print out the numbers. 
    Args: 
        result -- the result dict
    Returns:
        None        
    '''        
    countTab = 0
    countEmpty = 0
    for row,item in result.items():
        if len(item.keys())==0:
            countEmpty +=1
            print row,'has empty result'
        for key in item.keys():
            if '\t' in key:
                countTab+=1
                print row, 'has tab as a detection in',key,'next char:',item[key][0]=='\n'
    print 'tab count:',countTab
    print 'empty count:',countEmpty
if __name__ == '__main__':
    result = {}
    matches={}
    data = getData3('skin.csv')
    for row,text in data:
        result[row],matches[row] = get_section(text)

    qa(result)
        
