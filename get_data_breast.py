# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 13:41:52 2015

@author: sqltest
"""
import re 
from collections import defaultdict
from file_utilities import getData3
from file_utilities_edit import Datapoint
#data3 = getData3()
def get_section(text):
    '''
    Find the sections such as A: B: C: ... 
    Args: text a stirng a text to fimd section in. 
    Returns:
        Result:  result['A'], result['B'], result['C'] .......
                 reuslt['A'] -> text content
                 result['B'] -> text content 
                 ........
                 
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
    
    return result
            
            
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

 
def get_subcontent(result,datapoint,sub_content):
    j=0
    result[datapoint.key] = [datapoint.value.replace("\t",""),datapoint.origin]
    while j<len(sub_content):
        sub_content[j].key = datapoint.key+"_"+sub_content[j].key
        result.update(get_subcontent(result,sub_content[j],sub_content[j].sub))
        j+=1
    return result

def checkAllcancer(note,cut=110,pCut = 40):
    '''
    '''
    stages = re.finditer(re.compile('staging summary(?i)'),note)
    starts = []
    result = {}
    for stage in stages:
        previousText = note[:stage.start()].rsplit("\n",1)[1]
        if 'tumor' not in note[stage.start()-7:stage.start()].lower() and len(previousText)<pCut:
            cancerType = previousText
            starts.append([stage.start(),cancerType])
    i=0
    for i in xrange(len(starts)):
        if i != len(starts)-1:
            process_note = note[starts[i][0]-pCut:starts[i+1][0]]
        else:
            process_note = note[starts[i][0]-pCut:]
        process_note = process_note.split("\n",1)[1]
        
            
        # check that # captured datapoint is greater than 2 (if it's not, it's most likely that the returned datapoint is irrelavant)
        datapoint = get_datapoint_line(process_note, cut)
        if len(datapoint)>2:
            result[starts[i][1]] = (datapoint)
#        result[starts[i][1]]=(get_datapoint_line(process_note, cut))
    return result
  
    

def get_datapoint_line(note,cut):
    
    #cut off tnm staging +cut, or to the end of the line
#    try:
#        tnm_index = re.search('(tnm|tmn)[)]* staging(?i)', note).start()
#        note = note[0:tnm_index+cut]
#    except AttributeError:
#        pass;
    lineList = []
    lines = note.split("\n")
    l=0
    while l<len(lines):
        lineList.append(lines[l])
        tnmTag = re.findall('(tnm|tmn)[)]* staging(?i)', lines[l])

        if len(tnmTag)>0:
            tnmTag_line = re.findall('(tnm|tmn)[)]* staging:(?i)', lines[l])
            if len(tnmTag_line)>0:
                break
            
            # check the next line that is not empty
            l1 = l+1
            while lines[l1].strip()=='':
                l1+=1
           
            l2 = l1 
            tnmTag_line2 = re.findall('(tnm|tmn)[)]* staging:(?i)', lines[l2])
            
            # if the line contain "... staging:", the line is appended and stop. Otherwise, append the following line until the next empty line
            if len(tnmTag_line2)>0:
                lineList.append(lines[l2])
                break
            else:
                while lines[l2].strip()!='':               
                    lineList.append(lines[l2])
                    l2+=1               
            break
        l+=1
                
            
#    lines = note.split("\n")
#    lineList = []
#    for line in lines:
#        if line.strip()!='':
#            lineList.append(line)
    result = {}
    blockList = []
    i=1
    while i<len(lineList):
        block = lineList[i]+"\n"
        j=i+1
        while j<len(lineList):
            if lineList[j].startswith('\t') or lineList[j].startswith(' '):
                block = block + lineList[j]+"\n"
            else:
                break
            j+=1
        blockList.append(block)
        info = Datapoint(block)
        k = info.key; v = info.value; sub_content = info.sub
        if len(k)<=100 and (k!='' or v!=''):
            result[k] = v.replace("\t","")
            result = get_subcontent(result,info,sub_content)
        i=j
        
    return result

def get_format_data(data = None,fileName=None):
    if data is None:
        data = getData3(fileName)
    result = defaultdict(list)
    i=0
    while i<len(data):
        print "note",i
        result[i] = checkAllcancer(data[i][1].replace('"',''))
        result[i]['content'] = get_section(data[i][1])        
        i+=1
    return data,result
    
if __name__ == '__main__':
#    if 'data' not in locals():
#        data = getData3()
    #if 'data' not in locals():
    data = getData3('ovarian_cancer_notes.csv')
    data,result = get_format_data(data)
    #import json
    #json.dump(result,open('results.json','w'))
    #data = getData3()
    
    
    
    
    