from scripts.utility import *

from finsymbols import symbols
import pandas as pd, yahoo_finance, sys, json


class SymbolDownloader:
    def __init__(self):
        self.sectors = {}

    def getSymbols(self):
        idxs = self.cfg["general"]["idxs"].split(",")
        symbols_list = []
        sectors_map = {}

        if "sp500" in idxs:
            symbols_list += symbols.get_sp500_symbols()
        if "nyse" in idxs:
            symbols_list += symbols.get_nyse_symbols()
        if "nasdaq" in idxs:
            symbols_list += symbols.get_nasdaq_symbols()
        if "amex" in idxs:
            symbols_list += symbols.get_amex_symbols()

        for s in symbols_list:
            sectors_map[s["symbol"]] = s["sector"]

        with open(self.pwd + "cfg/tickers.json","w") as f:
            json.dump(sectors_map, f)

class PriceDownloader():
    def __init__(self, tickers, cfg):

        self.tickers = tickers
        self.cfg = cfg
        self.prices = []

        self.startDay = self.cfg["database"]["start_day"]
        self.startMonth = self.cfg["database"]["start_mon"]
        self.startYear = self.cfg["database"]["start_yr"]

        self.endDay = self.cfg["database"]["end_day"]
        self.endMonth = self.cfg["database"]["end_mon"]
        self.endYear = self.cfg["database"]["end_yr"]

    def run(self):
        p("Downloader launched.")

        outlist = {}
        i = 1
        tot = len(self.tickers)
        for t in self.tickers:
            try:
                tmp = self.queryYahooFinance(t)
                outlist[t] = tmp

            except Exception as e:
                p("Unable to download data for " + t + ".")
                p("Full Exception: " + str(e))
            pr("\rDownload Completion: " + str(round(i/tot*100,4)) + "%")

            i+=1
        print("\n")
        p("Download complete.")
        return outlist


    def queryYahooFinance(self,ticker):
        startDate = self.startYear + "-" + self.startMonth + "-" + self.startDay
        endDate = self.endYear + "-" + self.endMonth + "-" + self.endDay

        for x in range(int(self.cfg["yfinance"]["yfattempts"])):
            try:
                symbol = yahoo_finance.Share(ticker)
                dat = symbol.get_historical(startDate, endDate)

                df = pd.DataFrame(dat)
                break
            except:
                pass
        return df
