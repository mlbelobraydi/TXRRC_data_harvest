# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:27:23 2020

@author: MBelobraydic
"""
import argparse
import os
import sys
import pandas as pd
import json
from ebcdic_main import yield_blocks, parse_record
from layouts_wells_dbf900 import dbf900_layout
from ebcdic_formats import pic_yyyymmdd, pic_numeric, pic_any



def main():
    file_path, out_dir = parse_args()

    
    block_size  = 247 ##block size for each record in the file
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
    ## now linked to 22 wb14b2rm_df = pd.DataFrame() ##28 Recurring JSON best linked to 22
    

    
    """Loop section for all records or partial set"""
       
    for block in yield_blocks(file, block_size): ##for each block in file
    
        ##For testing script
        if Limiting_Counter == True and wellct > check_stop: ##Stops the loop once a set number of wells has been complete
            break
        
    
        startval = pic_any(block[0:2]) ## first two characters of a block
        
        """
        Holding unique key values for the current record structure. 
        Reset when new record "01" is found.
        """        
        if startval == '01': ##captures the API number for databasing
            API = API = '42'+ pic_any(block[2:10]) ##api value in records '01'
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
            wbcplkey = pic_any(block[2:15]) ##key for 03 ->04 05 06 07 08 09 10 11  ##similar to wbplugkey and wbplugkey
            fluid_code_02 = pic_any(block[2:3]) 
            
            
        if startval == '03': ##captures wbfilekey unique key for databasing
            wbfilekey = pic_numeric(block[2:10]) ##key for 04 05 06 07 08 09 10 11
        
        if startval == '14': ##captures wbfiledt unique key for databasing
            wbfiledt = pic_yyyymmdd(block[2:10]) ##key for 15 16 17 18 19
            wbplugkey = pic_any(block[177:190]).strip() ##similar to wbcplkey and wb14b2ky
            fluid_code_14 = pic_any(block[177:178]) ##Unknown if this needs to be captured since it is simlar to fluid_code in 02
        
        if startval == '20': ##captures wbpmtnum unique key for databasing
            wbpmtnum = pic_any(block[2:8]) ##key for 21 
            
        if startval == '22': ##captures wb14b2ky  unique key for databasing
            wb14b2ky = pic_any(block[2:15]).strip() ##key for 28  ##similar to wbcplkey and wbplugkey
            fluid_code_22 = pic_any(block[2:3]) ##Unknown if this needs to be captured since it is simlar to fluid_code in 02
            
        if startval == '23':
            h15_key = pic_numeric(block[2:10]) ##key for 24 WB-H15-DATE-KEY Derived by subtracting the mailing date for the H-15 Listing from 999999999.  This provides us with a date key
        
        """
        Selecting layout based on leading startval
        and parsing record based on the selected layout
        """
        layout = dbf900_layout(startval)['layout'] ##identifies layout based on record start values
        parsed_vals = parse_record(block, layout) ##formats the record and returns a formated {dict} 

        temp_df  = pd.DataFrame([parsed_vals], columns=parsed_vals.keys()) ##convert {dict} to dataframe
        temp_df['api10'] = API ##adds API number to record (might need to move this to first position)
        
        """Dataframe loading and correcting (as necessary)"""
        if startval =='01': ##
            wbroot_df = wbroot_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='02':
            ##add unique keys
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            ## break up 'WB-OIL-GAS-INFO' based on fluid_code_02 'o' vs 'g'
            wbcompl_df = wbcompl_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='03':
            ##add unique keys
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            temp_df['wbfilekey'] = wbfilekey ##adds wbfilekey to record for link to 04 05 06 07 08 09 10 11
            wbdate_df = wbdate_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        
        elif startval =='04': ###temporary
            """Should be appended to 03 by JSON"""
            ##add unique keys
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            temp_df['wbfilekey'] = wbfilekey ##adds wbfilekey to record for link to 04 05 06 07 08 09 10 11
            wbrmks_df = wbrmks_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        
        elif startval =='05':
            ##add unique keys
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            temp_df['wbfilekey'] = wbfilekey ##adds wbfilekey to record for link to 04 05 06 07 08 09 10 11
            wbtube_df = wbtube_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='06':
            ##add unique keys
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            temp_df['wbfilekey'] = wbfilekey ##adds wbfilekey to record for link to 04 05 06 07 08 09 10 11
            wbcase_df = wbcase_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='07':
            ##add unique keys
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            temp_df['wbfilekey'] = wbfilekey ##adds wbfilekey to record for link to 04 05 06 07 08 09 10 11
            wbperf_df = wbperf_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='08':
            ##add unique keys
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            temp_df['wbfilekey'] = wbfilekey ##adds wbfilekey to record for link to 04 05 06 07 08 09 10 11
            wbline_df = wbline_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='09':
            ##add unique keys
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            temp_df['wbfilekey'] = wbfilekey ##adds wbfilekey to record for link to 04 05 06 07 08 09 10 11
            wbform_df = wbform_df.append(temp_df, ignore_index=True) ##appends results to dataframe  
        elif startval =='10':
            ##add unique keys
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            temp_df['wbfilekey'] = wbfilekey ##adds wbfilekey to record for link to 04 05 06 07 08 09 10 11
            wbsqeze_df = wbsqeze_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='11':
            ##add unique keys
            temp_df['wbcplkey'] = wbcplkey ##adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11
            temp_df['wbfilekey'] = wbfilekey ##adds wbfilekey to record for link to 04 05 06 07 08 09 10 11
            wbfresh_df = wbfresh_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        
        elif startval =='12':
            wboldloc_df = wboldloc_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='13':
            wbnewloc_df = wbnewloc_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        
        elif startval =='14':
            ##add unique keys
            temp_df['wbfiledt'] = wbfiledt ##adds wbfiledt to record for 15 16 17 18 19
            temp_df['wbplugkey'] = wbplugkey ##adds wbplugkey to record for 15 16 17 18 19
            ## break up 'WB-OIL-GAS-INFO' based on fluid_code_14 'o' vs 'g'
            wbplug_df = wbplug_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='15':
             ##add unique keys
            temp_df['wbfiledt'] = wbfiledt ##adds wbfiledt to record for 15 16 17 18 19
            temp_df['wbplugkey'] = wbplugkey ##adds wbplugkey to record for 15 16 17 18 19
            wbplrmks_df = wbplrmks_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='16':
             ##add unique keys
            temp_df['wbfiledt'] = wbfiledt ##adds wbfiledt to record for 15 16 17 18 19
            temp_df['wbplugkey'] = wbplugkey ##adds wbplugkey to record for 15 16 17 18 19
            wbplrec_df = wbplrec_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='17':
            ##add unique keys
            temp_df['wbfiledt'] = wbfiledt ##adds wbfiledt to record for 15 16 17 18 19
            temp_df['wbplugkey'] = wbplugkey ##adds wbplugkey to record for 15 16 17 18 19
            wbplcase_df = wbplcase_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='18':
             ##add unique keys
            temp_df['wbfiledt'] = wbfiledt ##adds wbfiledt to record for 15 16 17 18 19
            temp_df['wbplugkey'] = wbplugkey ##adds wbplugkey to record for 15 16 17 18 19
            wbplperf_df = wbplperf_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='19':
             ##add unique keys
            temp_df['wbfiledt'] = wbfiledt ##adds wbfiledt to record for 15 16 17 18 19
            temp_df['wbplugkey'] = wbplugkey ##adds wbplugkey to record for 15 16 17 18 19
            wbplname_df = wbplname_df.append(temp_df, ignore_index=True) ##appends results to dataframe      
        
        elif startval =='20':
            ##add unique keys
            temp_df['wbpmtnum'] = wbpmtnum ##adds unique wbpmtnum key for record 21
            wbdrill_df = wbdrill_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='21':
            ##add unique keys
            temp_df['wbpmtnum'] = wbpmtnum ##adds unique wbpmtnum key from record 20
            wbwellid_df = wbwellid_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='22':
            ##add unique keys
            temp_df['wb14b2ky'] = wb14b2ky ##adds wb14b2ky unique key to record
            temp_df['wb14b2rm'] = None
            ## break up 'WB-OIL-GAS-INFO' based on fluid_code_22 'o' vs 'g'
            wb14b2_df = wb14b2_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='23':
            """each record needs to get the associated 24 remarks in json"""
            ##add unique keys
            temp_df['h15_key'] = h15_key ##adds h15_key to record 
            wbh15_df = wbh15_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        
        elif startval =='24':###temporary
            ##this section should be json and added to the remark field in the correct row for wb15_df 
            ##need to combine multiple 24 records into single json entry for 23
            ##how to trigger entry?
            ##add unique keys
            """using dataframe for testing, needs to be json and can be multiple remarks for single 23 record"""
            temp_df['h15_key'] = h15_key ##adds the h15_key from previous 23 record
            wbh15rmk_df = wbh15rmk_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        
        elif startval =='25':
            wbsb126_df = wbsb126_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='26':            
            wbdastat_df = wbdastat_df.append(temp_df, ignore_index=True) ##appends results to dataframe
        elif startval =='27':
            wbw3c_df = wbw3c_df.append(temp_df, ignore_index=True) ##appends results to dataframe
            
        elif startval =='28':###temporary
            ##add unique keys
            temp_df['wb14b2ky'] = wb14b2ky ##unique key from 22
            
            """ grabs exising 28 JSON field in 22 wb14b2_df ## None if first """
            wb14b2rm_json_28 = wb14b2_df.loc[(wb14b2_df['api10'] == API) & (wb14b2_df['wb14b2ky'] == wb14b2ky), ['wb14b2rm']].values[0][0]
            
            """ Adds JSON record of 28 to any previous values """
            if wb14b2rm_json_28: ## verifies if the value is not null
                wb14b2rm_json_28 = json.dumps(json.loads(wb14b2rm_json_28) + temp_df.to_json(orient="records"))
            else: ## if null (for first 28 record for a given 22 record)
                wb14b2rm_json_28 = json.dumps(temp_df.to_json(orient="records"))
            
            """writes record back to the correct position in 22 wb14b2_df """
            wb14b2_df.loc[(wb14b2_df['api10'] == API) & (wb14b2_df['wb14b2ky'] == wb14b2ky), ['wb14b2rm']] = wb14b2rm_json_28
            
            ## previous version 28 to seperate dataframe <delete when above works correctly>
            ## wb14b2rm_df = wb14b2rm_df.append(temp_df, ignore_index=True) ##appends results to dataframe
            
        ct+=1 ## count for number of records being reviewed by script
        
        """printable counter and percent to keep track in console"""
        ##the counter isn't necessary, but it helps to determine if it is still running.
        use_counter = True
        if use_counter:
            sys.stdout.write("\r record:{0} well#:{1}".format(ct,wellct))
            sys.stdout.flush()
        
    
    print('\n Writing results to disk...')
    
    ##Currently writing to CSV
    ##  Could be changed to XLS or written to SQL
    ##  Need to determine how all the different sections link prior to decision

    ##for local storage
    base_path = out_dir + os.sep + r'dbf900'
    path_ext = r'.csv'
    
    wbroot_df.to_csv(base_path+'01_wbroot'+path_ext, index=False) ##01
    wbcompl_df.to_csv(base_path+'02_wbcompl'+path_ext, index=False) ##02 
    wbdate_df.to_csv(base_path+'03_wbdate'+path_ext, index=False) ##03
    
    ##04 is temporary here and will need to be handeled differently
    wbrmks_df.to_csv(base_path+'04_wbrmks'+path_ext, index=False) ##04 
    
    wbtube_df.to_csv(base_path+'05_wbtube'+path_ext, index=False) ##05 
    wbcase_df.to_csv(base_path+'06_wbcase'+path_ext, index=False) ##06
    wbperf_df.to_csv(base_path+'07_wbperf'+path_ext, index=False) ##07
    wbline_df.to_csv(base_path+'08_wbline'+path_ext, index=False) ##08
    wbform_df.to_csv(base_path+'09_wbform'+path_ext, index=False) ##09
    wbsqeze_df.to_csv(base_path+'10_wbsqeze'+path_ext, index=False) ##10
    wbfresh_df.to_csv(base_path+'11_wbfresh'+path_ext, index=False) ##11

    wboldloc_df.to_csv(base_path+'12_wboldloc'+path_ext, index=False) ##12
    wbnewloc_df.to_csv(base_path+'13_wbnewloc'+path_ext, index=False) ##13
    wbplug_df.to_csv(base_path+'14_wbplug'+path_ext, index=False) ##14
    
    ##15 is temporary here and will need to be handeled differently
    wbplrmks_df.to_csv(base_path+'15_wbplrmks'+path_ext, index=False) ##15
    
    wbplrec_df.to_csv(base_path+'16_wbplrec'+path_ext, index=False) ##16
    wbplcase_df.to_csv(base_path+'17_wbplcase'+path_ext, index=False) ##17
    wbplperf_df.to_csv(base_path+'18_wbplperf'+path_ext, index=False) ##18
    wbplname_df.to_csv(base_path+'19_wbplname'+path_ext, index=False) ##19
    
    wbdrill_df.to_csv(base_path+'20_wbdrill'+path_ext, index=False) ##20
    wbwellid_df.to_csv(base_path+'21_wbwellid'+path_ext, index=False) ##21
    wb14b2_df.to_csv(base_path+'22_wb14b2'+path_ext, index=False) ##22
    wbh15_df.to_csv(base_path+'23_wbh15'+path_ext, index=False) ##23
    
    ##24 is temporary here and will need to be handeled differently
    wbh15rmk_df.to_csv(base_path+'24_wbh15rmk'+path_ext, index=False) ##24
    
    wbsb126_df.to_csv(base_path+'25_wbsb126'+path_ext, index=False) ##25
    wbdastat_df.to_csv(base_path+'26_wbdastat'+path_ext, index=False) ##26
    wbw3c_df.to_csv(base_path+'27_wbw3c'+path_ext, index=False) ##27
    
    ##28 is commented out since the code now combines 28 into 22
    ##wb14b2rm_df.to_csv(base_path+'28_wb14b2rm'+path_ext, index=False) ##28
    
    file.close()


