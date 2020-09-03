# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:03:51 2020

@author: MBelobraydic

formatting dates, strings, decimals, and numbers
"""



def pic_yyyymmdd(date):
    from datetime import datetime
    #Changes format YYYYMMDD from a series of numbers to datetime object
    try:
        val = datetime.strptime(date, '%Y%m%d').strftime('%m/%d/%Y')
    except ValueError:
        val = None
    return val
    
def pic_yyyymm(yyyymm):
    from datetime import date
    #Changes format YYYYMM from a series of numbers to datetime object
    #makes the date the first day of the month
    try:
        val = date(year=int(yyyymm[0:4]), month=int(yyyymm[4:]), day=1).strftime('%m/01/%Y')
    except ValueError:
        val = None

    return val
    
def pic_latlong(latlon, name): ##This is probably inefficent for the conversion
    ##DDDDDDDDD to DDD.DDDDDD
    try:
        val = float(str(latlon[0:3])+'.'+str(latlon[3:9]))
        if 'LONGITUDE' in name: ##This is only appropriate for western hemisphere
            val = -val
    except ValueError:
        val = None
    return val

def pic_coord(coord): ##This is probably inefficent for the conversion
    ##CCCCCCCC to CCCCCCC.C
    try:
        val = float(str(coord[0:8])+'.'+str(coord[8]))
    except ValueError:
        val = None    
    return val

def pic_numeric(num):
    try: ##using a try to ensure the values passed are actually 0-9 with no other characters
        val = int(num)
    except:
        val = None

    return val

def pic_any(string): #need to confirm the numberof characters
    STRIP_PIC_X = True # Set this to False if trimming PIC X causes problems.
    val = str(string)
    if STRIP_PIC_X == True:
        val = val.strip()

    return val