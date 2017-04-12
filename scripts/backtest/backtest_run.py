#Level of Difference Between Prices
#dij,t= β(ri,t−rf) − (rj,t−rf) t ∈ T
#(Regression coefficient between returns) * (return_1 - RFR) - (return_2 - RFR)

from scripts.backtest.similarity_calculations import *
from scripts.utility import *
import json, sys

class BacktestModule():
    def __init__(self):
        pass

    def backtestModuleRun(self):
        self.getDistance()

    def getDistance(self):
        p("Finding distance measures for all stock pairs.")
        tickers = q("SELECT name FROM sqlite_master WHERE type = 'table';")

        used_tickers = {}
        dist = self.cfg['distanceMeasure']['distance_measure']
        i = 1
        tot = len(tickers)**2 - len(tickers)

        distances = {}
        for t1 in tickers:
            for t2 in tickers:
                pr("Distance Calculation Completion: " + str(round(i/tot,4)) + "%")
                i+=1
                if t1 == t2:
                    continue
                if t1 in used_tickers.keys():
                    if used_tickers[t1] == t2:
                        continue
                used_tickers[t1] = t2

                vec1 = q("SELECT %s FROM %s;" % (self.cfg['distanceMeasure']['distance_column'],t1))
                vec2 = q("SELECT %s FROM %s;" % (self.cfg['distanceMeasure']['distance_column'],t2))

                if len(vec1) != len(vec2):
                    continue

                if self.cfg['distanceMeasure']['use_rfr']:
                    vec1b = [i - float(self.cfg['distanceMeasure']['val_rfr']) for i in vec1]
                    vec2b = [i - float(self.cfg['distanceMeasure']['val_rfr']) for i in vec2]
                else:
                    vec1b = vec1
                    vec2b = vec2

                if dist == 'cosine':
                    d = cosineDistance(vec1b, vec2b)
                elif dist == 'regression':
                    d = regressionDistance(vec1b, vec2b)
                elif dist == 'euclidian':
                    d = euclidianDistance(vec1b, vec2b)
                elif dist == 'manhattan':
                    d = manhattanDistance(vec1b, vec2b)

                distances[t1 + "|" + t2] = d

                print(distances)