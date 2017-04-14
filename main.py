import argparse, datetime
from configparser import ConfigParser

from scripts.downloader.downloader_run import *
from scripts.backtest.backtest_run import *

from scripts.backtest.distanceCalculation.distance_run import *

class statArb(DownloaderModule,BacktestModule,DistanceModule):
    def __init__(self,fetchTickers,useDownloaderModule,useDistanceModule,useBacktestModule,useAllModules):
        self.pwd = os.path.join(os.path.abspath(os.path.dirname(__file__))) + "/"
        self.cfg = ConfigParser()
        self.cfg.read(self.pwd + "cfg/cfg.ini")

        self.fetchTickers = fetchTickers

        self.useDownloaderModule = useDownloaderModule
        self.useDistanceModule = useDistanceModule
        self.useBacktestModule = useBacktestModule
        self.useAllModules = useAllModules

        self.startDay = self.cfg["database"]["start_day"]
        self.startMonth = self.cfg["database"]["start_mon"]
        self.startYear = self.cfg["database"]["start_yr"]

        self.endDay = self.cfg["database"]["end_day"]
        self.endMonth = self.cfg["database"]["end_mon"]
        self.endYear = self.cfg["database"]["end_yr"]

        self.startDate = datetime.datetime.strptime(self.startDay + "-" + self.startMonth + "-" + self.startYear, "%d-%m-%Y")
        self.endDate = datetime.datetime.strptime(self.endDay + "-" + self.endMonth + "-" + self.endYear, "%d-%m-%Y")
        self.delta = self.endDate - self.startDate

        self.conn = sqlite3.connect("prices.db")
        self.cursor = self.conn.cursor()

        self.distances_conn = sqlite3.connect("distances.db")
        self.distances_cursor = self.distances_conn.cursor()

        DownloaderModule.__init__(self)
        BacktestModule.__init__(self)
        DistanceModule.__init__(self)

    def statArbRun(self):
        if self.useDownloaderModule or self.useAllModules:
            self.downloaderModuleRun()
        if self.useDistanceModule or self.useAllModules:
            self.getDistance()
        if self.useBacktestModule or self.useAllModules:
            self.backtestModuleRun()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-a",help="Use all modules.",action="store_true")
    parser.add_argument("-down",help="Use downloader module. Downloads price data for stocks (specified in 'tickers.json') and saves it to 'prices.db'.",action="store_true")
    parser.add_argument("-dist",help="Use distance calculation module. Calculates the distance for each pair of tickers and saves it to 'prices.db'.", action="store_true")
    parser.add_argument("-back",help="Use backtester module",action="store_true")
    parser.add_argument("-f", help="Fetch fresh tickers. Fetches new tickers from the internet (based on what index is specified in cfg.ini and saves them to ;tickers.json;.", action="store_true")

    args = parser.parse_args()

    args.a = True

    sa = statArb(args.f, args.down, args.dist, args.back, args.a)
    sa.statArbRun()