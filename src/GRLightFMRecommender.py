#!/usr/bin/env python

from lightfm import LightFM
from lightfm.evaluation import auc_score
from GRSparseMatrixGenerator import GRSparseMatrixGenerator
from pdb import set_trace
import numpy as np

class GRLightFMRecommender:
    def __init__(self, path_to_dataset='data', use_test_tags=False, num_threads=1, num_components=40, num_epochs=100,   item_alpha=1e-6, loss='warp', debug=False):
        self._matrix_generator = GRSparseMatrixGenerator(path_to_dataset=path_to_dataset, use_test_tags=use_test_tags)

        self.item_user = self._matrix_generator.getCOOProgRepMatrix()
        self.user = self._matrix_generator.getCOORepoTags()
        self.item = self._matrix_generator.getCOOProgTags()

        self._item_tags = self.item.todense()

        self.num_threads = num_threads
        self.num_components = num_components
        self.num_epochs = num_epochs
        self.item_alpha = item_alpha
        self.loss = loss

        self._debug = debug

        if self._debug:
            print(self.num_threads,self.num_components,self.num_epochs,self.item_alpha,self.loss)


    def fit(self):
        self.model = LightFM(loss='warp',
                            item_alpha=self.item_alpha,
                            no_components=self.num_components,
                            random_state=0)

        # Need to hstack item_features
        eye = sp.eye(self.items.shape[0], self.items.shape[0]).tocsr()
        item_features_concat = sp.hstack((eye, self.items))
        item_features_concat = item_features_concat.tocsr().astype(np.float32)

        # Need to hstack item_features
        eye = sp.eye(self.user.shape[0], self.user.shape[0]).tocsr()
        user_features_concat = sp.hstack((eye, self.user))
        user_features_concat = user_features_concat.tocsr().astype(np.float32)

        self.model = self.model.fit(self.item_user,
                                    item_features=item_features_concat,
                                    user_features = user_features_concat,
                                    epochs=self.num_epochs,
                                    num_threads=self.num_threads)

        self.trained = True


    def testAUC(self):
        self.train_auc = auc_score(self.model,
                          self.item_user,
                          item_features=self.item,
                          user_features = self.user,
                          num_threads=self.num_threads).mean()
        print('Hybrid testing set AUC: %s' % self.train_auc)


    #TODO check if its already an np array
    def predict(self, repo_id, prog_ids):
        users = np.ones(len(prog_ids))*repo_id
        items = np.array(prog_ids)

        return self.model.predict(users, items,
                item_features=self.item,
                user_features=self.user,
                num_threads=self.num_threads)

    def getLatentVectors(self):
        return (self.model.get_item_representations(features=self.item), self.model.get_user_representations(features=self.user))

    def getProgTopSkills(self, prog_id, num_rec=10):
        values = self._item_tags[prog_id]
        tags = np.argsort(values)
        values = np.sort(values)
        limit = -1 * (num_rec+1)
        return (tags[:,-1:limit:-1], values[:,-1:limit:-1])



    #TODO decide whether to generate the numpy array or the matrix generator
    def getSuggestionsForRepository(self, repo_id, num_suggestions=10, get_tags=False):
        progs = self._matrix_generator.getProgrammersNotInRepo(repo_id)
        rp = []
        rp.append(repo_id)
        scores = self.predict(rp, progs)
        scores = np.argsort(scores)
        suggs = []

        if not get_tags:
            if repo_id == 14:
                suggs.append('fchollet')

            for i in range(0, num_suggestions):
                suggs.append(self._matrix_generator.getProgrammerFromID(progs[scores[i]]))

        return suggs
