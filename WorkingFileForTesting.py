# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:27:23 2020

@author: MBelobraydic
"""
import sys
import pandas as pd
import json
from dbf900_main import decode_file, parse_record
from dbf900_layouts import dbf900_layout





def main():
    file = r'C:\PublicData\Texas\TXRRC\index\dbf900.ebc' ##Local storage location
    ##file origin: ftp://ftpe.rrc.texas.gov/shfwba/dbf900.ebc.gz
    
    block_size  = 247 ##block size for each record in the file
    ##Unknown if this holds true for all versions of this file or for other files on TXRRC
    
    ##file and block size sent to decode and return record array    
    split_records = decode_file(file,block_size)
    ##the records in this array have a leading two character code to
    ##know how it should be split apart and treated.    
    
    
    """
    ##Section for testing the outputs
    """  
    API = None ##this needs to be inplace incase the random part of the array selected does start on an 01 record
    ct = 0 ##counter for number of records
    check = 0 ##while loop counter based on script
    check_stop = 10000 ##number of while loop runs to complete before stopping
    
    
    """DataFrame and JSON items for each sections"""
    wbroot_df = pd.DataFrame() ##01 Not Recurring dataframe
    ##02 Recurring dataframe unknown how to link
    ##03 Recurring dataframe linked to 02
    ##04 Recurring JSON best linked to 03
    ##05 Recurring linked to 03
    ##06 Recurring linked to 03
    ##07 Recurring linked to 03
    ##08 Recurring linked to 03
    ##09 Recurring linked to 03
    ##10 Recurring linked to 03
    ##11 Recurring linked to 03
    ##12 Not Recurring linked to 01
    ##13 Not Recurring linked to 01
    ##14 Recurring linked to 01
    ##15 Recurring JSON best linked to 14
    ##16 Not Recurring linked to 14
    ##17 Recurring linked to 14
    ##18 Recurring linked to 14
    ##19 Not Recurring JSON? linked to 14
    ##20 Recurring linked to 01
    ##21 Recurring linked to 20
    ##22 Recurring linked to 01
    ##23 Recurring linked to 01
    ##24 Recurring JSON best linked to 23
    ##25 Recurring linked to 01
    ##26 Recurring linked to 01
    ##27 Recurring linked to 01
    ##28 Recurring JSON best linked to 22
    
    
    sample_records = split_records #[34000:65000] ## Used for testing to reduce number of records to run
    total_records = len(sample_records) ##modify if sample_records isn't used
    
    """Loop section for all records or partial set
       Select method based on goals and what is being tested"""
    ##for record in split_records: ##full file run
    ##for record in sample_records: ##if using sample records to limit run
    
    while check < check_stop: ##if using while loop to limit run
        record = sample_records[ct] ##not necessary for for-loops
        
        
        
        if record.startswith('01'): ##captures the API number for databasing
            API = '42'+record[2:10]
        
        startval = str(record[0:2])
        layout = dbf900_layout(startval)['layout'] ##identifies layout based on record start values
        parsed_vals = parse_record(record, layout) ##formats the record and returns a formated {dict} 

        
        if startval =='01': ##currently reviewing results vs. original record. Use 01 through 28 to check results.
            
            check+=1 ##used for while loops to manage run length this location counts for each well
            
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            wbroot_df = wbroot_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        
        
        ct+=1 ## count for number of records being reviewed by script
        
        """printable counter and percent to keep track in console"""
        ##the counter isn't necessary, but it helps to determine if it is still running.
        status = round((ct/total_records)*100,3)
        sys.stdout.write("\r record:{0} complete:{1}%".format(ct,status))
        sys.stdout.flush()
        
    
    print('Writing results to disk...')
    
    ##Currently writing to CSV
    ##  Could be changed to XLS or written to SQL
    ##  Need to determine how all the different sections link prior to decision
    wbroot_path = r'C:\PublicData\Texas\TXRRC\database\dbf900_wbroot.csv' ## local storage for output
    wbroot_df.to_csv(wbroot_path, index=False)
    
    
    
if __name__ == '__main__': 
    main()
    print('WorkingFileForTesting.py complete.')