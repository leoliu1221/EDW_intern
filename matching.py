# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 09:09:55 2015

@author: sqltest
"""
def match_result(pResult,name):
    '''
    Args:
        pResult: an array of 2 dictionaries. 1st is for organs, 2nd is for line numbers
        name: a string representing which note the result come from. 
    Returns:
        [(organ1,stageNum1,lineNum1),(organ2,stageNum2,lineNum2) .... ]
        organs: string. organ that finds correlation
        stageNum: int. the stage number that finds correlation
        lineNum: int. the line number at which organ and stage Num are met
    '''
    result = {}
    if len(pResult[0].keys())!=0 and len(pResult[1].keys())!=0:
        for organ in pResult[0].keys():
            for lineNum in pResult[0][organ]:
                for stage in pResult[1].keys():
                    if lineNum in pResult[1][stage]:
                        #then we have a match! 
                        if result.get(organ)==None:
                            result[organ] = []
                        result[organ].append((stage,lineNum,name))
    return result

