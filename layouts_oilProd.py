# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 11:12:44 2020

Files for this layout:
    ftp://ftpe.rrc.texas.gov/sholed
        ftp://ftpe.rrc.texas.gov/sholed/olf001l.ebc.gz
        ftp://ftpe.rrc.texas.gov/sholed/olf003l.ebc.gz
        ftp://ftpe.rrc.texas.gov/sholed/olf004l.ebc.gz
        ftp://ftpe.rrc.texas.gov/sholed/olf005l.ebc.gz
        ftp://ftpe.rrc.texas.gov/sholed/olf007l.ebc.gz
        ftp://ftpe.rrc.texas.gov/sholed/olf008l.ebc.gz
        ftp://ftpe.rrc.texas.gov/sholed/olf009l.ebc.gz
        ftp://ftpe.rrc.texas.gov/sholed/olf010l.ebc.gz
        ftp://ftpe.rrc.texas.gov/sholed/olf011l.ebc.gz
        ftp://ftpe.rrc.texas.gov/sholed/olf013l.ebc.gz
        ftp://ftpe.rrc.texas.gov/sholed/olf014l.ebc.gz
        ftp://ftpe.rrc.texas.gov/sholed/ReadMe.txt
        
    Layout Manual:
        https://www.rrc.texas.gov/media/1273/ola013k.pdf
