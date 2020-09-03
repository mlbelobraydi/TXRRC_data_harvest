# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:03:51 2020

@author: MBelobraydic

formatting dates, strings, decimals, and numbers
"""
import codecs
from datetime import datetime
from datetime import date
from array import array


def pic_yyyymmdd(date):
    date = codecs.decode(date, 'cp1140')
    #Changes format YYYYMMDD from a series of numbers to datetime object
    try:
        val = datetime.strptime(date, '%Y%m%d').strftime('%m/%d/%Y')
    except ValueError:
        val = None
    return val
    
def pic_yyyymm(yyyymm):
    yyyymm = codecs.decode(yyyymm, 'cp1140')
    #Changes format YYYYMM from a series of numbers to datetime object
    #makes the date the first day of the month
    try:
        val = date(year=int(yyyymm[0:4]), month=int(yyyymm[4:]), day=1).strftime('%m/01/%Y')
    except ValueError:
        val = None

    return val

def pic_numeric(num):
    num = codecs.decode(num, 'cp1140')
    try: ##using a try to ensure the values passed are actually 0-9 with no other characters
        val = int(num)
    except:
        val = None

    return val

def pic_any(string): #need to confirm the numberof characters
    string  = codecs.decode(string, 'cp1140')
    STRIP_PIC_X = True # Set this to False if trimming PIC X causes problems.
    val = str(string)
    if STRIP_PIC_X == True:
        val = val.strip()

    return val

def pic_signed(signed, decimal=0): #replacement for pic_latlong and pic_coord
    # Converts an EBCDIC Signed number to Python float
    # 'signed' must be EBCDIC-encoded raw bytes -- this will not work
    # if the data has been converted to ASCII.
    print('original sent bytes:', signed)
    signed_raw = array('B', signed);
    val = float(0);
    print('converted to array:', signed_raw)
    
    # Bytes 1 to n-1 are stored as plain EBCDIC encoded digits
    for i in signed_raw:
        val = val * 10 + (i & 0x0F)
    
    print('result by adding array:',val)
    
    # If the penultimate nibble == 0xD, then the number is negative. Otherwise,
    # it is either positive or unsigned.
    val = (val * (-1 if signed_raw[-1] >> 4 == 0xD else 1)) / 10**decimal
    print('final val to be sent back:',val)
    
    return val