# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:25:01 2015

@author: sqltest
"""

from file_utilities import getData3
import re


def last_line_pos(text,pos):
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
    indStart = text.find('A.')
    #print 'indStart is working good'
    if indStart=='-1':return {}
    indEnd = text.lower().find('staging')
    if indEnd == -1:
        section = text[indStart:]
    else:
        section = text[indStart:indEnd]
    alpha = re.compile('[A-Z]\.')
    matches = []
    prev = None
    for match in alpha.finditer(section):
        if prev is None:
            prev = match.group()[0]
        elif ord(match.group()[0])-ord(prev)!=1:
            continue
        matches.append([match.group(),match.start(),match.end()])
        prev = match.group()[0]
    
    result = {}
    for i in xrange(len(matches)):
        if i == len(matches)-1:
            result[matches[i][0]] = text[matches[i][2]:last_line_pos(text,indEnd)]
        else:
            result[matches[i][0]] = text[matches[i][2]:matches[i+1][1]]
            
    return result
            
if __name__ == '__main__':
    result = {}
    
    #data = getData3()
    for row,text in data:
        result[row] = get_section(text)

        
        
        