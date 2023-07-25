# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:41:40 2020

@author: MBelobraydic
"""

from ebcdic_formats import pic_yyyymmdd, pic_yyyymm, pic_numeric, pic_any, pic_signed, comp3

##From https://github.com/skylerbast/TxRRC_data
##Generates the block of bytes from the file.
## Should be added to dbf900_main_bytes when it is working
def yield_blocks(file: str, number_of_bytes: int):
    while (block_bytes := file.read(number_of_bytes)):
        if len(block_bytes) != number_of_bytes:
            print(f"WARNING: Block size is {len(block_bytes)} bytes, not {number_of_bytes} bytes. If this is at the end of the file, there might just be extra bytes.")
        yield block_bytes

def parse_record(record: bytes, layout: tuple):
    breakpoint()
    values = dict()

    for name, start, size, convert_format in layout:
        decimal = 0
        ##check for additional data for pic_signed and comp 3 methods
        if '_' in str(size): ##check if size also includes the number of decimals "Size_Decimal"
            size_split = size.split('_')
            size = int(size_split[0])
            decimal = int(size_split[1])
            
        if convert_format == 'pic_yyyymmdd':
            values[name] = pic_yyyymmdd(record[start:start+size])
        elif convert_format == 'pic_yyyymm':
            values[name] = pic_yyyymm(record[start:start+size])
        elif convert_format == 'pic_numeric':
            values[name] = pic_numeric(record[start:start+size])
        elif convert_format == 'pic_signed':
            values[name] = pic_signed(record[start:start+size],name, decimal)
        elif convert_format == 'pic_comp':
            values[name] = comp3(record[start:start+size], decimal)
        else:
            values[name] = pic_any(record[start:start+size])

    return values
