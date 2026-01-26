""""""

"""Assess a betting strategy.

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

Student Name: Mohamed Deraz Nasr
GT User ID: mnasr34
GT ID: 904206985
"""

import matplotlib.pyplot as plt
import numpy as np


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "mnasr34"


def gtid():
    """
    :return: The GT ID of the student
    :rtype: int
    """
    return 904206985


def study_group():
    """
    :return: A comma separated string of GT_Name of each member of your study group
    :rtype: str
    """
    return "mnasr34"


def get_spin_result(win_prob):
    """
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.

    :param win_prob: The probability of winning
    :type win_prob: float
    :return: The result of the spin.
    :rtype: bool
    """
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result


def simulate_episode(win_prob, limited_bankroll=False):
    """
    Simulates one episode of the martingale strategy
    """
    winnings = np.zeros(1001)  # 0 to 1000 spins
    episode_winnings = 0
    bankroll = 256
    spin = 0

    while spin < 1000:
        # stop if we hit $80
        if episode_winnings >= 80:
            winnings[spin:] = episode_winnings
            return winnings

        # stop if we lost all money (only for limited bankroll)
        if limited_bankroll and episode_winnings <= -256:
            winnings[spin:] = -256
            return winnings

        bet = 1
        won = False

        while not won:
            if spin >= 1000:
                break

            # check win condition
            if episode_winnings >= 80:
                winnings[spin:] = episode_winnings
                return winnings

            # check if bankrupt
            if limited_bankroll and episode_winnings <= -256:
                winnings[spin:] = -256
                return winnings

            # if we dont have enough money, bet what we have left
            if limited_bankroll:
                money_left = 256 + episode_winnings
                if bet > money_left:
                    bet = money_left

            won = get_spin_result(win_prob)
            spin += 1

            if won:
                episode_winnings = episode_winnings + bet
            else:
                episode_winnings = episode_winnings - bet
                bet = bet * 2

            winnings[spin] = episode_winnings

    return winnings


def test_code():
    """
    Method to test your code
    """
    # 18 black slots out of 38 total on american roulette
    win_prob = 18 / 38

    np.random.seed(gtid())  # set seed once

    # ============ EXPERIMENT 1 ============

    # Figure 1 - run 10 episodes
    plt.figure()
    for i in range(10):
        episode = simulate_episode(win_prob, limited_bankroll=False)
        plt.plot(episode, label="Episode " + str(i + 1))
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel("Spin")
    plt.ylabel("Winnings")
    plt.title("Figure 1: 10 Episodes (Unlimited Bankroll)")
    plt.legend()
    plt.savefig("figure1.png")
    plt.close()

    # run 1000 episodes for figures 2 and 3
    results = np.zeros((1000, 1001))
    for i in range(1000):
        results[i] = simulate_episode(win_prob, limited_bankroll=False)

    # Figure 2 - mean and std
    mean = np.mean(results, axis=0)
    std = np.std(results, axis=0)

    plt.figure()
    plt.plot(mean, label="Mean")
    plt.plot(mean + std, label="Mean + Std")
    plt.plot(mean - std, label="Mean - Std")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel("Spin")
    plt.ylabel("Winnings")
    plt.title("Figure 2: Mean (Unlimited Bankroll)")
    plt.legend()
    plt.savefig("figure2.png")
    plt.close()

    # Figure 3 - median and std
    median = np.median(results, axis=0)

    plt.figure()
    plt.plot(median, label="Median")
    plt.plot(median + std, label="Median + Std")
    plt.plot(median - std, label="Median - Std")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel("Spin")
    plt.ylabel("Winnings")
    plt.title("Figure 3: Median (Unlimited Bankroll)")
    plt.legend()
    plt.savefig("figure3.png")
    plt.close()

    # print stats for experiment 1
    final = results[:, -1]
    winners = np.sum(final >= 80)
    print("Experiment 1:")
    print("  Prob of winning $80:", winners / 1000)
    print("  Expected value:", np.mean(final))

    # ============ EXPERIMENT 2 ============

    # run 1000 episodes with limited bankroll
    results2 = np.zeros((1000, 1001))
    for i in range(1000):
        results2[i] = simulate_episode(win_prob, limited_bankroll=True)

    # Figure 4 - mean and std
    mean2 = np.mean(results2, axis=0)
    std2 = np.std(results2, axis=0)

    plt.figure()
    plt.plot(mean2, label="Mean")
    plt.plot(mean2 + std2, label="Mean + Std")
    plt.plot(mean2 - std2, label="Mean - Std")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel("Spin")
    plt.ylabel("Winnings")
    plt.title("Figure 4: Mean ($256 Bankroll)")
    plt.legend()
    plt.savefig("figure4.png")
    plt.close()

    # Figure 5 - median and std
    median2 = np.median(results2, axis=0)

    plt.figure()
    plt.plot(median2, label="Median")
    plt.plot(median2 + std2, label="Median + Std")
    plt.plot(median2 - std2, label="Median - Std")
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel("Spin")
    plt.ylabel("Winnings")
    plt.title("Figure 5: Median ($256 Bankroll)")
    plt.legend()
    plt.savefig("figure5.png")
    plt.close()

    # print stats for experiment 2
    final2 = results2[:, -1]
    winners2 = np.sum(final2 >= 80)
    print("Experiment 2:")
    print("  Prob of winning $80:", winners2 / 1000)
    print("  Expected value:", np.mean(final2))


if __name__ == "__main__":
    test_code()
