# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:25:01 2015

@author: sqltest
"""

from file_utilities import getData3
import re


def last_line_pos(text,pos):
    if len(text)<pos:
        pos = len(text)-1
    if pos<=0:
        return len(text)
    while pos>0:
        if text[pos] == '\n':
            return pos
        pos-=1
    return len(text)
        

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
    matchA = re.compile('A[\s+\.]')
    if matchA.search(text) is not None:
        indStart = matchA.search(text).start()
    else:
        return {},{}
    #indStart = text.find('A.')
    #print 'indStart is working good'
    if indStart=='-1':return {}
    indEnd = text.lower().rfind('staging summary')
    if indEnd == -1 or indEnd<=indStart:
        section = text[indStart:]
    else:
        section = text[indStart:indEnd]
    alpha = re.compile('[A-Z][\\.\s+]')
    matches = []
    prev = None
    for match in alpha.finditer(section):
        if prev is None:
            if match.group()[0]!='A':
                continue
            prev = match.group()[0]
        elif ord(match.group()[0])-ord(prev)!=1:
            continue
        matches.append([match.group(),match.start(),match.end()])
        prev = match.group()[0]
    
    result = {}
    for i in xrange(len(matches)):
        if i == len(matches)-1:
            result[matches[i][0]] = section[matches[i][2]:last_line_pos(section,indEnd)]
        else:
            result[matches[i][0]] = section[matches[i][2]:matches[i+1][1]]
            
    return result,matches
            
if __name__ == '__main__':
    result = {}
    matches={}
    #data = getData3()
    for row,text in data:
        result[row],matches[row] = get_section(text)

        
        
        