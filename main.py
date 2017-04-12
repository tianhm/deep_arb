import argparse, datetime
from configparser import ConfigParser

from scripts.downloader.downloader_run import *
from scripts.backtest.backtest_run import *

class statArb(DownloaderModule,BacktestModule):
    def __init__(self,fetchTickers,useDownloaderModule,useBacktestModule,useAllModules):
        self.pwd = os.path.join(os.path.abspath(os.path.dirname(__file__))) + "/"
        self.cfg = ConfigParser()
        self.cfg.read(self.pwd + "cfg/cfg.ini")

        self.fetchTickers = fetchTickers

        self.useDownloaderModule = useDownloaderModule
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

        DownloaderModule.__init__(self)
        BacktestModule.__init__(self)

    def statArbRun(self):
        if self.useDownloaderModule or self.useAllModules:
            self.downloaderModuleRun()
        if self.useBacktestModule or self.useAllModules:
            self.backtestModuleRun()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    all_group = parser.add_mutually_exclusive_group()
    all_group.add_argument("-a",help="Use all modules.",action="store_true")

    other_group = parser.add_mutually_exclusive_group()
    other_group.add_argument("-d",help="Use downloader module.",action="store_true")
    other_group.add_argument("-b",help="Use backtester module",action="store_true")

    fetch_group = parser.add_mutually_exclusive_group()
    fetch_group.add_argument("-f", help="Fetch fresh tickers.", action="store_true")

    args = parser.parse_args()

    sa = statArb(args.f, args.d, args.b, args.a)
    sa.statArbRun()