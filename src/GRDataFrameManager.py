#!/usr/bin/env python

from pdb import set_trace
from GRFileController import GRFileController


class GRDataFrameManager:

    def __init__(self, recommender='lightfm', use_precalculated=False, add_author_patches=True):
        self._file_manager = GRFileController(file_format='parquet')
        self._file_manager.readFiles()

        self.programmers = self._file_manager.df_commits.author_name.unique()

        self.languages = self._file_manager.df_patches.language.unique()

        self.tags =
        self._file_manager.df_tags.language.unique()


        self.getProgrammerMetadata(add_author_patches=True)



    def getProgrammerMetadata(self, add_author_patches=True):
        df_com_patch = []

        # add author to each patched file, necessary only if author is not included already in the patch files
        if add_author_patches:
            for df in self.df_patches:
                df_com_patch.append(pd.merge(self._file_manager.df_commits[['id','author_name']], df, on='id'))

            self.df_author_patches = pd.concat(df_com_patch, ignore_index=True)

        else:
            self.df_author_patches = self._file_manager.df_commits

        #calculate sum of contributions (sum of loc and count of files modified), dataframe is different for knn (surprise) and lightfm
        if self.recommender == "lightfm":
            self._df_author_patch_sum = self.df_author_patches.groupby(['language','author_name']).sum()
            self._df_author_patch_count = self.df_author_patches.groupby(['language','author_name']).count()


        if self.recommender == "surprise":
            self._df_author_patch_sum = self.df_author_patches.groupby(['repository','language','author_name']).sum()
            self._df_author_patch_count = self.df_author_patches.groupby(['repository','language','author_name']).count()



    def getProgToRepoContributions(self):
        #create programmer - repository contributions
        self.prog_cont = []
        self.repo_cont = []
        for df in self._file_manager.df_patches:
            for author in df.author_name.unique():
                self.prog_cont.append(author)
                self.repo_cont.append(df.iloc[0].repository)


    def _generateIDDicts(self):
        # Assign a unique position to each programmer and tag
        self._programmers_dict = {}
        self.tags_dict = {}
        self._repos_dict = {}

        #Create programmer dictionary
        for i in range(0, len(self.programmers)):
            self._programmers_dict[self.programmers[i]] = i

        #Create repo dictionary
        for i in range(0, len(self.languages)):
            self.tags_dict[self.languages[i]] = i

        # Create tag dictionary and add the computer languages
        for i in range(0, len(self._repository_names)):
            self._repos_dict[self._repository_names[i]] = i

        # Add the repo tags to the tag dictionary
        current = len(self.languages)
        for tag, topics in self._tags.items():
            for topic in topics:
                if topic not in self.tags_dict:
                    self.tags_dict[topic] = current
                    current += 1



    def getContributionsRepositories(self):
        return (self.prog_cont, self.repo_cont, self._programmers_dict, self._repos_dict)


    def getRepositoryTags(self):
        self._df_repo_patch_count = self.df_author_patches.groupby(['repository','language']).count()
        return (self._df_repo_patch_count.index, self._df_repo_patch_count.id.as_matrix())


    def getProgrammerTags(self):
        files_modified = self._df_author_patch_count.id.as_matrix()
        loc_modified = self._df_author_patch_sum.loc_d.as_matrix() + self._df_author_patch_sum.loc_i.as_matrix()

        return (self._df_author_patch_count.index, files_modified+loc_modified)
