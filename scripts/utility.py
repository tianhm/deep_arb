import datetime, sqlite3, sys, re

def p(text):
    print(str(datetime.datetime.now()) + " | " + text)

def pr(text):
    sys.stdout.write("\r" + text)
    sys.stdout.flush()

def q(query):
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()

    cursor.execute(query)
    query_data = cursor.fetchall()

    outlist = []
    for q in query_data:
        outlist.append(q[0])

    return outlist
