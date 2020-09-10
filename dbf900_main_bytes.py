# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:41:40 2020

@author: MBelobraydic
"""

import codecs
from dbf900_formats_bytes import pic_yyyymmdd, pic_yyyymm, pic_numeric, pic_any, pic_signed

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

##From https://github.com/skylerbast/TxRRC_data
##Generates the block of bytes from the file.
## Should be added to dbf900_main_bytes when it is working
def yield_blocks(file, n):
    block_bytes = file.read(n)
    while block_bytes:
        yield block_bytes
        block_bytes = file.read(n)


def parse_record(record, layout):
    values = dict()

    for name, start, size, convert in layout:
        
        ##check for additional data for pic_signed method
        if '_' in str(size): ##check if size also includes the number of decimals "Size_Decimal"
            size_split = size.split('_')
            size = int(size_split[0])
            decimal = int(size_split[1])
            
        if convert == 'pic_yyyymmdd':
            values[name] = pic_yyyymmdd(record[start:start+size])
        elif convert == 'pic_yyyymm':
            values[name] = pic_yyyymm(record[start:start+size])
        elif convert == 'pic_numeric':
            values[name] = pic_numeric(record[start:start+size])
        elif convert == 'pic_signed':
            values[name] = pic_signed(record[start:start+size],name, decimal)
        else:
            values[name] = pic_any(record[start:start+size])

    return values