"""

OIL_FIELD_01 = [
                ('TYPE-REC',0,1,'pic_numeric'),  ##PIC 9
                ('DIST',1,3,'pic_any'),  ##PIC XXX
                ('FIELD',4,8,'pic_numeric'),  ##PIC 9(8)
                ('OPR',12,6,'pic_numeric'),  ##PIC 9(6)
                ('LEASE',18,5,'pic_numeric'),  ##PIC 9(5)
                ('LEASE FILLER',23,2,'pic_numeric'),  ##PIC 99
                ('OFFSHORE',25,1,'pic_numeric'),  ##PIC 9
                ('F-NAME',26,32,'pic_any'),  ##PIC X(32)
                ('COUNTY',58,18,'pic_numeric'),  ##PIC 9(18)
                ('DISC-DATE',76,8,'pic_yyyymmdd'),  ##PIC 9(8)
                ('F-DEPTH',84,5,'pic_numeric'),  ##PIC 9(5)
                ('O-GRAV',89,3,'pic_numeric'),  ##PIC 999
                ('F-TYPE',92,1,'pic_numeric'),  ##PIC 9
                ('MULT-RES',93,1,'pic_numeric'),  ##PIC 9
                ('F-LPB',94,1,'pic_numeric'),  ##PIC 9
                ('F-XMT',95,1,'pic_numeric'),  ##PIC 9
                ('PRT-AS-IS',96,1,'pic_numeric'),  ##PIC 9
                ('YARD',97,1,'pic_numeric'),  ##PIC 9
                ('T-CODES',98,12,'pic_numeric'),  ##PIC 9(12)
                ('ALLOCATION',110,12,'pic_numeric'),  ##PIC 9(12)
                ('RES-AMT',122,6,'pic_numeric'),  ##PIC 9(6)
                ('F-GOR',128,6,'pic_numeric'),  ##PIC 9(6)
                ('F-TOP',134,5,'pic_numeric'),  ##PIC 9(5)
                ('F-NET',139,6,'pic_numeric'),  ##PIC 9(6)
                ('UNET',145,3,'pic_numeric'),  ##PIC 999
                ('TOL',148,4,'pic_numeric'),  ##PIC 9999
                ('SPAC',152,8,'pic_numeric'),  ##PIC 9(8)
                ('DIAG',160,4,'pic_numeric'),  ##PIC 9999
                ('CUM-PROD',164,7,'pic_comp'),  ##PIC S9(13) COMP-3
                ('CASING',171,21,'pic_any'),  ##PIC X(21)
                ('COL-HEAD',192,1,'pic_any'),  ##PIC X
                ('ALO-CODE',193,1,'pic_any'),  ##PIC X
                ('F-RMK1',194,66,'pic_any'),  ##PIC X(66)
                ('F-RMK2',260,66,'pic_any'),  ##PIC X(66)
                ('PERM-NO',326,5,'pic_any'),  ##PIC X(5)
                ('SP-FHC',331,1,'pic_numeric'),  ##PIC 9
                ('AN-A',332,90,'pic_any'),  ##PIC X(90)
                ('AN-B',422,35,'pic_any'),  ##PIC X(35)
                ('F-OOIP',457,8,'pic_numeric'),  ##PIC 9(08) ##('FILLER',465,7,'pic_numeric'),  ##PIC 9(07) ##('FILLER',472,15,'pic_numeric'),  ##PIC 9(15) ##('FILLER',487,13,'pic_numeric'),  ##PIC 9(13) 
                ('FM-DATE',500,6,'pic_yyyymm'),  ##PIC 9(6)
                ('FM-PW',506,2,'pic_comp'),  ##PIC S9(3) COMP-3
                ('FM-AC',508,4_4,'pic_comp'),  ##PIC S999V9(4) COMP-3 ##('FILLER',512,4,'pic_numeric'),  ##PIC 9(4)
                ('FM-OTHC',516,1,'pic_numeric'),  ##PIC 9
                ('FM-CHG',517,1,'pic_numeric'),  ##PIC 9
                ('FM-PROD-FACT',518,3_3,'pic_comp'),  ##PIC S99V999 COMP-3
                ('FM-SPLIT-PROD-FACT',521,3_3,'pic_comp'),  ##PIC S99V999 COMP-3
                ('FM-JOHN',524,1,'pic_numeric'),  ##PIC 9
                ('FM-OTH',525,8_7,'pic_comp'),  ##PIC S9(8)V9(7) COMP-3 ##('FILLER',533,15,'pic_any'),  ##PIC X(15)
               ]

OIL_LEASE_03 = [
                ('LEASE-REC-TYPE-REC',0,1,'pic_numeric'),  ##PIC 9
                ('LEASE-REC-DIST',1,3,'pic_any'),  ##PIC XXX
                ('LEASE-REC-FIELD',4,8,'pic_numeric'),  ##PIC 9(8)
                ('LEASE-REC-OPR',12,6,'pic_numeric'),  ##PIC 9(6)
                ('LEASE-REC-LEASE',18,5,'pic_numeric'),  ##PIC 9(5)
                ('LEASE-REC-FILLER',23,2,'pic_any'),  ##PIC XX
                ('LEASE-REC-OFFSHORE',25,1,'pic_numeric'),  ##PIC 9
                ('L-NAME',26,32,'pic_any'),  ##PIC X(32)
                ('LSE-CO',58,6,'pic_numeric'),  ##PIC 9(6)
                ('POGATH',64,5,'pic_any'),  ##PIC X(5)
                ('PGGATH',69,5,'pic_any'),  ##PIC X(5)
                ('OSPLIT',74,1,'pic_numeric'),  ##PIC 9
                ('GSPLIT',75,1,'pic_numeric'),  ##PIC 9
                ('OOGATH',76,5,'pic_any'),  ##PIC X(5)
                ('OGGATH',81,5,'pic_any'),  ##PIC X(5)
                ('OOPR',86,6,'pic_numeric'),  ##PIC 9(6)
                ('BO-STATUS',92,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('BG-STATUS',96,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('MOVE-BAL',100,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('PO-STATUS',104,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('PG-STATUS',108,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('SEC-REC',112,1,'pic_numeric'),  ##PIC 9
                ('CERT',113,2,'pic_numeric'),  ##PIC 99
                ('BATCH',115,1,'pic_any'),  ##PIC X
                ('L-LPB',116,1,'pic_numeric'),  ##PIC 9
                ('COMMINGLE-CD',117,1,'pic_numeric'),  ##PIC 9
                ('COMMINGLE',118,4,'pic_numeric'),  ##PIC 9999
                ('L-INFO',122,54,'pic_any'),  ##PIC X(54)
                ('AD-BO-STATUS',176,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('AD-BG-STATUS',180,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('COMMINGLE-DATE',184,6,'pic_yyyymm'),  ##PIC 9(6)
                ('L-RMCD',190,1,'pic_numeric'),  ##PIC 9
                ('L-RMDT',191,6,'pic_yyyymm'),  ##PIC 9(6)
                ('SEV-CD-13',197,1,'pic_numeric'),  ##PIC 9
                ('SEV-CD-14',198,1,'pic_numeric'),  ##PIC 9
                ('L-CAS-SI-LTR-DTE',199,6,'pic_yyyymm'),  ##PIC 9(6)
                ('L-RED-RTE-DTE',205,6,'pic_yyyymm'),  ##PIC 9(6)
                ('L-EXC-TST',211,1,'pic_numeric'),  ##PIC 9
                ('L-RLTYCD',212,1,'pic_numeric'),  ##PIC 9
                ('L-ONE-WELL-LEASE',213,1,'pic_any'),  ##PIC X
                ('L-PANHANDLE-GOR-EXC',214,1,'pic_any'),  ##PIC X(01)
                ('L-PANHANDLE-GOR-AMT',215,5_1,'pic_comp'),  ##PIC 9(08)V9 COMP-3 ##('FILLER',220,4,'pic_numeric'),  ##PIC 9(04)
                ('L-MONTH-DATE',224,6,'pic_yyyymm'),  ##PIC 9(6)
                ('LM-SEV',230,1,'pic_numeric'),  ##PIC 9
                ('LM-RETRO',231,1,'pic_numeric'),  ##PIC 9
                ('LM-REC',232,1,'pic_numeric'),  ##PIC 9
                ('LM-CHG',233,1,'pic_numeric'),  ##PIC 9
                ('LM-ALLOW',234,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('LM-PROD',238,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('LM-FW',242,3,'pic_numeric'),  ##PIC 999
                ('LM-OW',245,3,'pic_numeric'),  ##PIC 999
                ('LM-PL',248,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('LM-PLC',252,1,'pic_numeric'),  ##PIC 9
                ('LM-OTH',253,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('LM-OTHC',257,1,'pic_numeric'),  ##PIC 9
                ('LM-STO',258,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('LM-GL',262,5,'pic_comp'),  ##PIC S9(7) COMP-3
                ('LM-GPROD',267,5,'pic_comp'),  ##PIC S9(7) COMP-3
                ('LM-GLIFT',272,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('LM-CSIL',276,1,'pic_numeric'),  ##PIC 9
                ('LM-JOHN',277,1,'pic_numeric'),  ##PIC 9
                ('LM-LTR-CODE',278,1,'pic_numeric'),  ##PIC 9 ##('FILLER',279,13,'pic_numeric'),  ##PIC 9(13) ##('FILLER',292,904,'pic_numeric'),  ##PIC 9(13) ##('FILLER',1196,4,'pic_numeric')  ##PIC 9(04) 
               ]

OIL_MULTI_WELL_04 = [
                ('MULTI-W-REC-TYPE-REC',0,1,'pic_numeric'),  ##PIC 9
                ('MULTI-W-REC-DIST',1,3,'pic_any'),  ##PIC XXX
                ('MUTLI-W-REC-FIELD',4,8,'pic_numeric'),  ##PIC 9(8)
                ('MULTI-W-REC-OPR',12,6,'pic_numeric'),  ##PIC 9(6)
                ('MULTI-W-REC-LEASE',18,5,'pic_numeric'),  ##PIC 9(5)
                ('MULTI-W-REC-FILLER',23,2,'pic_numeric'),  ##PIC 99
                ('MULTI-W-REC-OFFSHORE',25,1,'pic_numeric'),  ##PIC 9
                ('M-RECORD',26,6,'pic_any'),  ##PIC X(6)
                ('TYPEW',32,1,'pic_any'),  ##PIC X
                ('RESER',33,5,'pic_any'),  ##PIC X(5)
                ('M-COUNTY',38,6,'pic_numeric'),  ##PIC 9(6)
                ('M-TST-EFF',44,1,'pic_any'),  ##PIC X
                ('M-PNTR-1ST',45,6,'pic_numeric'),  ##PIC 9(6)
                ('CAP',51,1,'pic_numeric'),  ##PIC 9
                ('PROD-WELL',52,6,'pic_numeric'),  ##PIC 9(6)
                ('MARG-WELL',58,6,'pic_numeric'),  ##PIC 9(6)
                ('M-DEPTH',64,1,'pic_numeric'),  ##PIC 9
                ('M-PNTR-LST',65,6,'pic_numeric'),  ##PIC 9(6)
                ('M-EXC-TEST',71,1,'pic_numeric'),  ##PIC 9 ##('FILLER',72,6,'pic_numeric'),  ##PIC 9(6)
                ('M-WATER',78,6,'pic_numeric'),  ##PIC 9(6)
                ('M-REMARK',84,55,'pic_any'),  ##PIC X(55)
                ('MM-PRCNT',139,3,'pic_comp'),  ##PIC V999  ##('FILLER',142,11,'pic_numeric'),  ##PIC 9(11) ##('FILLER',153,11,'pic_numeric'),  ##PIC 9(11)
                ('M-MONTH-DATE',164,6,'pic_yyyymm'),  ##PIC 9(6)
                ('MM-CHG',170,1,'pic_numeric'),  ##PIC 9
                ('MM-NO',171,1,'pic_numeric'),  ##PIC 9
                ('MM-ALLOW',172,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('MM-ACODE',176,1,'pic_numeric'),  ##PIC 9
                ('MM-TCODE',177,1,'pic_numeric'),  ##PIC 9
                ('MM-LIMIT',178,5,'pic_comp'),  ##PIC S9(9) COMP-3
                ('MM-ALLOW2',183,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('MM-ACODE2',187,1,'pic_numeric'),  ##PIC 9
                ('MM-TCODE2',188,1,'pic_numeric'),  ##PIC 9
                ('MM-LIMIT2',189,5,'pic_comp'),  ##PIC S9(9) COMP-3
                ('MM-DATE2',194,2,'pic_numeric'),  ##PIC 99
                ('MM-ALLOW3',196,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('MM-ACODE3',200,1,'pic_numeric'),  ##PIC 9
                ('MM-TCODE3',201,1,'pic_numeric'),  ##PIC 9
                ('MM-LIMIT3',202,5,'pic_comp'),  ##PIC S9(9) COMP-3
                ('MM-DATE3',207,2,'pic_numeric'),  ##PIC 99
                ('MM-FORM-LCK',209,1,'pic_numeric'),  ##PIC 9
                ('MM-SPACE1',210,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('MM-KODE2',214,1,'pic_numeric'),  ##PIC 9
                ('MM-SPACE2',215,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('MM-JOHN',219,1,'pic_numeric'),  ##PIC 9 ##('FILLER',220,9,'pic_numeric'),  ##PIC 9(09) ##('FILLER',229,9,'pic_numeric'),  ##PIC 9(09)
               ]

OIL_WELL_05 = [
                ('WELL-REC-TYPE-REC',0,1,'pic_numeric'),  ##PIC 9
                ('WELL-REC-DIST',1,3,'pic_any'),  ##PIC XXX
                ('WELL-REC-FIELD',4,8,'pic_numeric'),  ##PIC 9(8)
                ('WELL-REC-OPR',12,6,'pic_numeric'),  ##PIC 9(6)
                ('WELL-REC-LEASE',18,5,'pic_numeric'),  ##PIC 9(5)
                ('WELL-REC-FILLER',23,2,'pic_numeric'),  ##PIC 99
                ('WELL-REC-OFFSHORE',25,1,'pic_numeric'),  ##PIC 9
                ('WELL-NO',26,6,'pic_any'),  ##PIC X(6)
                ('W-TYPE-WELL',32,1,'pic_any'),  ##PIC X(1)
                ('W-UNIT-NO',33,1,'pic_any'),  ##PIC X
                ('W-UNIT-VALUE',34,4,'pic_numeric'),  ##PIC 9V999
                ('W-KEY',38,1,'pic_numeric'),  ##PIC 9
                ('W-COUNTY',39,3,'pic_numeric'),  ##PIC 999
                ('PUMP',42,1,'pic_numeric'),  ##PIC 9
                ('W-SP',43,5,'pic_numeric'),  ##PIC 9(5)
                ('W-NET',48,6,'pic_numeric'),  ##PIC 9(6)
                ('W-DEPTH',54,5,'pic_numeric'),  ##PIC 9(5)
                ('SAND',59,3,'pic_numeric'),  ##PIC 9(3)
                ('FROZEN',62,5,'pic_numeric'),  ##PIC 9(5)
                ('PERF',67,5,'pic_numeric'),  ##PIC 9(5)
                ('W-DATE',72,8,'pic_yyyymmdd'),  ##PIC 9(8)
                ('EX-14B-CD',80,1,'pic_any'),  ##PIC X
                ('W-SUB-WELL',81,1,'pic_numeric'),  ##PIC 9
                ('W-NO-PROD-CD',82,1,'pic_numeric'),  ##PIC 9
                ('W-DELQ-FORM',83,1,'pic_numeric'),  ##PIC 9
                ('W-TST-EFF',84,1,'pic_any'),  ##PIC X
                ('W-EXC-TST',85,1,'pic_numeric'),  ##PIC 9
                ('W-WATER',86,4,'pic_numeric'),  ##PIC 9(4)
                ('EX-14B-DATE',90,6,'pic_yyyymm'),  ##PIC 9(6)
                ('W-RMKS',96,15,'pic_any'),  ##PIC X(15)
                ('BONUS-AMT',111,4,'pic_numeric'),  ##PIC 9(4)
                ('FROZTSF',115,3,'pic_numeric'),  ##PIC 999
                ('W-WLSD',118,1,'pic_numeric'),  ##PIC 9
                ('W-TST-DT',119,8,'pic_yyyymmdd'),  ##PIC 9(8)
                ('W-DTE-LST-UTL',127,6,'pic_yyyymm'),  ##PIC 9(6)
                ('W-NEW-WB-EXC',133,1,'pic_any'),  ##PIC X(01)
                ('W-NEW-WB-CONNECT-DATE',134,8,'pic_yyyymmdd'),  ##PIC 9(8)
                ('W-14B2-TYPE-COVERAGE',142,1,'pic_any'),  ##PIC X(01)
                ('W-14B2-APP-NO',143,6,'pic_numeric'),  ##PIC 9(06) ##('FILLER',149,4,'pic_numeric'),  ##PIC 9(04) ##('FILLER',153,18,'pic_numeric'),  ##PIC 9(18) ##('FILLER',171,7,'pic_numeric'),  ##PIC 9(07)
                ('W-MONTH-DATE',178,6,'pic_yyyymm'),  ##PIC 9(6)
                ('WM-CHG',184,1,'pic_numeric'),  ##PIC 9
                ('WM-NO',185,1,'pic_numeric'),  ##PIC 9
                ('WM-ALLOW',186,3,'pic_comp'),  ##PIC S9(5) COMP-3
                ('WM-ACODE',189,1,'pic_any'),  ##PIC X
                ('WM-TCODE',190,1,'pic_any'),  ##PIC X
                ('WM-LIMIT',191,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('WM-ALLOW2',195,3,'pic_comp'),  ##PIC S9(5) COMP-3
                ('WM-ACODE2',198,1,'pic_any'),  ##PIC X
                ('WM-TCODE2',199,1,'pic_any'),  ##PIC X
                ('WM-LIMIT2',200,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('WM-DATE2',204,2,'pic_numeric'),  ##PIC 99
                ('WM-ALLOW3',206,3,'pic_comp'),  ##PIC S9(5) COMP-3
                ('WM-ACODE3',209,1,'pic_any'),  ##PIC X
                ('WM-TCODE3',210,1,'pic_any'),  ##PIC X
                ('WM-LIMIT3',211,4,'pic_comp'),  ##PIC S9(7) COMP-3
                ('WM-DATE3',215,2,'pic_numeric'),  ##PIC 99
                ('WM-FORM-LICK',217,1,'pic_numeric'),  ##PIC 9
                ('WM-PGT',218,2,'pic_comp'),  ##PIC S999 COMP-3
                ('WM-TSWA',220,1,'pic_numeric'),  ##PIC 9
                ('WM-EGT',221,2,'pic_comp'),  ##PIC S999 COMP-3
                ('WM-ESWA',223,1,'pic_numeric'),  ##PIC 9
                ('WM-ACRE',224,3_2,'pic_comp'),  ##PIC S999V99 COMP-3
                ('WM-POTE',227,3_2,'pic_comp'),  ##PIC S9999V9 COMP-3
                ('WM-ACFT',230,3,'pic_comp'),  ##PIC S9(5) COMP-3
                ('WM-GOR',233,3,'pic_comp'),  ##PIC S9(5) COMP-3
                ('WM-OTRAN-CD',236,1,'pic_numeric'),  ##PIC 9
                ('WM-POT',237,2,'pic_comp'),  ##PIC S999 COMP-3
                ('WM-EOT',239,2,'pic_comp'),  ##PIC S999 COMP-3
                ('WM-JOHN',241,1,'pic_numeric'),  ##PIC 9
                ('WM-OOIP',242,6,'pic_numeric'),  ##PIC 9(06) ##('FILLER',248,3,'pic_numeric'),  ##PIC 9(03)
               ]

def oilProd_layout(startval):
    layouts_map = {
                    '1' : {'name': 'OIL_FIELD', 'layout': OIL_FIELD_01},
                    '3' : {'name': 'OIL_LEASE', 'layout': OIL_LEASE_03},
                    '4' : {'name': 'OIL_MULTI_WELL', 'layout': OIL_MULTI_WELL_04},
                    '5' : {'name': 'OIL_WELL', 'layout': OIL_WELL_05},
                  }
    
    if startval in layouts_map.keys():
        returnval = layouts_map[startval]
    else:
        returnval = None
    
    return returnval
