# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 14:27:23 2020

@author: MBelobraydic
"""
import argparse
import os
import sys
import polars as pl
import json
from typing import Union
from tqdm import tqdm

from ebcdic_main import yield_blocks, parse_record
from layouts_wells_dbf900 import dbf900_layout
from ebcdic_formats import pic_yyyymmdd, pic_numeric, pic_any

# TODO: refactor to use something other than Pandas df.append(...)
import warnings
warnings.filterwarnings(action='ignore', category=FutureWarning, message='The frame.append method is deprecated and will be removed from pandas in a future version.') # setting ignore as a parameter and further adding category

def run_parser(input_ebcdic_file_path: str, out_dir: str, limit_well_count: Union[int, None] = None):
        
    block_size = 247 ##block size for each record in the file
    ##Unknown if this holds true for all versions of this file or for other files on TXRRC
    
    print('opening',input_ebcdic_file_path,'...')
    with open(input_ebcdic_file_path, 'rb') as file:
        
        api10 = None ##this needs to be inplace incase the random part of the array selected does start on an 01 record
        record_count = 0 ##counter for number of records
        well_count = 0 ##counter for number of wells
        estimated_total_block_count = int(round(os.path.getsize(input_ebcdic_file_path) / block_size))
        
        """
        DataFrame and JSON items for each sections
        https://www.rrc.texas.gov/media/41906/wba091_well-bore-database.pdf
        """

        data_store: dict[dict] = {
            '01' : {'name': 'WBROOT', 'temp_dictlist': []},
            '02' : {'name': 'WBCOMPL', 'temp_dictlist': []},
            '03' : {'name': 'WBDATE', 'temp_dictlist': []},
            '04' : {'name': 'WBRMKS', 'temp_dictlist': []},
            '05' : {'name': 'WBTUBE', 'temp_dictlist': []},
            '06' : {'name': 'WBCASE', 'temp_dictlist': []},
            '07' : {'name': 'WBPERF', 'temp_dictlist': []},
            '08' : {'name': 'WBLINE', 'temp_dictlist': []},
            '09' : {'name': 'WBFORM', 'temp_dictlist': []},
            '10' : {'name': 'WBSQEZE', 'temp_dictlist': []},
            '11' : {'name': 'WBFRESH', 'temp_dictlist': []},
            '12' : {'name': 'WBOLDLOC', 'temp_dictlist': []},
            '13' : {'name': 'WBNEWLOC', 'temp_dictlist': []},
            '14' : {'name': 'WBPLUG', 'temp_dictlist': []},
            '15' : {'name': 'WBPLRMKS', 'temp_dictlist': []},
            '16' : {'name': 'WBPLREC', 'temp_dictlist': []},
            '17' : {'name': 'WBPLCASE', 'temp_dictlist': []},
            '18' : {'name': 'WBPLPERF', 'temp_dictlist': []},
            '19' : {'name': 'WBPLNAME', 'temp_dictlist': []},
            '20' : {'name': 'WBDRILL', 'temp_dictlist': []},
            '21' : {'name': 'WBWELLID', 'temp_dictlist': []},
            '22' : {'name': 'WB14B2', 'temp_dictlist': []},
            '23' : {'name': 'WBH15', 'temp_dictlist': []},
            '24' : {'name': 'WBH15RMK', 'temp_dictlist': []},
            '25' : {'name': 'WBSB126', 'temp_dictlist': []},
            '26' : {'name': 'WBDASTAT', 'temp_dictlist': []},
            '27' : {'name': 'WBW3C', 'temp_dictlist': []},
            '28' : {'name': 'WB14B2RM', 'temp_dictlist': []},
        }

        # The following is kept for comment purposes
        # wbroot_dictlist = [] ##01 Not Recurring dataframe
        # wbcompl_dictlist = [] ##02 Recurring dataframe most likely linked to 1 with error in .pdf manual
        # wbdate_dictlist = [] ##03 Recurring dataframe linked to 02
        # wbrmks_dictlist = [] ##04 Recurring JSON best linked to 03
        # wbtube_dictlist = [] ##05 Recurring linked to 03
        # wbcase_dictlist = [] ##06 Recurring linked to 03
        # wbperf_dictlist = [] ##07 Recurring linked to 03
        # wbline_dictlist = [] ##08 Recurring linked to 03
        # wbform_dictlist = [] ##09 Recurring linked to 03
        # wbsqeze_dictlist = [] ##10 Recurring linked to 03
        # wbfresh_dictlist = [] ##11 Recurring linked to 03
        # wboldloc_dictlist = [] ##12 Not Recurring linked to 01
        # wbnewloc_dictlist = [] ##13 Not Recurring linked to 01
        # wbplug_dictlist = [] ##14 Recurring linked to 01
        # wbplrmks_dictlist = [] ##15 Recurring JSON best linked to 14
        # wbplrec_dictlist = [] ##16 Not Recurring linked to 14
        # wbplcase_dictlist = [] ##17 Recurring linked to 14
        # wbplperf_dictlist = [] ##18 Recurring linked to 14
        # wbplname_dictlist = [] ##19 Not Recurring JSON? linked to 14
        # wbdrill_dictlist = [] ##20 Recurring linked to 01
        # wbwellid_dictlist = [] ##21 Recurring linked to 20
        # wb14b2_dictlist = [] ##22 Recurring linked to 01
        # wbh15_dictlist = [] ##23 Recurring linked to 01
        # wbh15rmk_dictlist = [] ##24 Recurring JSON best linked to 23 # TODO: move back into 23
        # wbsb126_dictlist = [] ##25 Recurring linked to 01
        # wbdastat_dictlist = [] ##26 Recurring linked to 01
        # wbw3c_dictlist = [] ##27 Recurring linked to 01
        # wb14b2rm_dictlist = [] ##28 Recurring JSON best linked to 22 # TODO: move back into 22

        
        """Loop section for all records or partial set"""

        # TODO: add a chunking loop herea
        
        for block in tqdm(yield_blocks(file, block_size), total=estimated_total_block_count, unit='block'): ##for each block in file
        
            ##For testing script
            if limit_well_count and well_count > limit_well_count: ##Stops the loop once a set number of wells has been complete
                print(f"Reached limit_well_count: {limit_well_count}")
                break
        
            startval = pic_any(block[0:2]) ## first two characters of a block
            
            """
            Holding unique key values for the current record structure. 
            Reset when new record "01" is found.
            """
            if startval == '01': ##captures the API number for databasing
                api10 = '42'+ pic_any(block[2:10]) ##api value in records '01'
                well_count+=1
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
            
            elif startval == '02': ##captures wbcplkey unique key for databasing
                wbcplkey = pic_any(block[2:15]) ##key for 03 ->04 05 06 07 08 09 10 11  ##similar to wbplugkey and wbplugkey
                fluid_code_02 = pic_any(block[2:3]) 
                
            elif startval == '03': ##captures wbfilekey unique key for databasing
                wbfilekey = pic_numeric(block[2:10]) ##key for 04 05 06 07 08 09 10 11
            
            elif startval == '14': ##captures wbfiledt unique key for databasing
                wbfiledt = pic_yyyymmdd(block[2:10]) ##key for 15 16 17 18 19
                wbplugkey = pic_any(block[177:190]).strip() ##similar to wbcplkey and wb14b2ky
                fluid_code_14 = pic_any(block[177:178]) ##Unknown if this needs to be captured since it is simlar to fluid_code in 02
            
            elif startval == '20': ##captures wbpmtnum unique key for databasing
                wbpmtnum = pic_any(block[2:8]) ##key for 21 
                
            elif startval == '22': ##captures wb14b2ky  unique key for databasing
                wb14b2ky = pic_any(block[2:15]).strip() ##key for 28  ##similar to wbcplkey and wbplugkey
                fluid_code_22 = pic_any(block[2:3]) ##Unknown if this needs to be captured since it is simlar to fluid_code in 02
                
            elif startval == '23':
                h15_key = pic_numeric(block[2:10]) ##key for 24 WB-H15-DATE-KEY Derived by subtracting the mailing date for the H-15 Listing from 999999999.  This provides us with a date key
            
            """
            Selecting layout based on leading startval
            and parsing record based on the selected layout
            """
            layout = dbf900_layout(startval)['layout'] ##identifies layout based on record start values
            parsed_vals: dict = parse_record(block, layout) ##formats the record and returns a formated {dict} 

            parsed_vals['api10'] = api10 ##adds API number to record (might need to move this to first position)
            
            """Fill carryover values for each section, as required"""
            if startval in ('02', '03', '04', '05', '06', '07', '08', '09', '10', '11'):
                parsed_vals['wbcplkey'] = wbcplkey ## adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11

            if startval in ('03', '04', '05', '06', '07', '08', '09', '10', '11'):
                parsed_vals['wbcplkey'] = wbcplkey ## adds wbcplkey to record for link to 03 04 05 06 07 08 09 10 11

            if startval in ('04', '05', '06', '07', '08', '09', '10', '11'):
                parsed_vals['wbfilekey'] = wbfilekey

            if startval in ('15', '16', '17', '18', '19'):
                parsed_vals['wbfiledt'] = wbfiledt ## adds wbfiledt to record for 15 16 17 18 19
                parsed_vals['wbplugkey'] = wbplugkey ## adds wbplugkey to record for 15 16 17 18 19

            if startval in ('20', '21'):
                parsed_vals['wbpmtnum'] = wbpmtnum ##adds unique wbpmtnum key for record 21
                
            if startval == '22':
                parsed_vals['wb14b2ky'] = wb14b2ky ##adds wb14b2ky unique key to record
                parsed_vals['wb14b2rm'] = None ## To be used for any following 28 sections
                
            if startval =='23':
                parsed_vals['h15_key'] = h15_key ##adds h15_key to record 
                parsed_vals['h15_remark'] = None ## To be used for any following 24 sections
            
            # FIXME: Combine these weirdnesses: 24 into 23; and 28 into 22
            if startval =='24': ###Loads any section 24 as JSON in associated 23
                parsed_vals['h15_key'] = h15_key ##adds the h15_key from previous 23 record
                
                """grab existing 24 JSON 'h15_remark' field from current section 23 ##None if first"""
                # wbh15rmk_json_24 = wbh15_df.loc[(wbh15_df['api10'] == api10) & (wbh15_df['h15_key'] == h15_key), ['h15_remark']].values[0][0] # FIXME: figure this out still
                
                """ Adds JSON record of 24 to any previous values """
                # FIXME: figure this out still
                # if wbh15rmk_json_24: ## verifies if the value is not null
                #     wbh15rmk_json_24 = json.dumps(json.loads(wbh15rmk_json_24) + temp_df.to_json(orient="records"))
                # else: ## if null (for first 24 record for a given 23 record)
                #     wbh15rmk_json_24 = json.dumps(temp_df.to_json(orient="records"))
                
                """writes record back to the correct position in 23 wbh15_df """
                # wbh15_df.loc[(wbh15_df['api10'] == api10) & (wbh15_df['h15_key'] == h15_key), ['h15_remark']] = wbh15rmk_json_24 # FIXME: figure this out still
                
            if startval =='28':### Loads section 28 as JSON into associated 22
                parsed_vals['wb14b2ky'] = wb14b2ky ##unique key from 22
                
                # """ grabs exising 28 JSON field in 22 wb14b2_df ## None if first """
                # wb14b2rm_json_28 = wb14b2_df.loc[(wb14b2_df['api10'] == api10) & (wb14b2_df['wb14b2ky'] == wb14b2ky), ['wb14b2rm']].values[0][0] # FIXME: figure this out still
                
                # """ Adds JSON record of 28 to any previous values """
                # FIXME: figure this out still
                # if wb14b2rm_json_28: ## verifies if the value is not null
                #     wb14b2rm_json_28 = json.dumps(json.loads(wb14b2rm_json_28) + temp_df.to_json(orient="records"))
                # else: ## if null (for first 28 record for a given 22 record)
                #     wb14b2rm_json_28 = json.dumps(temp_df.to_json(orient="records"))
                
                # """writes record back to the correct position in 22 wb14b2_df """
                # wb14b2_df.loc[(wb14b2_df['api10'] == api10) & (wb14b2_df['wb14b2ky'] == wb14b2ky), ['wb14b2rm']] = wb14b2rm_json_28 # FIXME: figure this out still
                
            # do the actual append
            data_store[startval]['temp_dictlist'].append(parsed_vals)

            record_count += 1 ## count for number of records being reviewed by script
            
            """printable counter and percent to keep track in console"""
            ##the counter isn't necessary, but it helps to determine if it is still running.
            use_counter = False # disabled since move to tqdm progress bar
            if use_counter:
                if limit_well_count:
                    sys.stdout.write(f"\r record:{record_count} well#:{well_count}/{limit_well_count} ({round(well_count/limit_well_count*100,2)}%)")
                else:
                    sys.stdout.write(f"\r record:{record_count} well#:{well_count}")
                sys.stdout.flush()
            
        
    print('\n Writing results to disk...')
    
    ##Currently writing to CSV
    ##  Could be changed to XLS or written to SQL
    ##  Need to determine how all the different sections link prior to decision

    ##for local storage
    base_path = os.path.join(out_dir, 'dbf900_')
    
    for startval in data_store.keys():
        df = pl.DataFrame(data_store[startval]['temp_dictlist'], infer_schema_length=10_000_000_000_000)
        csv_filename = f"{base_path}{startval}_{data_store[startval]['name']}.csv"
        df.write_csv(csv_filename)
    


