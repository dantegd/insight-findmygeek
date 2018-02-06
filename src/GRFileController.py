#!/usr/bin/env python

import os
from glob import glob
import pandas as pd
from pdb import set_trace

class GRFileController:

    def __init__(self, path_to_dataset='data', file_format='parquet', precalculated=False):
        if not precalculated:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            self._data_path = dir_path[:-3] + path_to_dataset + '/*/'
            self._folder_paths = list(glob(self._data_path))

            self._repo_names = []
            self.file_format = 'parquet'

            for folder in self._folder_paths:
                self._repo_names.append(folder)

            for folder in self._folder_paths:
                self._commit_files.append(folder + 'commits.' + self.file_format)
                self._patches_files.append(folder + 'patches.' + self.file_format)

            self.files_loaded = False

        else:
            self.normalized_df = pd.read_csv('data/normalized_df.csv')
            self.files_loaded = Truedrive


    def readFiles(self):
        self.readCommitFiles()
        self.readPatchFiles()
        self.readTagFiles()



    def readCommitFiles(self):
        print("Loading commit files into memory...")
        if self.file_format == 'parquet':
            commit_df_from_each_file = (pd.read_parquet(f) for f in self._commit_files)
        else:
            commit_df_from_each_file = (pd.read_csv(f) for f in self._commit_files)
        self.df_commits = pd.concat(commit_df_from_each_file, ignore_index=True)


    def readPatchFiles(self):
        print("Loading patch files into memory...")
        self.df_patches = []
        current = 0
        for filename in self._patches_files:
            self.df_patches.append(pd.read_parquet(filename))
            self.df_patches[current].insert(0,'repository',self._repository_names[current])
            current += 1
        self.filesLoaded = True

    def readTagFiles(self):
        print("Loading repository tag files into memory...")
        self.df_tags = (pd.read_csv(f) for f in self._commit_files)


    def lastocc(self, somestr, char):
        return max(i for i,c in enumerate(somestr) if c==char)

    def get_repo_name_from_path(self, path):
        return path[self.lastocc(self._folder_paths[0][:-1], '/')+1:-1]




if __name__ == '__main__':
    fil = GRFileController()
    set_trace()
