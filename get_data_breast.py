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



#def extractContent(regex,text):
#    '''
#    extract each data point
#    Args:
#        regex: regular expression used to capture each data point
#        text: raw data from which information is extracted 
#    return:
#        resultText: information extracted 
#        returnText: the remaining text after extract the data point
#    '''
#    value = re.split(regex+'(?i)',text)
#    if len(value)>1:
#        content = value[1]
#        if len(value)>2:
#            j=2
#            while j<len(value):
#                content = content+regex+value[j]
#                j+=1
#        resultText = content.split('\n')[0]
#        resultText = resultText.replace(":","").lstrip()
#        returnText = content[content.find('\n'):len(content)]
#    else:
#        resultText = "None"
#        returnText = text
#    return resultText,returnText
#def get_line_staging_summary(line):
#    print 'in line:',line
#    line = line.replace('"','')
#    val = re.split('invasive breast cancer staging summary(?i)',line)
#    result = []
#    if len(val)>1:
#        specimen_submitted,returnText = extractContent('specimen submitted:',val[1])
#        result.append(specimen_submitted)        
#        specimen_dim,returnText = extractContent('specimen dimensions:',returnText)
#        result.append(specimen_dim)
#        tumor_size,returnText = extractContent('tumor size:',returnText)
#        result.append(tumor_size)
#        histologic_type,returnText = extractContent('histologic type:',returnText)
#        result.append(histologic_type)
#        grade,returnText = extractContent('grade:',returnText)
#        result.append(grade)
#        lymphatic_vascular_invasion,returnText = extractContent('lymphatic vascular invasion:',returnText)
#        result.append(lymphatic_vascular_invasion)
#        DCIS,returnText = extractContent('dcis as extensive component: |dcis as extensive intraductal component:',returnText)
#        result.append(DCIS)
#        DCIS_measurement,returnText = extractContent('dcis measurement/proportion:',returnText)
#        result.append(DCIS_measurement)
#        LCIS,returnText = extractContent('lcis:',returnText)
#        result.append(LCIS)
#        lobular_neoplasia,returnText = extractContent('lobular neoplasia:',returnText)
#        result.append(lobular_neoplasia)
#        calcifications,returnText = extractContent('calcifications:',returnText)
#        result.append(calcifications)
#        location_of_calcifications,returnText = extractContent('location of calcifications:',returnText)
#        result.append(location_of_calcifications)
#        margins_of_excision,returnText = extractContent('margins of excision:',returnText)
#        result.append(margins_of_excision)
#        invasive_cancer,returnText = extractContent('invasive cancer:',returnText)
#        result.append(invasive_cancer)
#        distance_to_margin,returnText = extractContent('distance to margin:',returnText)
#        result.append(distance_to_margin)
#        DCIS2,returnText = extractContent('dcis:',returnText)
#        result.append(DCIS2)
#        distance_to_margin,returnText = extractContent('distance to margin:',returnText)
#        result.append(distance_to_margin)
#        axillary_lymph_nodes,returnText = extractContent('axillary lymph nodes:',returnText)
#        result.append(axillary_lymph_nodes)
#        num_of_positive_versus_total,returnText = extractContent('# of positive versus total:|number of positive versus total:',returnText)
#        result.append(num_of_positive_versus_total)
#        size_of_largest_metastasis,returnText = extractContent('size of largest metastasis:',returnText)
#        result.append(size_of_largest_metastasis)
#        extranodal_extension,returnText = extractContent('extranodal extension:',returnText)
#        result.append(extranodal_extension)
#        breast_tumor_markers,returnText = extractContent('breast tumor markers',returnText)
#        result.append(breast_tumor_markers)
#        er,returnText = extractContent('er:',returnText)
#        result.append(er)
#        pr,returnText = extractContent('pr:',returnText)
#        result.append(pr)
#        p53,returnText = extractContent('p53:',returnText)
#        result.append(p53)
#        ki_67,returnText = extractContent('ki-67:',returnText)
#        result.append(ki_67)
#        her_2_neu,returnText = extractContent('her-2/neu:',returnText)
#        result.append(her_2_neu)
#        tumorBank,returnText = extractContent('tumor\sbank:',returnText)
#        result.append(tumorBank)
#        TNM_staging,returnText = extractContent('tnm staging:',returnText)
#        result.append(TNM_staging)
#    else:
#        result.append("no info")
#    return result
 
def get_subcontent(result,k,v,sub_content):
    j=0
    while j<len(sub_content):
        k = k+"_"+sub_content[j].key; v = sub_content[j].value
        result[k] = v.replace("\t","")
        if len(sub_content[j].sub)>0:
            get_subcontent(result,k,v,sub_content[j].sub)
        k = k.split("_")[0] 
        j+=1
    return result
    
def get_datapoint(note):
    result = {}
    note = note.split("\n")
    text = ""
    for line in note:
        line = line.split(":")
        if len(line)==1:
            text = text+line[0]+"\n"
        else:
            if '\t' in line[0]:
                if len(line)>1:
                    text = text+line[0]+"###"+line[1]+"\n"
                else:
                    temp = line[0].split("\t",1)
                    text = text+temp[0]+"###"+temp[1]+"\n"
            else:
                text = text+line[0]+":"+line[1]+"\n"
    
    text = text.split(":")
    key = text[0].rsplit("\n",1)
    key = key[1].replace("\n","")
    i=1
    while i<len(text):
        if "###" in text[i]:
            content = text[i].rsplit("\n",1)
        else:
            content = text[i].split("\n",1)
        value = content[0].replace("###",":")
        info = Datapoint(key+":"+value)
        k = info.key; v = info.value; sub_content = info.sub
        result[k] = v.replace("\t","")
        result = get_subcontent(result,k,v,sub_content)
    
        key = content[1].replace("\n","")
        i+=1
    return result
        
    
    
   
def get_staging_summary(data3 = None):
    if data3 is None:
        data3 = getData3()
    resultDict = defaultdict(list)
    i=0
    while i<len(data3):
        print i
        note = data3[i][1]
        note = re.split('Cancer Staging Summary'+'(?i)',note)
        note2 = note[1].lower()
        index = note2.find('tnm staging:')
        if index > 0:
            note_process = note[1][0:index+20]
        else:
            note_process = note[1]
        resultDict[i] = get_datapoint(note_process)
        
        i+=1
    return resultDict
    
if __name__ == '__main__':
    if 'data' not in locals():
        data = getData3()
    
    result2 = {}
    matches={}
    result = get_staging_summary(data)
    for row,text in data:
        result[row].append(get_section(text))
        print row
    #import json
    #json.dump(result,open('results.json','w'))
    #data = getData3()
    
    
    
    
    