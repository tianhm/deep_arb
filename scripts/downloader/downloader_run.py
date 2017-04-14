import os
from datetime import datetime

from scripts.downloader.databaseMgr import *
from scripts.downloader.downloader import *

class DownloaderModule(SymbolDownloader, DatabaseMgr):
    def __init__(self):
        SymbolDownloader.__init__(self)
        DatabaseMgr.__init__(self)

    def downloaderModuleRun(self):
        if self.fetchTickers:
            p("Fetching stock tickers from internet.")
            self.getSymbols()
        with open(self.pwd + "cfg/tickers.json","r") as f:
            self.sectors = json.load(f)

        p("Checking SQL for stock data.")
        for t in list(self.sectors.keys()):
            self.checkSQL(t)
        p("Finished checking SQL for stock data.")


        dl = PriceDownloader(list(self.missing_data),self.cfg)
        self.prices = dl.run()
        #check content of self.prices

        p("Inserting missing data into SQL.")
        for t in list(self.missing_data):
            self.insertSQL(t)
        p("Done inserting missing data into SQL.")