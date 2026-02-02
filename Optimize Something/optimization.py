""""""  		  	   		 		  			  		 			     			  	 
"""MC1-P2: Optimize a portfolio.  		  	   		 		  			  		 			     			  	 
  		  	   		 		  			  		 			     			  	 
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
  		  	   		 		  			  		 			     			  	 
  		  	   		 		  			  		 			     			  	 
import datetime as dt
import os
import sys

# Add parent directory to path to find util.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from scipy.optimize import minimize

import matplotlib.pyplot as plt
import pandas as pd
from util import get_data, plot_data
  		  	   		 		  			  		 			     			  	 
  		  	   		 		  			  		 			     			  	 
# This is the function that will be tested by the autograder  		  	   		 		  			  		 			     			  	 
# The student must update this code to properly implement the functionality  		  	   		 		  			  		 			     			  	 
def optimize_portfolio(  		  	   		 		  			  		 			     			  	 
    sd=dt.datetime(2008, 1, 1),  		  	   		 		  			  		 			     			  	 
    ed=dt.datetime(2009, 1, 1),  		  	   		 		  			  		 			     			  	 
    syms=["GOOG", "AAPL", "GLD", "XOM"],  		  	   		 		  			  		 			     			  	 
    gen_plot=False,  		  	   		 		  			  		 			     			  	 
):  		  	   		 		  			  		 			     			  	 
    """  		  	   		 		  			  		 			     			  	 
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe  		  	   		 		  			  		 			     			  	 
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of  		  	   		 		  			  		 			     			  	 
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take  		  	   		 		  			  		 			     			  	 
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and  		  	   		 		  			  		 			     			  	 
    statistics.  		  	   		 		  			  		 			     			  	 
  		  	   		 		  			  		 			     			  	 
    :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		 		  			  		 			     			  	 
    :type sd: datetime  		  	   		 		  			  		 			     			  	 
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		 		  			  		 			     			  	 
    :type ed: datetime  		  	   		 		  			  		 			     			  	 
    :param syms: A list of symbols that make up the portfolio (note that your code should support any  		  	   		 		  			  		 			     			  	 
        symbol in the data directory)  		  	   		 		  			  		 			     			  	 
    :type syms: list  		  	   		 		  			  		 			     			  	 
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your  		  	   		 		  			  		 			     			  	 
        code with gen_plot = False.  		  	   		 		  			  		 			     			  	 
    :type gen_plot: bool  		  	   		 		  			  		 			     			  	 
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,  		  	   		 		  			  		 			     			  	 
        standard deviation of daily returns, and Sharpe ratio  		  	   		 		  			  		 			     			  	 
    :rtype: tuple  		  	   		 		  			  		 			     			  	 
    """  		  	   		 		  			  		 			     			  	 
  		  	   		 		  			  		 			     			  	 
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

    # Data cleansing: fill forward then backward to handle missing values
    prices = prices.ffill().bfill()
    prices_SPY = prices_SPY.ffill().bfill()

    # Normalize prices to start at 1.0
    normed = prices / prices.iloc[0]
    
    # Calculate daily returns
    daily_returns = (prices / prices.shift(1)) - 1
    daily_returns = daily_returns.iloc[1:]  # Remove first row (NaN)
    
    # Number of assets
    n = len(syms)
    
    # Initial guess: uniform allocation
    initial_guess = np.ones(n) / n
    
    # Risk-free rate per day
    risk_free_rate = 0.0
    
    # Trading days per year
    trading_days = 252
    
    def negative_sharpe(allocs):
        """Calculate negative Sharpe ratio for minimization"""
        # Normalize allocations to sum to 1
        allocs = allocs / np.sum(allocs)
        
        # Calculate portfolio daily returns
        port_daily_returns = (daily_returns * allocs).sum(axis=1)
        
        # Calculate statistics
        avg_daily_return = port_daily_returns.mean()
        std_daily_return = port_daily_returns.std(ddof=1)  # Sample standard deviation
        
        # Avoid division by zero
        if std_daily_return == 0:
            return 1e6
        
        # Sharpe ratio (annualized)
        sharpe_ratio = np.sqrt(trading_days) * (avg_daily_return - risk_free_rate) / std_daily_return
        
        # Return negative for minimization
        return -sharpe_ratio
    
    # Constraints: sum of allocations = 1.0
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0})
    
    # Bounds: each allocation between 0.0 and 1.0 (long positions only)
    bounds = tuple((0.0, 1.0) for _ in range(n))
    
    # Optimize
    result = minimize(negative_sharpe, initial_guess, method='SLSQP', 
                     bounds=bounds, constraints=constraints)
    
    # Get optimal allocations (normalized to sum to 1)
    allocs = result.x / np.sum(result.x)
    allocs = np.asarray(allocs)
    
    # Calculate portfolio value using optimal allocations
    alloced = normed * allocs
    port_val = alloced.sum(axis=1)
    
    # Calculate portfolio daily returns
    port_daily_returns = (daily_returns * allocs).sum(axis=1)
    
    # Calculate statistics
    adr = port_daily_returns.mean()
    sddr = port_daily_returns.std(ddof=1)  # Sample standard deviation
    
    # Cumulative return (portfolio value starts at 1.0)
    cr = port_val.iloc[-1] - 1.0
    
    # Sharpe ratio (annualized)
    if sddr == 0:
        sr = 0.0
    else:
        sr = np.sqrt(trading_days) * (adr - risk_free_rate) / sddr

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # Normalize SPY to start at 1.0
        normed_SPY = prices_SPY / prices_SPY.iloc[0]
        
        # Normalize portfolio to start at 1.0
        normed_port = port_val / port_val.iloc[0]
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.plot(normed_port.index, normed_port.values, label='Portfolio', linewidth=2)
        plt.plot(normed_SPY.index, normed_SPY.values, label='SPY', linewidth=2)
        plt.xlabel('Date')
        plt.ylabel('Normalized Price')
        plt.title('Daily Portfolio Value vs SPY')
        plt.legend(loc='best')
        plt.grid(True)
        plt.savefig('Figure1.png', bbox_inches='tight')
        plt.close()

    return allocs, cr, adr, sddr, sr


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "mnasr34"


def study_group():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "mnasr34"


def test_code():
    """  		  	   		 		  			  		 			     			  	 
    This function WILL NOT be called by the auto grader.  		  	   		 		  			  		 			     			  	 
    """  		  	   		 		  			  		 			     			  	 
  		  	   		 		  			  		 			     			  	 
    start_date = dt.datetime(2009, 1, 1)  		  	   		 		  			  		 			     			  	 
    end_date = dt.datetime(2010, 1, 1)  		  	   		 		  			  		 			     			  	 
    symbols = ["GOOG", "AAPL", "GLD", "XOM", "IBM"]  		  	   		 		  			  		 			     			  	 
  		  	   		 		  			  		 			     			  	 
    # Assess the portfolio  		  	   		 		  			  		 			     			  	 
    allocations, cr, adr, sddr, sr = optimize_portfolio(  		  	   		 		  			  		 			     			  	 
        sd=start_date, ed=end_date, syms=symbols, gen_plot=False  		  	   		 		  			  		 			     			  	 
    )  		  	   		 		  			  		 			     			  	 
  		  	   		 		  			  		 			     			  	 
    # Print statistics  		  	   		 		  			  		 			     			  	 
    print(f"Start Date: {start_date}")  		  	   		 		  			  		 			     			  	 
    print(f"End Date: {end_date}")  		  	   		 		  			  		 			     			  	 
    print(f"Symbols: {symbols}")  		  	   		 		  			  		 			     			  	 
    print(f"Allocations:{allocations}")  		  	   		 		  			  		 			     			  	 
    print(f"Sharpe Ratio: {sr}")  		  	   		 		  			  		 			     			  	 
    print(f"Volatility (stdev of daily returns): {sddr}")  		  	   		 		  			  		 			     			  	 
    print(f"Average Daily Return: {adr}")  		  	   		 		  			  		 			     			  	 
    print(f"Cumulative Return: {cr}")  		  	   		 		  			  		 			     			  	 
  		  	   		 		  			  		 			     			  	 
  		  	   		 		  			  		 			     			  	 
if __name__ == "__main__":  		  	   		 		  			  		 			     			  	 
    # This code WILL NOT be called by the auto grader  		  	   		 		  			  		 			     			  	 
    # Do not assume that it will be called  		  	   		 		  			  		 			     			  	 
    test_code()  		  	   		 		  			  		 			     			  	 
