# deep_arb
A statistical arbitrage trading implementation using daily data and deep learning predictive models.

## Development Status
Currently the ticker downloader, price downloader, and distance calculation modules are functional (albeit buggy).

The backtester and all subsequent modules are not yet functional.

## Quick Start
1. Please review the dependencies page before running.
2. To run the program, run main.py with one of the following command line arguments:  
  a. '-a' to run all modules (download data, calculate distances and backtest).  
  b. '-down' to run the downloader module (do not run with '-a').  
  c. '-dist' to run the distance calculation module (do not run with '-a').  
  d. '-back' to run the backtester module (do not run with '-a').  
  e. '-f' (only applicable when using '-a' or '-down' to download a new set of tickers).  
  
## Deleting Data
To delete all price data from the database, run 'delete_all_prices.py' without any command line arguments. This will delete all price tables from prices.db.  
  
Delete program for the distances db is a WIP.
  
## Config File
The config file (/cfg/cfg.ini) contains several values that can modify the backtester.
1. [general][idxs] tells the program which indexes to update tickers.json with. This finds just the tickers from the web, updates the json file, and then uses that json file to download actual prices.
2. [multithreading][threads] is for later implementations that will have multithreading.
3. [yfinance][yfattempts] tells the program how many times to attempt to download prices (for a given ticker) from yahoo finance before giving up.
4. [database][all] are the start dates and end dates of the download period. This instructs the program which dates to download data for.
5. [distanceMeasure][distance_column] tells the program which column of the prices.db tables to look at when calculating distance.
6. [distanceMeasure][distance_measure] tells the program which distance measure function to use to calculate distance between two stocks.
7. [distanceMeasure][distance_threshold_type] tells the program what measure to use to determine when a distance is abnormal.
8. [distanceMeasure][distance_threshold] is the value or zscore the program will use as the threshold in order to determine if a distance is abnormal.
9. [distanceMeasure][distance_observations] is the number of obsevations the program will use to calculate distance.
10. [distanceMeasure][use_rfr] allows the user to subtract a risk-free-rate from returns before calculating distance.
11. [distanceMeasure][val_rfr] is the risk free rate in use_rfr.
12. [model][train_ratio] is the proportion of data that will be used for training the model as opposed to testing.

## Tickers File
The tickers file (/cfg/tickers.json) contains all of the tickers that the program will download data for. This file is updated when you use a '-f' command line argument when running main.py. This file can also be manually maintained by the user.
