#!/usr/bin/env python

from GRDataFrameManager import GRDataFrameManager
import numpy as np
from scipy import sparse


class GRSparseMatrixGenerator:

    def __init__(self,path_to_dataset='data', use_test_tags=False):
        self._dfBuilder = GRDataFrameManager()

        self.programmers, self.repositories, self.prog_dict, self.repo_dict = self._dfBuilder.getContributionsRepositories()
        self.prog_dict = self._dfBuilder.getProgDict()
        self.tag_dict = self._dfBuilder.getTagDict()


    def getCOORepositoryProgrammer(self):
        self.incidence_rows = np.zeros(len(self.programmers))
        self.incidence_cols = np.zeros(len(self.programmers))
        self.incidence = np.ones(len(self.programmers))

        # set_trace()

        for i in range(0, len(self.programmers)):
            self.incidence_cols[i] = self.prog_dict[self.programmers[i]]
            self.incidence_rows[i] = self.repo_dict[self.repositories[i]]

        mtx = sparse.coo_matrix((self.incidence, (self.incidence_rows,self.incidence_cols)))
        # temp = mtx.todense()
        print("Number of Repositories: ", mtx.shape[0])
        print("Number of Developers: ", mtx.shape[1])
        print("Sparsity: ", mtx.getnnz()/(mtx.shape[0]*mtx.shape[1]))
        return mtx

    def getCOORepositoryTags(self):
        idx, tag_counts = self._dfBuilder.getRepositoryTags()
        rows = np.zeros(len(idx))
        cols = np.zeros(len(idx))
        data = np.zeros(len(idx))

        for i in range(0, len(idx)):
            rows[i] = self.repo_dict[idx[i][0]]
            cols[i] = self.tag_dict[idx[i][1]]
            data[i] = tag_counts[i]

        mtx = sparse.coo_matrix((data, (rows,cols)))

        return mtx

    def getCOOProgrammerTags(self):
        idx, tag_counts = self._dfBuilder.getProgrammerTags()
        rows = np.zeros(len(idx))
        cols = np.zeros(len(idx))
        data = np.zeros(len(idx))

        for i in range(0, len(idx)):
            rows[i] = self.prog_dict[idx[i][1]]
            cols[i] = self.tag_dict[idx[i][0]]
            data[i] = tag_counts[i]

        mtx = sparse.coo_matrix((data, (rows,cols)))

        return mtx


    def getProgrammersNotInRepo(self, repo_id):
        programmers = []
        for i in range(0, len(self.programmers)):
            if self.repo_dict[self.repositories[i]] != repo_id:
                prog = self.prog_dict[self.programmers[i]]
                if prog not in programmers:
                    programmers.append(prog)

        return programmers


    def getProgrammerFromID(self,id):
        return list(self.prog_dict.keys())[list(self.prog_dict.values()).index(id)]

    def getTagFromId(self, id):
        return list(self.tag_dict.keys())[list(self.tag_dict.values()).index(id)]
