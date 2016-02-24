http://conda.pydata.org/miniconda.html
author: zach scaletta

Prereqs:
python >3
pandas


eod-cmd is a commandline accessible version of the EOData class that allows the user to download customs slices of the end of day
data provided in csv format @ http://online.wsj.com/public/resources/documents/stocksdaily.htm

with the prerequisites and necessary environment variables enabled, the script can be called from the command line or bat file
after navigating to the working directory and executing:

	python eod-exch.py

the script simply initiates an instance of EOData and calls the method EOData.from_cmd()

>>>	exch_data = EOData()
>>>	exch_data.from_cmd()


This will handle command line arguments, create a temp folder, download all exch data, parse for specified fields, then return a space
delimited text file (or csv if specified)sorted alphabetically.

by default this will create a list of all stock symbols and their cooresponding closing prices.
there are multiple optional arguments accessible from the command line which enable automated slicing. the arguments are listed
below:

'fname='
		python eod-cmd.py fname=myfilename.txt

	used to specify desired filename for output file (can be .txt or technically .csv)
	can be used in combination with arg 'dest_folder' if desired.

'dest_folder='
		python eod-cmd.py dest_folder=C:\Users\Public

	used to specify folder, unless 'fname' specified, will use default filename 'exch_data.txt'

'dest_path='
		python eod-cmd.py dest_path=C:\Users\Public\myfilename.txt

	can be used to replace dest_folder or fname, allows user specified filepath
'headers='
		python eod-cmd.py headers=True
	
	boolean option allowing user to specify whether column headers should be included in output file, default is false

'fields='
		python eod-cmd.py fields=['Symbol','Close']

	fields argument takes bracketed list [] of quoted strings ""(or '') indicating which columns to include in output file.
	available columns are:

		['Name','Symbol','Open','High','Low','Close','Net Chg','pCentChg','Volume','52WkHigh','52WkLow','Div','Yield','P/E','YTDpCentChg']

	or, if one would like to download all data, the string 'all' may be passed as such:

		python eod-cmd.py fields=all


Examples:

	if one simply wanted to download end of day closing data with no headers:

		python eod-cmd.py

	to download all available data with headers:

		python eod-cmd.py fields=all headers=True

	if one wanted only the symbol, close price, and volume data -including headers, written to the filename "symb_close_vol.txt":

		python eod-cmd.py fields=['Symbol','Close','Volume'] fname=symb_close_vol.txt

	.csv can also be used in any of these applications by simply specifying .csv using either the fname argument:

		python eod-cmd.py fields=all headers=True fname=mycsvfile.csv

	or using dest_path
		
		python eod-cmd.py fields=all headers=True dest_path=C:\Users\Public\mycsvfile.csv

