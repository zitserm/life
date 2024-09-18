# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 16:08:14 2024

@author: Misha Zitser
"""

import subprocess
import shlex
import pandas as pd
import os
import gzip
import shutil
from pathlib import Path

DATA_DIR = Path(r"C:\Users\Misha Zitser\life\data\inat")


data_downloader = None

def get_data_downloader():
    global data_downloader
    
    if data_downloader is None:
        data_downloader = DataDownloader()
    return data_downloader


class DataDownloader(object):
    ALL_FILES = ["observations", "observers", "photos", "taxa"]
    BASE_DIR = "s3://inaturalist-open-data"
    AWS = r'"C:\Program Files\Amazon\AWSCLIV2\aws.exe"'
    
    def download(self, files=None):
        """
        Download specified iNaturalist files from S3 to the local disk.

        Parameters
        ----------
        files : list or None 
            Specify one or more of: "observations", "observers", "photos", "taxa".
            If no file list is provided, all of the data will be downloaded
            as one giant zip file, which is about 17GB in size.

        Returns
        -------
        None.

        """
        
        if files is None:
            file_name = "inaturalist-open-data-latest.tar.gz"
            path = Path(DATA_DIR) / file_name
            commands = [ f"{self.AWS} s3 --no-sign-request cp {self.BASE_DIR}/metadata/{file_name} '{str(path)}'"] 
        else:
            commands = list()
            for file_type in files:
                path = Path(DATA_DIR) / f"{file_type}.csv.gz"
                cmd = f"{self.AWS} s3 --no-sign-request cp {self.BASE_DIR}/{file_type}.csv.gz '{str(path)}'"
                commands.append(cmd)
            
        for cmd in commands:
            args = shlex.split(cmd)
            # open a buffered connection
            with subprocess.Popen(args,stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, shell=True) as PROC:
            
                print(cmd)
                for line in PROC.stdout.readlines():
                    print(line.decode("utf-8"))
                
                for line in PROC.stderr.readlines():
                    print(line.decode("utf-8"))
                    

class DataManager(object):
    def __init__(self, file_type, zip_file):
        self.downloader = get_data_downloader()
        self.file_type = file_type
        self.zip_file = DATA_DIR / Path(zip_file)
        self.csv_file = DATA_DIR / Path(zip_file.rstrip(".gz"))
        self.df_impl = None
        
    def download(self, all_files=False):
        if not os.path.isfile(self.zip_file):
            if all_files:
                file_type = None
            else:
                file_type = self.file_type
            self.downloader.download([file_type])
        else:
            print(f'{self.zip_file} already exists.')
      
        if not os.path.isfile(self.csv_file):
            self.unzip_data()
        else:
            print(f'{self.cvs_file} already exists.')
        
    def unzip_data(self):
        with gzip.open(self.zip_file, 'rb') as IN:
            with open(self.csv_file, 'wb') as OUT:
                shutil.copyfileobj(IN, OUT)
    
    @property
    def df(self):
        if self.df_impl is None:
            self.df_impl = pd.read_csv(self.csv_file)
        return self.df_impl

class TaxonManager(DataManager):
    def __init__(self):
        super().__init__(file_type="taxa",
                         zip_file="taxa.csv.gz")

class ObservationManager(DataManager):
    def __init__(self):
        super().__init__(file_type="observations",
                         zip_file="observations.csv.gz")
        
class ObserverManager(DataManager):
    def __init__(self):
        super().__init__(file_type="observers",
                         zip_file="observers.csv.gz")
        
class PhotoManager(DataManager):
    def __init__(self):
        super().__init__(file_type="photos",
                         zip_file="photos.csv.gz")
















                
            
            
            