# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:41:40 2020

@author: MBelobraydic
"""

import codecs
from dbf900_formats import pic_yyyymmdd, pic_yyyymm, pic_latlong, pic_coord, pic_numeric, pic_any

##potential add to decode file and break into the individual records 

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