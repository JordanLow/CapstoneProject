from flask import *
import sqlite3, json
import datastore

routes, services, stops = [[],[],[]]

with open('data/bus_routes.json') as f:
    broutes = json.load(f)

with open('data/bus_services.json') as f:
    bservices = json.load(f)

with open('data/bus_stops.json') as f:
    bstops = json.load(f)

BusData = datastore.BusData("buses.db")

def qsortlla(arr, index):
    '''
    QuickSORT a List of Lists in Ascending order
    QSORTLLA
    '''
    if len(arr) <= 1:
        return arr
    piv = arr[0]
    L, R = ([], [])
    for i in range(1, len(arr)):
        if arr[i][index] > piv[index]:
            R.append(arr[i])
        else:
            L.append(arr[i])
    return qsortlla(L, index) + [piv] + qsortlla(R, index)
        

init = ""
with open('initTable.sql', 'r') as f:
    init = f.read()

bstopscript = "INSERT INTO Stops VALUES (?, ?, ?, ?, ?)"
bstopparams = "(\
        i[\"BusStopCode\"],\
        i[\"RoadName\"],\
        i[\"Description\"],\
        i[\"Latitude\"],\
        i[\"Longitude\"])"


bservicescript = "INSERT INTO Services VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
bserviceparams = "(\
        i[\"ServiceNo\"],\
        i[\"Operator\"],\
        int(i[\"Direction\"]),\
        i[\"Category\"],\
        i[\"OriginCode\"],\
        i[\"DestinationCode\"],\
        i[\"AM_Peak_Freq\"],\
        i[\"AM_Offpeak_Freq\"],\
        i[\"PM_Peak_Freq\"],\
        i[\"PM_Offpeak_Freq\"],\
        i[\"LoopDesc\"])"

broutescript = "INSERT INTO Routes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
brouteparams = "(\
        i[\"ServiceNo\"],\
        i[\"Operator\"],\
        int(i[\"Direction\"]),\
        int(i[\"StopSequence\"]),\
        i[\"BusStopCode\"],\
        float(i[\"Distance\"]),\
        i[\"WD_FirstBus\"],\
        i[\"WD_LastBus\"],\
        i[\"SAT_FirstBus\"],\
        i[\"SAT_LastBus\"],\
        i[\"SUN_FirstBus\"],\
        i[\"SUN_LastBus\"])"

#BusData.init(init, (bstops, bstopscript, bstopparams), (bservices, bservicescript, bserviceparams), (broutes, broutescript, brouteparams))

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

        if criterion == 'code':
            stop = BusData.getStopByCode(params)
        elif criterion == "loc":
            stop = BusData.getStopByDesc(params)
        elif criterion == "coords":
            stop = BusData.getStopByCoords(params)

        return render_template('search-busstop.html', stop=stop)

    param = request.form.get('param', None)
    return render_template('search.html', param=param)

@app.route('/buses', methods=['GET', 'POST'])
def buses():
    stopCode = request.form.get('code', None)
    buses = False
    if stopCode is not None:
        buses = BusData.getBusesForStop(stopCode)
    return render_template('buses.html', buses=buses)

@app.route('/routes', methods=['GET', 'POST'])
def routes():
    stop1 = request.form.get("stop1", False)
    stop2 = request.form.get("stop2", False)
    routes = False
    if stop1 and stop2:
        routes = BusData.getBusesBetweenStops(stop1, stop2)

    routes = qsortlla(routes, 3)
    return render_template('routes.html', routes=routes)

app.run('0.0.0.0')