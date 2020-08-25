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
from dbf900_formats import pic_yyyymmdd, pic_yyyymm, pic_latlong, pic_coord, pic_numeric, pic_any




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
    wellct = 0 ##counter for number of wells
    check = 0 ##while loop counter based on script
    check_stop = 500 ##number of while loop runs to complete before stopping
    
    
    """
    DataFrame and JSON items for each sections
    https://www.rrc.texas.gov/media/41906/wba091_well-bore-database.pdf
    """
    wbroot_df = pd.DataFrame() ##01 Not Recurring dataframe
    wbcompl_df = pd.DataFrame() ##02 Recurring dataframe most likely linked to 1 with error in .pdf manual
    wbdate_df = pd.DataFrame() ##03 Recurring dataframe linked to 02
    wbrmks_df = pd.DataFrame() ##04 Recurring JSON best linked to 03
    wbtube_df = pd.DataFrame() ##05 Recurring linked to 03
    wbcase_df = pd.DataFrame() ##06 Recurring linked to 03
    wbperf_df = pd.DataFrame() ##07 Recurring linked to 03
    wbline_df = pd.DataFrame() ##08 Recurring linked to 03
    wbform_df = pd.DataFrame() ##09 Recurring linked to 03
    wbsqeze_df = pd.DataFrame() ##10 Recurring linked to 03
    wbfresh_df = pd.DataFrame() ##11 Recurring linked to 03
    wboldloc_df = pd.DataFrame() ##12 Not Recurring linked to 01
    wbnewloc_df = pd.DataFrame() ##13 Not Recurring linked to 01
    wbplug_df = pd.DataFrame() ##14 Recurring linked to 01
    wbplrmks_df = pd.DataFrame() ##15 Recurring JSON best linked to 14
    wbplrec_df = pd.DataFrame() ##16 Not Recurring linked to 14
    wbplcase_df = pd.DataFrame() ##17 Recurring linked to 14
    wbplperf_df = pd.DataFrame() ##18 Recurring linked to 14
    wbplname_df = pd.DataFrame() ##19 Not Recurring JSON? linked to 14
    wbdrill_df = pd.DataFrame() ##20 Recurring linked to 01
    wbwellid_df = pd.DataFrame() ##21 Recurring linked to 20
    wb14b2_df = pd.DataFrame() ##22 Recurring linked to 01
    wbh15_df = pd.DataFrame() ##23 Recurring linked to 01
    wbh15rmk_df = pd.DataFrame() ##24 Recurring JSON best linked to 23
    wbsb126_df = pd.DataFrame() ##25 Recurring linked to 01
    wbdastat_df = pd.DataFrame() ##26 Recurring linked to 01
    wbw3c_df = pd.DataFrame() ##27 Recurring linked to 01
    wb14b2rm_df = pd.DataFrame() ##28 Recurring JSON best linked to 22
    
    
    sample_records = split_records #[34000:65000] ## Used for testing to reduce number of records to run
    total_records = len(sample_records) ##modify if sample_records isn't used
    
    """Loop section for all records or partial set
       Select method based on goals and what is being tested"""
    ##for record in split_records: ##full file run
    ##for record in sample_records: ##if using sample records to limit run
    ##while check < check_stop: ##if using while loop to limit run
    while wellct < check_stop:  ##while look for first XX number of wells
    
        record = sample_records[ct] ##not necessary for for-loops
        
        startval = str(record[0:2])
        
        """
        Holding unique key values for the current record structure. 
        Reset when new record "01" is found.
        """        
        if startval == '01': ##captures the API number for databasing
            API = '42'+record[2:10] ##42 is the state code for Texas + the county and unique api number
            wellct+=1
            ##Might be helpful to find the next occurance of a record staring with "01"
            ##This way all the associated items are added to the right sections with a check of completion
            wbcplkey = None ## defined in '02' cleared upon new API 
            fluid_code_02 = None ## defined in '02' cleared upon new API 
            wbfilekey = None ## defined in '03' cleared upon new API
            wbfiledt = None ## defined in '14' cleared upon new API
            wbplugkey = None ## defined in '14' cleared upon new API
            fluid_code_14 = None ## defined in '14' cleared upon new API
            wbpmtnum = None ## defined in '20' cleared upon new API
            wb14b2ky = None ## defined in '22' cleared upon new API
            fluid_code_22 = None ## defined in '22' cleared upon new API
            h15_key = None ## defined in '23' cleared upon new API
        
        if startval == '02': ##captures wbcplkey unique key for databasing
            wbcplkey = str(record[2:15]).strip() ##key for 03 ->04 05 06 07 08 09 10 11  ##similar to wbplugkey and wbplugkey
            fluid_code_02 = str(record[2]) 
            
        if startval == '03': ##captures wbfilekey unique key for databasing
            wbfilekey = int(record[2:10]) ##key for 04 05 06 07 08 09 10 11
        
        if startval == '14': ##captures wbfiledt unique key for databasing
            wbfiledt = pic_yyyymmdd(record[2:10]) ##key for 15 16 17 18 19
            wbplugkey = str(record[177:190]).strip() ##similar to wbcplkey and wb14b2ky
            fluid_code_14 = str(record[177]) ##Unknown if this needs to be captured since it is simlar to fluid_code in 02
        
        if startval == '20': ##captures wbpmtnum unique key for databasing
            wbpmtnum = int(record[2:7]) ##key for 21 
            
        if startval == '22': ##captures wb14b2ky  unique key for databasing
            wb14b2ky = str(record[2:15]).strip() ##key for 28  ##similar to wbcplkey and wbplugkey
            fluid_code_22 = str(record[2]) ##Unknown if this needs to be captured since it is simlar to fluid_code in 02
            
        if startval == '23':
            h15_key = int(record[2:10]) ##key for 24 WB-H15-DATE-KEY Derived by subtracting the mailing date for the H-15 Listing from 999999999.  This provides us with a date key
        
        """
        Selecting layout based on leading startval
        and parsing record based on the selected layout
        """
        layout = dbf900_layout(startval)['layout'] ##identifies layout based on record start values
        parsed_vals = parse_record(record, layout) ##formats the record and returns a formated {dict} 


        """Dataframe loading and correcting (as necessary)"""
        if startval =='01': ##currently reviewing results vs. original record.
            #check+=1 ##used for while loops to manage run length this location counts for each well
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            wbroot_df = wbroot_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='02':
            #check+=1 ##used for while loops to manage run length this location counts for each well
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            ## break up 'WB-OIL-GAS-INFO' based on fluid_code_02 'o' vs 'g'
            wbcompl_df = wbcompl_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='03':
            #check+=1 ##used for while loops to manage run length this location counts for each well
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            temp_df['wbfilekey'] = wbfilekey ##adds wbfilekey to record for link to 04 05 06 07 08 09 10 11
            wbdate_df = wbdate_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        # elif startval =='04':
            
        # elif startval =='05':
            
        # elif startval =='06':
            
        # elif startval =='07':
            
        # elif startval =='08':
            
        # elif startval =='09':
            
        # elif startval =='10':
            
        # elif startval =='11':
            
        elif startval =='12':
            #check+=1 ##used for while loops to manage run length this location counts for each well
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            wboldloc_df = wboldloc_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='13':
            #check+=1 ##used for while loops to manage run length this location counts for each well
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            wbnewloc_df = wbnewloc_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='14':
            #check+=1 ##used for while loops to manage run length this location counts for each well
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            temp_df['wbfiledt'] = wbfiledt ##adds wbfiledt to record for 15 16 17 18 19
            temp_df['wbplugkey'] = wbplugkey ##adds wbplugkey to record for 15 16 17 18 19
            ## break up 'WB-OIL-GAS-INFO' based on fluid_code_14 'o' vs 'g'
            wbplug_df = wbplug_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        # elif startval =='15':
            
        # elif startval =='16':
            
        # elif startval =='17':
            
        # elif startval =='18':
            
        # elif startval =='19':
            
        # elif startval =='20':
            
        # elif startval =='21':
            
        # elif startval =='22':
            
        #     ## break up 'WB-OIL-GAS-INFO' based on fluid_code_22 'o' vs 'g'
            
        elif startval =='23':
            """each record needs to get the associated 24 remarks in json"""
            #check+=1 ##used for while loops to manage run length this location counts for each well
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            wbh15_df = wbh15_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        
        elif startval =='24':
            ##this section should be json and added to the remark field in the correct row for wb15_df 
            ##need to combine multiple 24 records into single json entry for 23
            ##how to trigger entry?
            #check+=1 ##used for while loops to manage run length this location counts for each well
            """using dataframe for testing, needs to be json and can be multiple remarks for single 23 record"""
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            temp_df['h15_key'] = h15_key ##adds the h15_key from previous 23 record
            wbh15rmk_df = wbh15rmk_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        
        elif startval =='25':
            #check+=1 ##used for while loops to manage run length this location counts for each well
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            wbsb126_df = wbsb126_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='26':
            #check+=1 ##used for while loops to manage run length this location counts for each well
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            wbdastat_df = wbdastat_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='27':
            #check+=1 ##used for while loops to manage run length this location counts for each well
            temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
            temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
            wbw3c_df = wbw3c_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        # elif startval =='28':
            
            
        ct+=1 ## count for number of records being reviewed by script
        
        """printable counter and percent to keep track in console"""
        ##the counter isn't necessary, but it helps to determine if it is still running.
        use_counter = True
        if use_counter:
            status = round((ct/total_records)*100,3)
            sys.stdout.write("\r record:{0} complete:{1}% well#:{2}".format(ct,status,wellct))
            sys.stdout.flush()
        
    
    print('\n Writing results to disk...')
    
    ##Currently writing to CSV
    ##  Could be changed to XLS or written to SQL
    ##  Need to determine how all the different sections link prior to decision
    base_path = r'C:\PublicData\Texas\TXRRC\database\dbf900_' ##for local storage
    path_ext = r'.csv'
    
    wbroot_df.to_csv(base_path+'01_wbroot'+path_ext, index=False) ##01
    wbcompl_df.to_csv(base_path+'02_wbcompl'+path_ext, index=False) ##02 
    wbdate_df.to_csv(base_path+'03_wbdate'+path_ext, index=False) ##03
        ##04 05 06 07 08 09 10 11
    wboldloc_df.to_csv(base_path+'12_wboldloc'+path_ext, index=False) ##12
    wbnewloc_df.to_csv(base_path+'13_wbnewloc'+path_ext, index=False) ##13
    wbplug_df.to_csv(base_path+'14_wbplug'+path_ext, index=False) ##14
        ##15 16 17 18 19
    ##20 ->21
    ##22 ->28
    wbh15_df.to_csv(base_path+'23_wbh15'+path_ext, index=False) ##23
    
    ##24 is temporary here and will need to be handeled differently
    wbh15rmk_df.to_csv(base_path+'24_wbh15rmk'+path_ext, index=False) ##24
    
    wbsb126_df.to_csv(base_path+'25_wbsb126'+path_ext, index=False) ##25
    wbdastat_df.to_csv(base_path+'26_wbdastat'+path_ext, index=False) ##26
    wbw3c_df.to_csv(base_path+'27_wbw3c'+path_ext, index=False) ##27
    
    
if __name__ == '__main__': 
    main()
    print('WorkingFileForTesting.py complete.')