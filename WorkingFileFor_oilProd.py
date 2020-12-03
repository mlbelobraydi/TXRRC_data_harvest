# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 18:19:54 2020

@author: MBelobraydic
"""

import pandas as pd

## Importing from the main directory now
from ebcdic_main import yield_blocks, parse_record
from layouts_oilProd import oilProd_layout
from ebcdic_formats import pic_any

file_path = r'C:\PublicData\Texas\TXRRC\index\olf001l.ebc' ##Local storage location
##file origin: ftp://ftpe.rrc.texas.gov/sholed/olf001l.ebc.gz ## extracted with 7-zip locally


block_size  = 1200 ##block size for each record in the file
##Unknown if this holds true for all versions of this file or for other files on TXRRC

print('opening',file_path,'...')
file = open(file_path, 'rb') ##Opens the .ebc file and reads it as bytes

##Use limiting counter for testing formatting
Limiting_Counter = True

"""
##Section for testing the outputs
"""  
API = None ##this needs to be inplace incase the random part of the array selected does start on an 01 record
ct = 0 ##counter for number of records
wellct = 0 ##counter for number of wells
check_stop = 100 ##number of loop runs to complete before stopping

"""Loop section for all records or partial set"""
for block in yield_blocks(file, block_size): ##for each block in file
    
    ##For testing script
    if Limiting_Counter == True and wellct > check_stop: ##Stops the loop once a set number of wells has been complete
        break
        
    startval = pic_any(block[0:1]) ## first two characters of a block
    
    print(startval)
    print(type(startval))
    print(pic_any(block))
    
    
    """
    Selecting layout based on leading startval
    and parsing record based on the selected layout
    """
    layout = oilProd_layout(startval)['layout'] ##identifies layout based on record start values
    parsed_vals = parse_record(block, layout) ##formats the record and returns a formated {dict} 

    temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
    #temp_df['api10'] = API ##adds API number to record (might need to move this to first position)

    print(temp_df)
    
    wellct+=1