def get_parser():
    desc = "Process oil and gas well data from the Texas Railroad Commission"
    parser = argparse.ArgumentParser(
        description=desc,
    )

    parser.add_argument("--filepath", required=False, help="path to source data file")
    parser.add_argument(
        "--outdir", required=False, help="directory path to write the processed data"
    )
    return parser


def parse_args():
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])
    if args.filepath:
        # python WorkingFileForTesting.py --filepath data/dbf900.ebc
        file_path = args.filepath
    else:
        ## Default input data source
        file_path = r"C:\PublicData\Texas\TXRRC\index\dbf900.ebc"
        ##file origin: ftp://ftpe.rrc.texas.gov/shfwba/dbf900.ebc.gz
        ##file size: 1.96MB-ish

    if not os.path.isfile(file_path):
        print("File Error: {} is not a file\n".format(file_path))
        parser.print_help(sys.stderr)
        parser.exit(1)

    if args.outdir:
        # python WorkingFileForTesting.py --outdir C:\mydatabase
        out_dir = args.outdir
    else:
        ## Default local storage location
        out_dir = r"C:\PublicData\Texas\TXRRC\database"

    if not os.path.isdir(out_dir):
        print("Directory Error: {} is not a directory\n".format(out_dir))
        parser.print_help(sys.stderr)
        parser.exit(1)

    return file_path, out_dir

    
if __name__ == '__main__': 
    main()
    print('WorkingFileForTesting.py complete.')
