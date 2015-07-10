# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:25:01 2015

@author: sqltest
"""

from file_utilities import getData3

#find the first A. in the text
#read to the start of 'Invasive Breast Cancer Staging Summary'
def getSection(text):
    '''
    Find the sections such as A: B: C: ... 
    Args: text a stirng a text to fimd section in. 
    Returns:
        Result:  result['A']['content'], result['A']['title'],result['B']['content'].....
                 'content' -> ['a','b','c']
                 'title' -> 'title'
    '''
    indStart = text.find('A.')
    print indStart
    if indStart=='-1':return {}
    indEnd = text.lower().find('staging summary')
    section = text[indStart:indEnd]
    lines = section.split('\n')
    result = {}
    charSection = 'A'
    for line in lines:
        line = line.strip()
        if len(line)==0:continue
        if line[0] == '-':
            result[charSection]['contents'].append(line[1:].strip())
        if line[0]!='-':
            if len(line)<=1:continue
            if line[1]!='.':continue
            charSection = line[0]
            if result.get(charSection) == None:
                result[charSection] = {}
                result[charSection]['contents']=[]
                result[charSection]['title']=line[2:].strip()
    return result
            
if __name__ == '__main__':
    result = {}
    #data = getData3()
    for row,text in data:
        result[row] = getSection(text)

        
        
        