# -*- coding: utf-8 -*-
"""
Created on Wed Jul 01 16:05:54 2015

@author: sqltest
"""

import time

def compareTime(x,y):
    '''
    Args:
        x,y: items to be compared
    return:
        1 : if x > y
        -1: if x < y
        0 : otherwise
    '''
    if x[1] > y[1]:
        return 1
    if x[1] < y[1]:
        return -1
    return 0
def dateToObject(dt):
    '''
    Change date and time to time object 
    Args:
        dt: date with Year-month-date format and time with 00:00:00 format
    Returns:
        to: time object
    '''
    dt = dt.split()
    Date = dt[0].split("-")
    Time = dt[1].split(":")
    to = time.strptime(Date[2]+" "+Date[1]+" "+Date[0]+" "+Time[0]+" "+Time[1]+" "+Time[2], "%d %m %Y %H %M %S")
    return to
    
