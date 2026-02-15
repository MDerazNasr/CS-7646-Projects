""""""

"""
A Bag Learner (Bootstrap Aggregation).

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


class BagLearner(object):
    def __init__(self, learner, kwargs=None, bags=20, boost=False, verbose=False):
        if kwargs is None:
            kwargs = {}
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        self.learners = []
        for i in range(0, bags):
            self.learners.append(learner(**kwargs))

    def author(self):
        return "mnasr34"

    def study_group(self):
        return "mnasr34"

    def add_evidence(self, data_x, data_y):
        n = data_x.shape[0]
        for learner in self.learners:
            # sample with replacement
            indices = np.random.choice(n, size=n, replace=True)
            bag_x = data_x[indices]
            bag_y = data_y[indices]
            learner.add_evidence(bag_x, bag_y)

    def query(self, points):
        results = np.zeros((self.bags, points.shape[0]))
        for i, learner in enumerate(self.learners):
            results[i] = learner.query(points)
        return np.mean(results, axis=0)


if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
