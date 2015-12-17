__author__ = 'Zach'

import os
import sys
import datetime
import csv
import ast
import shutil
import urllib.request, urllib.parse, urllib.error
import logging
import pandas as pd

logging.basicConfig(filename='eod_log_{0}.log'.format(datetime.date.today()),level=logging.DEBUG,format='%(asctime)s %(message)s')

class EOData:

    def get_eod_csv(self,dir='',exchs=[]):
        # downloads csv files to dir specified for exchs specified
        # default is all exchanges to local directory

        if dir:
            if not os.path.exists(dir):
                    os.makedirs(dir)

        exch_list = ['AMEX','NYSE','Nasdaq','SCAP']

        if exchs:
            for item in exchs:
                path = 'http://online.wsj.com/public/resources/documents/{0}.csv'.format(item)
                filename = os.path.join(dir,'{0}_EOD.csv'.format(item))
                if not os.path.exists(filename):
                    try:
                        urllib.request.urlretrieve(path, filename)
                        logging.info('{0}...downloaded successfully'.format(path))
                    except:
                        logging.warning('unable to download {0}...'.format(path))
        else:
            for item in exch_list:
                path = 'http://online.wsj.com/public/resources/documents/{0}.csv'.format(item)
                filename = os.path.join(dir,'{0}_EOD.csv'.format(item))
                if not os.path.exists(filename):
                    try:
                        urllib.request.urlretrieve(path, filename)
                        logging.info('{0}...downloaded successfully'.format(path))
                    except:
                        logging.warning('unable to download {0}...'.format(path))

    def get_all_eod(self,keep_csv=False):
        # returns unindexed df containing combination of raw eod csv data files from each exch

        self.get_eod_csv(dir='temp')
        dfs = []
        logging.info('... reading files')
        for i in os.listdir('temp'):
            if '.csv' in i:
                pt = os.path.join('temp',i)
                exchange = i.split('_EOD.csv')[0]
                new = []
                with open(pt, 'r') as total:
                    csvreader = csv.reader(total)
                    for row in self.skip_header(csvreader, 4):
                        new.append(row)
                df = pd.DataFrame(new,index=None)
                df['Exchange'] = exchange
                dfs.append(df)
        if keep_csv == False:
            logging.info('... cleaning up')
            shutil.rmtree('temp',ignore_errors=True)
        df = pd.concat(dfs)
        df.columns = ['Name','Symbol','Open','High','Low','Close','Net Chg','pCentChg','Volume','52WkHigh','52WkLow','Div','Yield','P/E','YTDpCentChg','Exchange']
        df = df.sort_values('Symbol',kind='quicksort')
        return df

    def from_cmd(self):


        # allows command-line access to some features of pandas slicing
        # default fields can be adjusted below, see readme for details
        fields=['Symbol','Close']

        exch_data = self.get_all_eod()
        argd = self.parse_args()
        if argd[2] == 'all':
            ftr = exch_data
        elif len(argd[2]) > 0:
            fields = ast.literal_eval(argd[2])
            ftr = exch_data[fields]
        else:
            ftr = exch_data[fields]

        logging.info('... length of df: {0}'.format(len(ftr)))
        fpath = argd[0]

        # lines below enable overwriting by default
        if os.path.exists(fpath):
            os.remove(fpath)

        if '.csv' in fpath:
            if argd[1] == True:
                ftr.to_csv(fpath,index= False,header= True)
            else:
                ftr.to_csv(fpath,index= False,header= False)
            logging.info('... complete {0}'.format(fpath))
        else:
            if argd[1] == True:
                ftr.to_csv(fpath,index= False,header= True,sep= ' ',mode= 'a')
            else:
                ftr.to_csv(fpath,index= False,header= False,sep= ' ',mode= 'a')
            logging.info('... complete {0}'.format(fpath))



    def skip_header(self,seq, n):
        # supporting func for EOData.get_all_eod
        for i,item in enumerate(seq):
            if i >= n:
                yield item

    def parse_args(self):
        # supporting func for EOData.from_cmd
        # parses cmd line arguments for ease of use with automation/bat files
        # defaults can be set in strings below - specifying dest_path will overwrite dest_folder and fname

        dest_folder = ''
        fname='exch_data.txt'
        dest_path = ''
        header=False
        listofcols = []
        if len(sys.argv) > 1:
            for item in sys.argv:
                if 'fname=' in item:
                    t = item.split('fname=')
                    fname = t[1]
                    logging.info('... filename specified: {0}'.format(fname))

                if 'dest_folder=' in item:
                    t = item.split('dest_folder=')
                    dest_folder = t[1]
                    logging.info('... destination folder specified: {0}'.format(dest_folder))

                if 'dest_path=' in item:
                    t = item.split('dest_path=')
                    dest_path = t[1]
                    logging.info('... destination filepath specified: {0}'.format(dest_path))

                if 'headers=' in item:
                    t = item.split('headers=')
                    if t[1].lower() == 'true':
                        header = True
                        logging.info('... headers enabled')
                    else:
                        header = False

                if 'fields=' in item:
                    t = item.split('fields=')
                    if t[1] == str(t[1]):
                        listofcols=t[1]
                        logging.info('... filtered for specified fields')
                    else:
                        listofcols = ast.literal_eval(t[1])
                        logging.info('... filtered for specified fields')

        full_path = os.path.join(dest_folder,fname)
        if dest_path:
            full_path=dest_path
        logging.info('... saving to path: {0}'.format(full_path))
        argd = [full_path,header,listofcols]

        return argd

exch_data = EOData()
exch_data.from_cmd()