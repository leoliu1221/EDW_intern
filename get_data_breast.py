# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 13:41:52 2015

@author: sqltest
"""
import re 
from collections import defaultdict
import json

def getData3(fName=None):
    '''
    Get data from file. 
    Args:
        fName: optional. Provides the filename to the csv data file. Format: each column is separated by "|"
    Returns:
        Data: a dictionary of [...]
    '''
    
    if fName is None:
        fName = 'breast_cancer_notes.csv'
    f = open(fName,'r')
    #burn the first line
    header = f.readline();
    print "header:",header
    rawText = f.read()
    rawText = rawText.split("|")
    raw = ''
    data = []   
    i=0
    while i<len(rawText):
        
        if i%6 != 0 :
            raw = raw + rawText[i] + "|"
        else:
            pid = re.findall(re.compile('\d{8}'),rawText[i])
            text = re.split('"\d{8}"',rawText[i])
            if len(pid)>0:
                raw = raw + text[0] + "|" + pid[0] + "|"
            else:
                print i
                break

        i+=1
    
    raw = raw.split("|")      
    
    i=1
    rowNum = 0
    while i<len(raw)-1:
        '''
        encntr_id = int(raw[i].replace('"',''))
        event_id = int(raw[i+1].replace('"',''))
        event_end_dt_tm = raw[i+2]
        event_cd = int(raw[i+3].replace('"',''))
        event_dsc = raw[i+4]
        '''
        first_eightthousand = raw[i+5]
        second_eightthousand = raw[i+6]
        data.append([rowNum,first_eightthousand+second_eightthousand])
                
        i = i+7
        rowNum+=1
    return data   
    
#data3 = getData3()
result = defaultdict(list)

def extractContent(regex,text):
    '''
    extract each data point
    Args:
        regex: regular expression used to capture each data point
        text: raw data from which information is extracted 
    return:
        resultText: information extracted 
        returnText: the remaining text after extract the data point
    '''
    value = re.split(regex+'(?i)',text)
    if len(value)>1:
        content = value[1]
        if len(value)>2:
            j=2
            while j<len(value):
                content = content+regex+value[j]
                j+=1
        resultText = content.split('\n')[0]
        resultText = resultText.replace(":","").lstrip()
        returnText = content[content.find('\n'):len(content)]
    else:
        resultText = "None"
        returnText = text
    return resultText,returnText

temp = []
i=1
while i<len(data3):
    note = data3[i][1].replace('"','')
    val = re.split('invasive breast cancer staging summary(?i)',note)
    if len(val)>1:
        specimen_submitted,returnText = extractContent('specimen submitted:',val[1])
        result[i].append(specimen_submitted)        
        specimen_dim,returnText = extractContent('specimen dimensions:',returnText)
        result[i].append(specimen_dim)
        tumor_size,returnText = extractContent('tumor size:',returnText)
        result[i].append(tumor_size)
        histologic_type,returnText = extractContent('histologic type:',returnText)
        result[i].append(histologic_type)
        grade,returnText = extractContent('grade:',returnText)
        result[i].append(grade)
        lymphatic_vascular_invasion,returnText = extractContent('lymphatic vascular invasion:',returnText)
        result[i].append(lymphatic_vascular_invasion)
        DCIS,returnText = extractContent('dcis as extensive component: |dcis as extensive intraductal component:',returnText)
        result[i].append(DCIS)
        DCIS_measurement,returnText = extractContent('dcis measurement/proportion:',returnText)
        result[i].append(DCIS_measurement)
        LCIS,returnText = extractContent('lcis:',returnText)
        result[i].append(LCIS)
        lobular_neoplasia,returnText = extractContent('lobular neoplasia:',returnText)
        result[i].append(lobular_neoplasia)
        calcifications,returnText = extractContent('calcifications:',returnText)
        result[i].append(calcifications)
        location_of_calcifications,returnText = extractContent('location of calcifications:',returnText)
        result[i].append(location_of_calcifications)
        margins_of_excision,returnText = extractContent('margins of excision:',returnText)
        result[i].append(margins_of_excision)
        invasive_cancer,returnText = extractContent('invasive cancer:',returnText)
        result[i].append(invasive_cancer)
        distance_to_margin,returnText = extractContent('distance to margin:',returnText)
        result[i].append(distance_to_margin)
        DCIS2,returnText = extractContent('dcis:',returnText)
        result[i].append(DCIS2)
        distance_to_margin,returnText = extractContent('distance to margin:',returnText)
        result[i].append(distance_to_margin)
        axillary_lymph_nodes,returnText = extractContent('axillary lymph nodes:',returnText)
        result[i].append(axillary_lymph_nodes)
        num_of_positive_versus_total,returnText = extractContent('# of positive versus total:|number of positive versus total:',returnText)
        result[i].append(num_of_positive_versus_total)
        size_of_largest_metastasis,returnText = extractContent('size of largest metastasis:',returnText)
        result[i].append(size_of_largest_metastasis)
        extranodal_extension,returnText = extractContent('extranodal extension:',returnText)
        result[i].append(extranodal_extension)
        breast_tumor_markers,returnText = extractContent('breast tumor markers',returnText)
        result[i].append(breast_tumor_markers)
        er,returnText = extractContent('er:',returnText)
        result[i].append(er)
        pr,returnText = extractContent('pr:',returnText)
        result[i].append(pr)
        p53,returnText = extractContent('p53:',returnText)
        result[i].append(p53)
        ki_67,returnText = extractContent('ki-67:',returnText)
        result[i].append(ki_67)
        her_2_neu,returnText = extractContent('her-2/neu:',returnText)
        result[i].append(her_2_neu)
        tumorBank,returnText = extractContent('tumor\sbank:',returnText)
        result[i].append(tumorBank)
        TNM_staging,returnText = extractContent('tnm staging:',returnText)
        result[i].append(TNM_staging)
        
    else:
        result[i].append("no info")

    i+=1
    