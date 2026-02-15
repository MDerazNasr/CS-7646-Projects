""""""

"""
A Decision Tree Learner.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---
"""

import numpy as np


class DTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None

    def author(self):
        return "mnasr34"

    def study_group(self):
        return "mnasr34"

    def add_evidence(self, data_x, data_y):
        self.tree = self._build_tree(data_x, data_y)
        if self.verbose:
            print("Tree shape:", self.tree.shape)

    def _build_tree(self, data_x, data_y):
        # if all y values are the same, make a leaf
        if np.all(data_y == data_y[0]):
            return np.array([[-1, data_y[0], np.nan, np.nan]])

        # if number of samples <= leaf_size, make a leaf
        if data_x.shape[0] <= self.leaf_size:
            return np.array([[-1, np.mean(data_y), np.nan, np.nan]])

        # find best feature to split on using correlation
        best_feature = self._get_best_feature(data_x, data_y)

        split_val = np.median(data_x[:, best_feature])

        # if all values in the best feature are the same, make a leaf
        if np.all(data_x[:, best_feature] <= split_val):
            return np.array([[-1, np.mean(data_y), np.nan, np.nan]])

        left_mask = data_x[:, best_feature] <= split_val
        right_mask = ~left_mask

        left_tree = self._build_tree(data_x[left_mask], data_y[left_mask])
        right_tree = self._build_tree(data_x[right_mask], data_y[right_mask])

        root = np.array([[best_feature, split_val, 1, left_tree.shape[0] + 1]])
        return np.vstack((root, left_tree, right_tree))

    def _get_best_feature(self, data_x, data_y):
        num_features = data_x.shape[1]
        correlations = np.zeros(num_features)
        for i in range(num_features):
            # skip features with zero std dev
            if np.std(data_x[:, i]) == 0:
                correlations[i] = 0.0
            else:
                correlations[i] = abs(np.corrcoef(data_x[:, i], data_y)[0, 1])
        return np.argmax(correlations)

    def query(self, points):
        predictions = np.zeros(points.shape[0])
        for i in range(points.shape[0]):
            predictions[i] = self._traverse_tree(points[i])
        return predictions

    def _traverse_tree(self, point):
        node = 0
        while True:
            feature = int(self.tree[node, 0])
            if feature == -1:
                return self.tree[node, 1]
            split_val = self.tree[node, 1]
            if point[feature] <= split_val:
                node = node + int(self.tree[node, 2])
            else:
                node = node + int(self.tree[node, 3])


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
