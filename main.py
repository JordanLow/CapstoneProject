from flask import *
import datastore


BusData = datastore.BusData("buses.db")


## Import data into the database
## Uncomment if buses.db needs to be initialized

#from dataInit import *
#BusData.init(init, (bstops, bstopscript, bstopparams), (bservices, bservicescript, bserviceparams), (broutes, broutescript, brouteparams))


app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    Search for a Bus Stop based on one of three criteria
    """
    if request.form.get('search', False) == 'YESPLEASE':
        criterion = request.form.get('searchType', "code")
        params = request.form.getlist(criterion, None)
        stop = "No Stop Found!"

        if criterion == 'code':
            stop = BusData.getStopByCode(params)
        elif criterion == "loc":
            stop = BusData.getStopByDesc(params)
        elif criterion == "coords[]":
            stop = BusData.getStopByCoords(params)

        return render_template('search-busstop.html', stop=stop)

    param = request.form.get('param', None)
    return render_template('search.html', param=param)

@app.route('/buses', methods=['GET', 'POST'])
def buses():
    """
    Find all buses that service a bus stop
    """
    stopCode = request.form.get('code', None)
    buses = False
    if stopCode is not None:
        buses = BusData.getBusesForStop(stopCode)
    return render_template('buses.html', buses=buses)

@app.route('/routes', methods=['GET', 'POST'])
def routes():
    """
    Find Direct Buses between two stops, sorted in ascending distance
    """
    stop1 = request.form.get("stop1", False)
    stop2 = request.form.get("stop2", False)
    routes = False
    if stop1 and stop2:
        routes = BusData.getBusesBetweenStops(stop1, stop2)

    return render_template('routes.html', routes=routes)

app.run('0.0.0.0') 