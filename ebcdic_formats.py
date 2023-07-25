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

##From https://github.com/skylerbast/TxRRC_data
##converts bytes to string through codecs decoding
## Should be added to dbf900_main_bytes when it is working
def ebc_decode(data: bytes):
    ebcdic_decoder = codecs.getdecoder('cp1140')
    decoded = ebcdic_decoder(data)
    val = decoded[0]
    return val

def pic_yyyymmdd(date_data: bytes):
    date = ebc_decode(date_data)
    #Changes format YYYYMMDD from a series of numbers to datetime object
    try:
        val = datetime.strptime(date, '%Y%m%d').strftime('%Y-%m-%d')
    except ValueError:
        val = None
    return val
    
def pic_yyyymm(yyyymm_data: bytes):
    yyyymm = ebc_decode(yyyymm_data)
    #Changes format YYYYMM from a series of numbers to datetime object
    #makes the date the first day of the month
    try:
        val = date(year=int(yyyymm[0:4]), month=int(yyyymm[4:]), day=1).strftime('%Y-%m-%d')
    except ValueError:
        val = None

    return val

def pic_numeric(num_data: bytes):
    num = ebc_decode(num_data)
    try: ##using a try to ensure the values passed are actually 0-9 with no other characters
        val = int(num)
    except:
        val = None

    return val

def pic_any(input_data: bytes): #need to confirm the number of characters
    string  = ebc_decode(input_data)
    STRIP_PIC_X = True # Set this to False if trimming PIC X causes problems.
    val = str(string)
    if STRIP_PIC_X == True:
        val = val.strip()

    return val

def pic_signed(signed_data: bytes, name, decimal=0): #replacement for pic_latlong and pic_coord
    # Converts an EBCDIC Signed number to Python float
    # 'signed' must be EBCDIC-encoded raw bytes -- this will not work
    # if the data has been converted to ASCII.
    ## info here http://www.3480-3590-data-conversion.com/article-signed-fields.html
    signed_raw = array('B', signed_data)
    val = float(0)
    
    # Bytes 1 to n-1 are stored as plain EBCDIC encoded digits
    for i in signed_raw:
        val = val * 10 + (i & 0x0F)
    
   
    # If the penultimate nibble == 0xD, then the number is negative. Otherwise,
    # it is either positive or unsigned.
    val = (val * (-1 if signed_raw[-1] >> 4 == 0xD else 1)) / 10**decimal
    
    ##TXRRC signs longitude as a positive value with 0xC and requires transformation to a negative number
    if ('LONGITUDE' in name) and (val > 0): ##This is only appropriate for western hemisphere
        val = -val
    
    return val

def comp3(packed: bytes, decimal_location=0):
    ##From: https://github.com/skylerbast/TxRRC_data/blob/master/cobol_types.py
    ## For more see: http://3480-3590-data-conversion.com/article-packed-fields.html
    # Function unpacks a COMP-3 number with number of digits n
    # Also optionally allows for conversion to float, which is specificed by PICture,
    # rather than in the data itself
    bin_arr = array('B', packed)
    val = float(0)
    
    # For nibbles 1 to n - 1
    # First digit in nibble is found by performing bitwise and with 0xf0, shifting 
    # right by 4 bits, and then multiplying the integer result by 10. The second 
    # digit in the nibble is found by performing a bitwise and with 0xf. These are
    # added together, and added to the existing (more significant) digits
    for i in bin_arr[:-1]:
      val = (val * 100) + (((i & 0xf0) >> 4) * 10) + (i & 0xf) 
    
    # For nibble n, only the first four bits represent a digit; the last 4 bits of 
    # nibble n represent the sign of the number
    i = bin_arr[-1]
    val = (val * 10) + ((i & 0xf0) >> 4)
    if (i & 0xf) == 0xd:
      val = -val
    
    # If we've been told how many decimals there are, leave the result float and 
    # put the decimal in the proper place; otherwise make it an integer 
    val = val / (10 ** decimal_location)
    if decimal_location == 0:
      val = int(val)
    
    return val
