from flask import *
import sqlite3, json

routes, services, stops = [[],[],[]]

with open('data/bus_routes.json') as f:
    broutes = json.load(f)

with open('data/bus_services.json') as f:
    bservices = json.load(f)

with open('data/bus_stops.json') as f:
    bstops = json.load(f)

def connectSQLite():
    conn = sqlite3.connect("buses.db")
    cur = conn.cursor()
    return conn, cur

conn, cur = connectSQLite()

init = ""
with open('initTable.sql', 'r') as f:
    init = f.read()

cur.executescript(init)
"""
for i in bstops:
    cur.execute('''
    INSERT INTO Stops VALUES (?, ?, ?, ?, ?)
    ''' , (
        i["BusStopCode"],
        i["RoadName"],
        i["Description"],
        i["Latitude"],
        i["Longitude"]
    ))

for i in bservices:
    cur.execute('''
    INSERT INTO Services VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        i["ServiceNo"],
        i["Operator"],
        int(i["Direction"]),
        i["Category"],
        i["OriginCode"],
        i["DestinationCode"],
        i["AM_Peak_Freq"],
        i["AM_Offpeak_Freq"],
        i["PM_Peak_Freq"],
        i["PM_Offpeak_Freq"],
        i["LoopDesc"]
    ))
for i in broutes:
    if i["ServiceNo"] == "252" and i["Distance"] == None:
        continue
    cur.execute('''
    INSERT INTO Routes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        i["ServiceNo"],
        i["Operator"],
        int(i["Direction"]),
        int(i["StopSequence"]),
        i["BusStopCode"],
        float(i["Distance"]),
        i["WD_FirstBus"],
        i["WD_LastBus"],
        i["SAT_FirstBus"],
        i["SAT_LastBus"],
        i["SUN_FirstBus"],
        i["SUN_LastBus"]
    ))

conn.commit()
conn.close()
"""
app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.form.get('search', False) == 'YESPLEASE':
        criterion = request.form.get('searchType', "code")
        params = request.form.getlist(criterion, None)
        stop = "No Stop Found!"
        conn, cur = connectSQLite()

        if criterion == 'code':
            cur.execute("SELECT * FROM Stops WHERE BusStopCode == ?", params)
            stop = cur.fetchall()
        elif criterion == "loc":
            cur.execute("SELECT * FROM Stops WHERE Description == ?", params)
            stop = cur.fetchall()
        elif criterion == "coords":
            cur.execute("SELECT * FROM Stops WHERE Latitude == ? AND Longitude == ?", params)
            stop = cur.fetchall()

        conn.close()
        return render_template('search-busstop.html', stop=stop)

    param = request.form.get('param', None)
    return render_template('search.html', param=param)

@app.route('/routes', methods=['GET', 'POST'])
def routes():
    stopCode = request.form.get('code', None)
    buses = set()
    if stopCode is not None:
        conn, cur = connectSQLite()
        cur.execute("SELECT ServiceNo FROM Routes WHERE BusStopCode == ?", (stopCode,))
        buses = cur.fetchall()
    else:
        buses = False
    return render_template('routes.html', buses=buses)

app.run('0.0.0.0')