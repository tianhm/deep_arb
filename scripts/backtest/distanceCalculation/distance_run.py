from scripts.backtest.distanceCalculation.similarity_calculations import *
from scripts.utility import *
import pandas as pd

class DistanceModule():
    def __init__(self):
        pass

    def getDistance(self):
        p("Finding distance measures for all stock pairs.")
        tickers = q("SELECT name FROM sqlite_master WHERE type = 'table';")

        used_tickers = {}

        dist = self.cfg['distanceMeasure']['distance_measure']
        i = 1
        tot = len(tickers) ** 2

        for t1 in tickers:
            for t2 in tickers:
                pr("Distance Calculation Completion: " + str(round(i / tot * 100, 4)) + "%")
                i += 1
                if t1 == "distances" or t2 == "distances":
                    continue
                if t1 == t2:
                    continue
                if t1 in used_tickers.keys():
                    if used_tickers[t1] == t2:
                        continue
                used_tickers[t1] = t2
                used_tickers[t2] = t1

                self.cursor.execute("SELECT * FROM %s;" % t1)
                test_res = self.cursor.fetchall()
                if test_res == []: continue

                self.cursor.execute("SELECT * FROM %s;" % t2)
                test_res = self.cursor.fetchall()
                if test_res == []: continue

                try:
                    vec1 = q("SELECT %s FROM %s;" % (self.cfg['distanceMeasure']['distance_column'], t1))
                    date1 = q("SELECT Date FROM %s;" % t1)
                except:
                    self.cursor.execute("SELECT * FROM %s;" % t1)
                    print("\n###########################################\n")
                    print("ERROR: EXCEPTION IN QUERYING VEC1 DATA IN getDistance().")
                    print("ERROR encountered when querying: " + t1)
                    print("DATA:")
                    print(self.cursor.fetchall())
                    sys.exit()
                try:
                    vec2 = q("SELECT %s FROM %s;" % (self.cfg['distanceMeasure']['distance_column'], t2))
                    date2 = q("SELECT Date FROM %s;" % t2)
                except:
                    self.cursor.execute("SELECT * FROM %s;" % t2)
                    print("\n###########################################\n")
                    print("ERROR: EXCEPTION IN QUERYING VEC1 DATA IN getDistance().")
                    print("ERROR encountered when querying: " + t2)
                    print("DATA:")
                    print(self.cursor.fetchall())
                    sys.exit()

                d1_list = []
                d2_list = []
                v1_list = []
                v2_list = []

                l = self.cfg['distanceMeasure']['distance_observations']
                for d1,d2,v1,v2 in zip (date1,date2,vec1,vec2):
                    d1_list.append(d1)
                    d2_list.append(d2)
                    v1_list.append(v1)
                    v2_list.append(v2)

                    if len(d1_list) >= int(l): del d1_list[0]
                    if len(d2_list) >= int(l): del d2_list[0]
                    if d1_list != d2_list: continue

                    if len(v1_list) >= int(l): del v1_list[0]
                    if len(v2_list) >= int(l): del v2_list[0]

                    if self.cfg['distanceMeasure']['use_rfr']:
                        vec1b = [i - float(self.cfg['distanceMeasure']['val_rfr']) for i in v1_list]
                        vec2b = [i - float(self.cfg['distanceMeasure']['val_rfr']) for i in v2_list]
                    else:
                        vec1b = v1_list
                        vec2b = v2_list

                    if dist == 'cosine':
                        d = cosineDistance(vec1b, vec2b)
                    elif dist == 'regression':
                        d = regressionDistance(vec1b, vec2b)
                    elif dist == 'euclidian':
                        d = euclidianDistance(vec1b, vec2b)
                    elif dist == 'manhattan':
                        d = manhattanDistance(vec1b, vec2b)

                    select_sql1 = "SELECT * FROM distances WHERE stock1 = '%s' AND stock2 = '%s' AND distance_type = '%s' AND start_date = '%s' AND observations = %s;" % (t1,t2,dist,d1_list[0],l)
                    self.distances_cursor.execute(select_sql1)
                    res1 = self.distances_cursor.fetchall()
                    select_sql2 = "SELECT * FROM distances WHERE stock1 = '%s' AND stock2 = '%s' AND distance_type = '%s' AND start_date = '%s' AND observations = %s;" % (t2,t1,dist,d1_list[0],l)
                    self.distances_cursor.execute(select_sql2)
                    res2 = self.distances_cursor.fetchall()

                    if res1 == [] and res2 == []:
                        insert_sql = "INSERT INTO distances (stock1,stock2,distance,distance_type,start_date,observations) VALUES ('%s','%s',%s,'%s','%s',%s)" % (t1,t2,d,dist,d1_list[0],l)
                        self.distances_cursor.execute(insert_sql)
                        self.distances_conn.commit()
                        print(insert_sql)
                    if res1 == [] and res2 != []:
                        update_sql = "UPDATE distances SET distance=%s WHERE stock1='%s' AND stock2='%s' AND distance_type='%s' AND start_date='%s' AND observations=%s;" % (d,t2,t1,dist,d1_list[0],l)
                        self.distances_cursor.execute(update_sql)
                        self.distances_conn.commit()
                        print(update_sql)
                    if res1 != [] and res2 == []:
                        update_sql = "UPDATE distances SET distance=%s WHERE stock1='%s' AND stock2='%s' AND distance_type='%s' AND start_date='%s' AND observations=%s;" % (d,t1,t2,dist,d1_list[0],l)
                        self.distances_cursor.execute(update_sql)
                        self.distances_conn.commit()
                        print(update_sql)