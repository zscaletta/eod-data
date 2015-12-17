__author__ = 'Zach'

import os
import sys
import csv
import ast
import shutil
import urllib.request, urllib.parse, urllib.error
import pandas as pd

class EOData:




    def get_eod_csv(self,dir='',exchs=[]):
        if dir:
            if not os.path.exists(dir):
                    os.makedirs(dir)
        exch_list = ['AMEX','NYSE','Nasdaq','SCAP']

        if exchs:
            print('...exchanges specified: {0}'.format(exchs))
            for item in exchs:
                path = 'http://online.wsj.com/public/resources/documents/{0}.csv'.format(item)
                print(path)
                filename = os.path.join(dir,'{0}_EOD.csv'.format(item))
                if not os.path.exists(filename):
                    try:
                        urllib.request.urlretrieve(path, filename)
                        print('...downloaded successfully')
                    except:
                        print('unable to download...')
        else:
            print('...downloading data from all exch!')
            for item in exch_list:
                path = 'http://online.wsj.com/public/resources/documents/{0}.csv'.format(item)
                print(path)
                filename = os.path.join(dir,'{0}_EOD.csv'.format(item))
                if not os.path.exists(filename):
                    try:
                        urllib.request.urlretrieve(path, filename)
                        print('...downloaded successfully')
                    except:
                        print('unable to download...')

    def get_all_eod(self,keep_csv=False):
        # returns unindexed df containing combination of raw eod csv data files from each exch

        self.get_eod_csv(dir='temp')
        dfs = []
        print('... reading files')
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
            shutil.rmtree('temp',ignore_errors=True)
        df = pd.concat(dfs)
        #df.reset_index(inplace=True)
        df.columns = ['Name','Symbol','Open','High','Low','Close','Net Chg','pCentChg','Volume','52WkHigh','52WkLow','Div','Yield','P/E','YTDpCentChg','Exchange']
        df = df.sort(columns='Symbol',kind='quicksort')
        #df.set_index(['Symbol'])
        return df

    def from_cmd(self):
        # simply filters get_all_eod df for fields specified below:
        fields=['Symbol','Close']
        # or in commandline argument 'fields=[list of fieldnames]'
        exch_data = self.get_all_eod()
        argd = self.parse_args()
        if argd[2].lower() == 'all':
            ftr = exch_data
        elif argd[2] != str(argd[2]):
            fields = argd[2]
            ftr = exch_data[fields]
        else:
            ftr = exch_data[fields]
        # this implementation is somewhat esoteric to the commandline branch
        print(ftr.head())
        print(argd)
        fpath = argd[0]
        if os.path.exists(fpath):
            os.remove(fpath)

        if '.csv' in fpath:

            if argd[1] == True:
                print('made it this far')
                ftr.to_csv(fpath,index= False,header= True)
            else:
                ftr.to_csv(fpath,index= False,header= False)
        else:
            if argd[1] == True:
                print('made it this far')
                ftr.to_csv(fpath,index= False,header= True,sep= ' ',mode= 'a')
            else:
                ftr.to_csv(fpath,index= False,header= False,sep= ' ',mode= 'a')


    def skip_header(self,seq, n):
    # supporting func for 'get_all_eod'
        for i,item in enumerate(seq):
            if i >= n:
                yield item


    def parse_args(self):
        # supporting func for EOData.from_cmd
        # parses cmd line arguments for ease of use with automation/bat files
        pth = ''
        fname='exch_data.txt'
        newfpath = ''
        header=False
        listofcols = []
        if len(sys.argv) > 1:
            for item in sys.argv:
                if 'fname=' in item:
                    t = item.split('fname=')
                    fname = t[1]
                    print('fname specified: {0}'.format(fname))
                if 'dest_folder=' in item:
                    t = item.split('dest_folder=')
                    pth = t[1]
                    print('path specified: {0}'.format(pth))

                if 'dest_path=' in item:
                    t = item.split('dest_path=')
                    newfpath = t[1]

                if 'headers=' in item:
                    t = item.split('headers=')
                    if t[1].lower() == 'true':
                        header = True
                    else:
                        header = False

                if 'fields=' in item:
                    t = item.split('fields=')
                    if t[1] == str(t[1]):
                        listofcols=t[1]
                    else:
                        listofcols = ast.literal_eval(t[1])


        full_path = os.path.join(pth,fname)
        if newfpath:
            full_path=newfpath
        print('saving to path: {0}'.format(full_path))

        argd = [full_path,header,listofcols]
        return argd