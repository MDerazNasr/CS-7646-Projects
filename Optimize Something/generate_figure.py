"""Script to generate Figure1.png for the optimization project report."""

import datetime as dt
from optimization import optimize_portfolio

if __name__ == "__main__":
    # Parameters for Figure 1 as specified in the assignment
    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ['IBM', 'X', 'GLD', 'JPM']
    
    print("Generating Figure1.png...")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Symbols: {symbols}")
    print()
    
    # Call optimize_portfolio with gen_plot=True to generate the chart
    allocs, cr, adr, sddr, sr = optimize_portfolio(
        sd=start_date,
        ed=end_date,
        syms=symbols,
        gen_plot=True
    )
    
    print("Figure1.png generated successfully!")
    print()
    print("Portfolio Statistics:")
    print(f"  Allocations: {allocs}")
    print(f"  Cumulative Return: {cr:.4f}")
    print(f"  Average Daily Return: {adr:.6f}")
    print(f"  Standard Deviation of Daily Returns: {sddr:.6f}")
    print(f"  Sharpe Ratio: {sr:.4f}")
