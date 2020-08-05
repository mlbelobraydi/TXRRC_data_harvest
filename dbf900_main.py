# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:41:40 2020

@author: MBelobraydic
"""

import codecs
from dbf900_formats import pic_yyyymmdd, pic_yyyymm, pic_latlong, pic_coord, pic_numeric, pic_any

def decode_file(file, block_size): ##Requires string for the file location and integer for blocksize
    print('opening',file)
    with open(file, 'rb') as ebcdicfl: #Reads the .ebc file
        data = ebcdicfl.read()
    
    print('decoding...')
    ascii_txt = codecs.decode(data, 'cp1140') #decodes the entire .ebc file to ascii
    ##This decoding method still leaves a few uncoded "/x0" type characters
    
    split_records = [] ##empty array for records
    
    print('separating records...')
    for index in range(0, len(ascii_txt), block_size): ##Creates an array for all records in the file
        split_records.append(ascii_txt[index : index + block_size])    
    
    print('returning records...')
    return split_records


def parse_record(record, layout):
    values = dict()

    for name, start, size, convert in layout:
        if convert == 'pic_yyyymmdd':
            values[name] = pic_yyyymmdd(record[start:start+size])
        elif convert == 'pic_yyyymm':
            values[name] = pic_yyyymm(record[start:start+size])
        elif convert == 'pic_latlong':
            values[name] = pic_latlong(record[start:start+size], name)
        elif convert == 'pic_coord':
            values[name] = pic_coord(record[start:start+size])
        elif convert == 'pic_numeric':
            values[name] = pic_numeric(record[start:start+size])
        else:
            values[name] = pic_any(record[start:start+size])

    return values