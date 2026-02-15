""""""

"""
Test a learner.  (c) 2015 Tucker Balch

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

import math
import sys
import time

import matplotlib
import numpy as np

matplotlib.use("Agg")
import BagLearner as bl
import DTLearner as dt
import LinRegLearner as lrl
import matplotlib.pyplot as plt
import RTLearner as rt

np.random.seed(903574027)


def load_data(filename):
    inf = open(filename)
    lines = inf.readlines()
    inf.close()
    # skip header if present, skip date column (first col) for Istanbul
    data_lines = []
    for s in lines:
        s = s.strip()
        if s == "":
            continue
        parts = s.split(",")
        try:
            row = list(map(float, parts))
            data_lines.append(row)
        except ValueError:
            # try skipping first column (date column)
            try:
                row = list(map(float, parts[1:]))
                data_lines.append(row)
            except ValueError:
                continue
    data = np.array(data_lines)
    return data


def get_rmse(pred_y, actual_y):
    return math.sqrt(((actual_y - pred_y) ** 2).sum() / actual_y.shape[0])


def experiment1(train_x, train_y, test_x, test_y):
    # Experiment 1: Overfitting with DTLearner as leaf_size varies
    max_leaf = 100
    in_sample_rmse = np.zeros(max_leaf)
    out_sample_rmse = np.zeros(max_leaf)

    for leaf_size in range(1, max_leaf + 1):
        learner = dt.DTLearner(leaf_size=leaf_size, verbose=False)
        learner.add_evidence(train_x, train_y)

        pred_train = learner.query(train_x)
        in_sample_rmse[leaf_size - 1] = get_rmse(pred_train, train_y)

        pred_test = learner.query(test_x)
        out_sample_rmse[leaf_size - 1] = get_rmse(pred_test, test_y)

    leaf_sizes = np.arange(1, max_leaf + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(leaf_sizes, in_sample_rmse, label="In-sample RMSE")
    plt.plot(leaf_sizes, out_sample_rmse, label="Out-of-sample RMSE")
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.title("Experiment 1: DTLearner Overfitting Analysis")
    plt.legend()
    plt.grid(True)
    plt.savefig("experiment1.png")
    plt.close()


def experiment2(train_x, train_y, test_x, test_y):
    # Experiment 2: Effect of bagging on overfitting with DTLearner
    max_leaf = 100
    num_bags = 20

    in_sample_rmse_bag = np.zeros(max_leaf)
    out_sample_rmse_bag = np.zeros(max_leaf)
    in_sample_rmse_nobag = np.zeros(max_leaf)
    out_sample_rmse_nobag = np.zeros(max_leaf)

    for leaf_size in range(1, max_leaf + 1):
        # without bagging (single DTLearner)
        learner_nobag = dt.DTLearner(leaf_size=leaf_size, verbose=False)
        learner_nobag.add_evidence(train_x, train_y)
        pred_train = learner_nobag.query(train_x)
        in_sample_rmse_nobag[leaf_size - 1] = get_rmse(pred_train, train_y)
        pred_test = learner_nobag.query(test_x)
        out_sample_rmse_nobag[leaf_size - 1] = get_rmse(pred_test, test_y)

        # with bagging
        learner_bag = bl.BagLearner(
            learner=dt.DTLearner,
            kwargs={"leaf_size": leaf_size},
            bags=num_bags,
            boost=False,
            verbose=False,
        )
        learner_bag.add_evidence(train_x, train_y)
        pred_train = learner_bag.query(train_x)
        in_sample_rmse_bag[leaf_size - 1] = get_rmse(pred_train, train_y)
        pred_test = learner_bag.query(test_x)
        out_sample_rmse_bag[leaf_size - 1] = get_rmse(pred_test, test_y)

    leaf_sizes = np.arange(1, max_leaf + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(leaf_sizes, in_sample_rmse_nobag, label="No Bag - In-sample RMSE")
    plt.plot(leaf_sizes, out_sample_rmse_nobag, label="No Bag - Out-of-sample RMSE")
    plt.plot(leaf_sizes, in_sample_rmse_bag, label="Bag (20) - In-sample RMSE")
    plt.plot(leaf_sizes, out_sample_rmse_bag, label="Bag (20) - Out-of-sample RMSE")
    plt.xlabel("Leaf Size")
    plt.ylabel("RMSE")
    plt.title("Experiment 2: Effect of Bagging on DTLearner Overfitting")
    plt.legend()
    plt.grid(True)
    plt.savefig("experiment2.png")
    plt.close()


def experiment3(train_x, train_y, test_x, test_y):
    # Experiment 3: Compare DTLearner vs RTLearner
    # Metric 1: Mean Absolute Error (MAE)
    # Metric 2: R-squared (Coefficient of Determination)
    max_leaf = 100

    dt_mae = np.zeros(max_leaf)
    rt_mae = np.zeros(max_leaf)
    dt_r2 = np.zeros(max_leaf)
    rt_r2 = np.zeros(max_leaf)

    for leaf_size in range(1, max_leaf + 1):
        # DTLearner
        dt_learner = dt.DTLearner(leaf_size=leaf_size, verbose=False)
        dt_learner.add_evidence(train_x, train_y)
        dt_pred = dt_learner.query(test_x)

        # RTLearner
        rt_learner = rt.RTLearner(leaf_size=leaf_size, verbose=False)
        rt_learner.add_evidence(train_x, train_y)
        rt_pred = rt_learner.query(test_x)

        # MAE
        dt_mae[leaf_size - 1] = np.mean(np.abs(test_y - dt_pred))
        rt_mae[leaf_size - 1] = np.mean(np.abs(test_y - rt_pred))

        # R-squared
        ss_res_dt = np.sum((test_y - dt_pred) ** 2)
        ss_res_rt = np.sum((test_y - rt_pred) ** 2)
        ss_tot = np.sum((test_y - np.mean(test_y)) ** 2)
        dt_r2[leaf_size - 1] = 1 - (ss_res_dt / ss_tot)
        rt_r2[leaf_size - 1] = 1 - (ss_res_rt / ss_tot)

    leaf_sizes = np.arange(1, max_leaf + 1)

    # Chart 1: MAE comparison
    plt.figure(figsize=(10, 6))
    plt.plot(leaf_sizes, dt_mae, label="DTLearner MAE")
    plt.plot(leaf_sizes, rt_mae, label="RTLearner MAE")
    plt.xlabel("Leaf Size")
    plt.ylabel("Mean Absolute Error")
    plt.title("Experiment 3: DTLearner vs RTLearner - MAE Comparison")
    plt.legend()
    plt.grid(True)
    plt.savefig("experiment3_mae.png")
    plt.close()

    # Chart 2: R-squared comparison
    plt.figure(figsize=(10, 6))
    plt.plot(leaf_sizes, dt_r2, label="DTLearner R-squared")
    plt.plot(leaf_sizes, rt_r2, label="RTLearner R-squared")
    plt.xlabel("Leaf Size")
    plt.ylabel("R-squared")
    plt.title("Experiment 3: DTLearner vs RTLearner - R-squared Comparison")
    plt.legend()
    plt.grid(True)
    plt.savefig("experiment3_r2.png")
    plt.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python testlearner.py <filename>")
        sys.exit(1)

    data = load_data(sys.argv[1])

    # randomly shuffle the data
    np.random.shuffle(data)

    # compute how much of the data is training and testing
    train_rows = int(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    train_x = data[:train_rows, 0:-1]
    train_y = data[:train_rows, -1]
    test_x = data[train_rows:, 0:-1]
    test_y = data[train_rows:, -1]

    print(f"Training data: {train_x.shape}")
    print(f"Testing data: {test_x.shape}")

    # run all experiments
    print("Running Experiment 1...")
    experiment1(train_x, train_y, test_x, test_y)
    print("Experiment 1 complete. Chart saved as experiment1.png")

    print("Running Experiment 2...")
    experiment2(train_x, train_y, test_x, test_y)
    print("Experiment 2 complete. Chart saved as experiment2.png")

    print("Running Experiment 3...")
    experiment3(train_x, train_y, test_x, test_y)
    print(
        "Experiment 3 complete. Charts saved as experiment3_mae.png and experiment3_r2.png"
    )

    print("All experiments complete.")
