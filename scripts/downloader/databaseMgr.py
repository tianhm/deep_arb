from scripts.utility import *
from datetime import datetime, timedelta

import sqlite3, pandas as pd

class DatabaseMgr():
    def __init__(self):
        self.missing_data = []
        self.included_data = []

    def checkSQL(self,symbol):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        res = self.cursor.fetchall()[0]

        if symbol in res:
            for i in range(self.delta.days + 1):
                if (self.startDate + timedelta(days=i)).weekday() in [6, 7]:
                    continue
                self.cursor.execute("SELECT * FROM %s WHERE Date = %s" % (symbol, datetime.strftime(self.startDate + timedelta(days=i),"%Y-%m-%d")))
                r = self.cursor.fetchall()

                if r == []:
                    self.missing_data.append(symbol)
                    break
            self.included_data.append(symbol)
        else:
            self.missing_data.append(symbol)


    def insertSQL(self, symbol):
        res = q("SELECT name FROM sqlite_master WHERE type='table';")
        if symbol not in res:
            self.cursor.execute("CREATE TABLE %s(Adj_Close FLOAT, Close FLOAT, Date DATE, High FLOAT, Low FLOAT, Open FLOAT, Volume INT);" % symbol)
            self.conn.commit()
        for i in range(self.delta.days + 1):
            this_date = datetime.strftime(self.startDate + timedelta(days=i), "%Y-%m-%d")
            if (self.startDate + timedelta(days=i)).weekday() in [6,7]:
                continue
            self.cursor.execute("SElECT * FROM %s WHERE Date = %s;" % (symbol, i))
            r = self.cursor.fetchall()

            if r == []:
                try:
                    this_row = self.prices[symbol].loc[self.prices[symbol]["Date"] == this_date]
                except Exception as e:
                    break


                if not this_row.empty:
                    v = this_row.values[0]

                    query = "INSERT INTO %s VALUES (%s, %s, '%s', %s, %s, %s, %s);" % (symbol, round(float(v[0]),2),
                                                                                                 round(float(v[1]),2), v[2],
                                                                                                 round(float(v[3]),2), round(float(v[4]),2),
                                                                                                 round(float(v[5]),2), int(v[7]))
                    print(query)
                    self.cursor.execute(query)
                    self.conn.commit()