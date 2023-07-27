# TXRRC_data_harvest

## Data Source
Download files from: https://www.rrc.texas.gov/resource-center/research/data-sets-available-for-download/

* `WorkingFileFor_dbf900.py` references the "Full Wellbore" EBCDIC file named `dbf900.ebc` (which is shared as both a `.gz` and an uncompressed file).

## Changes
* 2021-03-03 - TXRCC have redesigned the website and the locations of the datafiles. We are working to make sure the connections are correct. The file formats look to not be affected at this time.

## About 

TXRRC_data_harvest is a set of tools for downloading and organizing oil and gas well data from the [Texas Railroad Commission](https://www.rrc.texas.gov).

This project is currently in an alpha development stage. It is definitely a work in progress and will take a bit to get fully organized and usable, so please bear with us. 

## Contributing

We are always happy for any help: pull requests, bug reports, feature requests are all appreciated.

## Project goals
The goal is to provide scripts to help download and organize the oil and gas well data provided publicly from the Texas Railroad Commission (TXRRC).


## Getting started

If you are unfamiliar with python, using the notebooks with an .ipynb reader like Jupyter Notebook is a good place to start and test:<br>
https://github.com/mlbelobraydi/TXRRC_data_harvest/tree/master/Notebooks

<br>
The current development is happening in the working files:<br>
Well info: https://github.com/mlbelobraydi/TXRRC_data_harvest/blob/master/WorkingFileFor_dbf900.py <br>
Oil Prod: https://github.com/mlbelobraydi/TXRRC_data_harvest/blob/master/WorkingFileFor_oilProd.py <br>
Gas Prod: Coming soon!

## Install

### Install with conda

Coming soon!

### Install with a virtualenv and pip 

```bash
# Make a workspace directory or cd to your favorite workspace directory
mkdir workspace

# Make a python virtualenv for the TXRRC_data_harvest
python -m venv venv-txrrc

# Start the virtualenv
source venv-txrrc/bin/activate

# Clone this repository
# Here we are cloning the home repo, but if you wish to contribute fork the
# repo on GitHub and clone your fork
git clone https://github.com/mlbelobraydi/TXRRC_data_harvest.git

# Cd into the repository
cd TXRRC_data_harvest

# Install the requried packages in the virtualenv.
pip -r requirements.txt

# get a data file to work with
mkdir data
cd data
wget ftp://ftpe.rrc.texas.gov/shfwba/dbf900.ebc.gz
gunzip dbf900.ebc.gz
cd ..

# do a sample run
mkdir output
python WorkingFileFor_dbf900.py --filepath data/dbf900.ebc --outdir outdir
...
# look in outdir for the processed files!
```


## TXRRC Data Source

https://github.com/mlbelobraydi/TXRRC_data_harvest/wiki/TXRRC-Data-Source-Reference

## Other Similar Projects

If this code isn't what you are looking for, here is a list of other TXRRC projects on github.

https://github.com/mlbelobraydi/TXRRC_data_harvest/wiki/Similar-projects
