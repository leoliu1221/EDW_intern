'''
fileName: tnm.py
Usage: mainly for use the function get_stage_from_pa
Wanted to create a parser that checks for all lines in the text
If the line has tnm system then outputs the tnm system staging
'''
from file_utilities import update,getData2
from stage_cancer import get_stage_num,get_stage_from_pa,get_cancer_type,get_tnm
from matching import match_result
if __name__ == '__main__':
    result = {}
    data = getData2()
    row=0
    for pid,fDate,pDate,pNote,paDate,paNote in data:
        if result.get(row)==None:
            result[row]= {}
            result[row]['p'] = [{},{}]
            result[row]['pa']=[{},{}]
            result[row]['pid'] = pid
        update(result[row]['p'][1],get_stage_num(pNote,'grade'))
        update(result[row]['p'][1],get_stage_num(pNote,'stage'))
        update(result[row]['p'][1],get_tnm(pNote))
        update(result[row]['pa'][1],get_stage_num(paNote,'stage'))
        update(result[row]['pa'][1],get_stage_num(paNote,'grade'))
        update(result[row]['pa'][1],get_stage_from_pa(paNote))
        update(result[row]['pa'][0],get_cancer_type(paNote))
        update(result[row]['p'][0],get_cancer_type(pNote))
        matchResult = update(match_result(result[row]['p'],'p'),match_result(result[row]['pa'],'pa'))
        result[row]['stage'] = matchResult
        row+=1
    count=0;
    
    result2 = {}
    #result2 has patient as the key and all other things as values. 
    for key in result.keys():
        if result2.get(result[key]['pid'])==None:
            result2[result[key]['pid']]={}
        result2[result[key]['pid']][key] = None
    for pid in result.keys():
        #if len(result[pid]['pa'][0].keys())==0:
        if len(result[pid]['stage'])==0:
            count+=1
    print count,len(result.keys())
