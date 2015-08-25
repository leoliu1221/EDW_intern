# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 13:41:52 2015

@author: sqltest
"""
import re 
from collections import defaultdict
from file_utilities import getData3
from models import Datapoint

#from get_data_breast import get_format_data


def clean_string(key,returnString=False):
    key = key.lower()
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
        
    # remove right parenthesis
    regEx = re.compile(r'(\).*)')
    if len(re.findall(regEx,key))!=0:
        return ''
    
    #now check if the key is empty
    key = key.strip()
    if returnString:
        return key
    if key=='':
        return ''
    #now remove all non-alpha numeric values, replace by space. 
    key = re.sub('[^_/0-9a-zA-Z]+', ' ', key)
    
    return key




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
    val = datapoint.value.replace("\t","")
    key = datapoint.key
    clean_val = clean_string(val)
    clean_key = clean_string(key)
    
    
    if clean_key!='':
        result[clean_key] = [clean_val,datapoint.origin]
    while j<len(sub_content):
        sub_content[j].key = datapoint.key+"_"+sub_content[j].key
        result.update(get_subcontent(result,sub_content[j],sub_content[j].sub))
        j+=1
    return result

def checkAllcancer(note,cut=110,pCut = 40):
    '''
    '''
    # a dictionary of cancerType code 
    cancerType_code = {"breast":1,"colorectal":2,"melanoma":3,"ovarian":4,"prostatic":5,"pulmonary":6,"skin":7,"thyroid":8,"uterine":9}
    note = note.replace('"','')
    #stages contrain all matches containing staging summary keyword. 
    stages = re.finditer(re.compile('staging summary(?i)'),note)
    starts = []
    result = {}
    #for different cancer staging summary there will be different start index. 
    #we store the start index in variable starts. 
    for stage in stages:
        #preivous text is the last line before our stage keyword 
        if len(note[:stage.start()].rsplit("\n",1))<2:
            previousText = ''
        else:
            previousText = note[:stage.start()].rsplit("\n",1)[1]
        #print 'previoustext',previousText
        #pcut is for finding the name of the certain cancer before staging keyword
        if 'tumor' not in note[stage.start()-7:stage.start()].lower() and len(previousText)<pCut:
            cancerType = previousText.lstrip(' ').strip()
            
            #now if the cancer type is valid we add the index to start
            if cancerType!='' and cancerType[0].isalpha() :
                for k,v in cancerType_code.items():
                    if k in cancerType.lower():
                        cancerType = cancerType_code[k]
                        break
                starts.append([stage.start(),cancerType])
        
    #for the start index in starts:
    #
    i=0
    for i in xrange(len(starts)):
        #start is the starting index for note
        start=starts[i][0]
        if start<0:
            start=0
        if i != len(starts)-1:
            process_note = note[start:starts[i+1][0]]
        else:
            process_note = note[start:]
        process_note = process_note.split("\n",1)[1]
        #print process_note
        # check that # captured datapoint is greater than 2 (if it's not, it's most likely that the returned datapoint is irrelavant)
        datapoint = get_datapoint_line(process_note, cut)
        #print 'datapoint',datapoint
        #if len(datapoint.keys())>2:
        result[starts[i][1]] = (datapoint)
#        result[starts[i][1]]=(get_datapoint_line(process_note, cut))
        
    return result
       
    # remove key_ cases
#    final_result = {}
#
#    for key,val in result.items():
#        datapoint_dict = {}
#       
#        for k in val.keys():
#            split_k = k.rsplit("_",1)
#            if len(split_k)>1 and split_k[1]=="":
#                pass
#            else:
#                datapoint_dict[k]=val[k]
#        final_result[key] = datapoint_dict
#        
#    return final_result
   
  
    

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
        tnmKeys = re.findall('(tnm|tmn)[)]* staging(?i)', lines[l])

        if len(tnmKeys)>0:
            tnmKeys = re.findall('(tnm|tmn)[)]* staging:(?i)', lines[l])
            if len(tnmKeys)>0:
                break
            
            # check the next line that is not empty
            lNext = l+1            
           
            while lines[lNext].strip()=='':
                lNext+=1
                if lNext>=len(lines):
                    break
            break 
            tnmKeys = re.findall('(tnm|tmn)[)]* staging:(?i)', lines[lNext])
            
            # if the line contain "... staging:", the line is appended and stop. Otherwise, append the following line until the next empty line
            if len(tnmKeys)>0:
                lineList.append(lines[lNext])
                break
            else:
                while lines[lNext].strip()!='':               
                    lineList.append(lines[lNext])
                    lNext+=1               
                break
        l+=1
    
    #now linelist contains any line input till it finds tnm staging. 
    #print lineList
            
#    lines = note.split("\n")
#    lineList = []
#    for line in lines:
#        if line.strip()!='':
#            lineList.append(line)
            
    result = []
    ############
    #blocklist is for storing blocks
    #blocks can spread multiple lines. 
    #1 block only contain 1 main data point and key
    #1 block can contain many sub keys and values. 
    blockList = []
    
    #starting from the first line of linelist
    i=0
    while i<len(lineList):
        #the first line of block has to be a main datapoint
        #therefore we strip it. 
        #tempLine = keydb_clean(lineList[i],True)

        block = lineList[i]+"\n"
        #check if the block first line is empty or not. If its empty, then do not process it. 
        #j is for finding the sub keys for a note. 
        ##################
        #things like: 
        #mainkey: maindata
        #   subkey: subdata
        #   subkey:subdata 
        ##################
        j=i+1
        while j<len(lineList):
            lineList[j] = lineList[j].replace('    ','\t')
            if lineList[j].startswith('\t'):
                #block +=linesList[j]+'\n'
                #tab_tag are the all the tabs existed in lineList[[j]]
                #e.g. tab_tag = re.split('[^\t]+','\t\t\tsdfs\tfghd')
                #results in ['\t\t\t', '\t', '']
                #tab_tag[0] is the first \t, might contain more than 1 \t
                tab_tag = re.split('[^\t]+',lineList[j])
                block = block + tab_tag[0] +lineList[j].strip()+'\n'
            else:
                break
            j+=1
        #print 'block['+block+']'
        blockList.append(block)
        #print 'block:',block
        info = Datapoint(block)
        #print 'info',info
        '''
        k = info.key; v = info.value; sub_content = info.sub
        
        #print 'in block',k,v,sub_content
        if len(k)<=95 and (k!='' or v!=''):
            
            clean_key = clean_string(k)
            clean_val = clean_string(v)
            clean_val = clean_val.replace("\t","")
            
            if clean_key!='':                
                result[clean_key] = clean_val
                result = get_subcontent(result,info,sub_content)
        '''
        result.append(info)
        i=j
        
    return result
  
        #print 'result',result
#    return result
      

def get_format_data(data = None,fileName=None):
    if data is None:
        data = getData3(fileName)
    result = defaultdict(list)
    i=0
    while i<len(data):
        
        result[i] = checkAllcancer(data[i][1])
        #result[i]['content'] = get_section(data[i][1])        
        i+=1
    return data,result
    
if __name__ == '__main__':
    #from file_utilities import match_encounter_id
    if 'data' not in locals():
        pass
    data = getData3('./data/ovarian.csv')
    data,result = get_format_data(data)
    #new_result = match_encounter_id(data,result)
    
    
    
    
    
