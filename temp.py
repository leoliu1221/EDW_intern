# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from collections import defaultdict
import re
#
#def collectValue(inputDict):
#    value = defaultdict(list)
#    for k,v in inputDict.iteritems():
#        for k2,v2 in v.iteritems():
#            if k2!='content':
#                for k3,v3 in v2.iteritems():
#                    value[k3].append(v3[0])
#    return value
#
#    
#val = collectValue(result)


def featureType(value,lenCutoff = 0.8):
    typeDict = defaultdict(list)
    # countType contains [total, num only, num+text, text only]
    countType = [0]*4 
    countType[0]=len(value)
    for v in value:
        if bool(re.search(r'\d', v)):
            if bool(re.search(r'\s',v)):               
                typeDict['num_text'].append(v)
                countType[2]+=1
            else:
                typeDict['num'].append(v)
                countType[1]+=1
        else:
            typeDict['text'].append(v)
            countType[3]+=1
  
    # process num_text by counting length of string 
    # countLength contains [total num+text, short text, long text]    
    if countType[2]>0:    
        countLength = [0]*3
        countLength[0] = countType[2]
        for v in typeDict['num_text']:
            s = ''.join([i for i in v if not i.isdigit()])
   
            if len(s)/len(v)>lenCutoff:
                countLength[2]+=1
            else:
                countLength[1]+=1
    else:
        countLength = [1,1,1]
    
         
    # process text by using NLP
    if countType[3]>0:
        
            
    
        