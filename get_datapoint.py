# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 14:46:28 2015

@author: sqltest
"""
import re
            

def extract_key(note,key):
    note = note.replace('"','')    
    val = re.split('cancer staging summary(?i)',note)
    newkey = []
    returnkey = []
    if len(val)>1:
        lineList = val[1].split("\n")
        for line in lineList: 
            index = line.find(":")
            if index>0:           
                k = line[0:index]   
                newkey.append(k)
        
        while newkey!=key:
            list_common = []
            if key==[]:
                returnkey = newkey
                break
            for a,b in zip(key,newkey):
                if a==b:
                    list_common.append(a)
                else:
                    break
            returnkey = returnkey + list_common
            num = len(list_common)
            num_key = num; num_newkey = num
  
            if newkey!=key:
                if len(newkey)==num:
                    returnkey = returnkey + key[num:len(key)]
                    break
                if len(key)==num:
                    returnkey = returnkey + newkey[num:len(newkey)]
                    break
                if newkey[num] in key:
                    returnkey.append(key[num])
                    key.remove(key[num])
                elif key[num] in newkey:
                    returnkey.append(newkey[num])
                    newkey.remove(newkey[num])
                else:
                    common = [i for i in key[num:len(key)] if i in newkey[num:len(newkey)]]
                    if len(common)>0:
                        ind_key = key.index(common[0])
                        ind_newkey = newkey.index(common[0])
                        returnkey = returnkey + newkey[num:ind_newkey] + key[num:ind_key]
                        num_key = ind_key
                        num_newkey = ind_newkey                           
                    else:
                        newkey = newkey[num:len(newkey)]
                        key = key[num:len(key)]
                        returnkey = returnkey + newkey + key
                        break
                newkey = newkey[num_newkey:len(newkey)]
                key = key[num_key:len(key)]
        return returnkey
    else:
        return key
             
            
i=0
key = []
while i<len(data):
    note = data[i][1].lower()
    key = extract_key(note,key) 
    i+=1               