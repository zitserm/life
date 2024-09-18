# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 18:54:45 2024

@author: Misha Zitser
"""

import duckdb
from pathlib import Path

DATA_DIR = Path(r"C:\Users\Misha Zitser\life\data\globi")

class Interactions(object):
    def __init__(self, sources=['iNaturalist'], is_local=True, **kwargs):
        self.sources = sources
        if is_local:
            self.src_path = Path(DATA_DIR) / 'interactions.csv'
        else:
            self.src_path = kwargs.get('path', 'https://zenodo.org/record/11552565/files/interactions.csv.gz')
            
    def make_source_dbs(self):
        """
        Make a separate duckdb database for each source in self.sources

        Returns
        -------
        None.

        """
        for src in self.sources:
            path = Path(DATA_DIR) / f"{src.lower()}.db"
            print(f'Connecting to {path}')
            con = duckdb.connect(str(path))
            print(f'Created {path}')
            cmd = f"CREATE TABLE interactions AS select * from read_csv('{str(self.src_path)}') where sourceInstitutionCode='{src}'"
            con.execute(cmd)
            print(cmd)
            con.close()
            # how do you release the lock on the database?