def get_parser():
    desc = "Process oil and gas well data from the Texas Railroad Commission"
    parser = argparse.ArgumentParser(
        description=desc,
    )

    parser.add_argument("--filepath", required=False, help="path to source data file (dbf900.ebc)")
    parser.add_argument("--outdir", required=False, help="directory path to write the processed data")
    parser.add_argument("--limit", required=False, type=int, help="limit to this many wells processed")
    return parser


def parse_args():
    parser = get_parser()
    args = parser.parse_args(sys.argv[1:])
    if args.filepath:
        # python WorkingFileForTesting.py --filepath data/dbf900.ebc
        input_file_path = args.filepath
    else:
        ## Default input data source
        input_file_path = r"C:\PublicData\Texas\TXRRC\index\dbf900.ebc"
        ##file origin: ftp://ftpe.rrc.texas.gov/shfwba/dbf900.ebc.gz
        ##file size: 1.96MB-ish (uuuuh)

    if not os.path.isfile(input_file_path):
        print("File Error: {} is not a file\n".format(input_file_path))
        parser.print_help(sys.stderr)
        parser.exit(1)

    if args.outdir:
        # python WorkingFileForTesting.py --outdir C:\mydatabase
        out_dir = args.outdir
    else:
        ## Default local storage location
        out_dir = r"C:\PublicData\Texas\TXRRC\database"

    if args.limit:
        limit_well_count = args.limit
    else:
        limit_well_count = None

    if not os.path.isdir(out_dir):
        print("Directory Error: {} is not a directory\n".format(out_dir))
        parser.print_help(sys.stderr)
        parser.exit(1)

    return input_file_path, out_dir, limit_well_count

    
if __name__ == '__main__':
    input_file_path, out_dir, limit_well_count = parse_args()
    run_parser(input_file_path, out_dir, limit_well_count=limit_well_count)
    print('WorkingFileForTesting.py complete.')
