from flask import *
import csv, json

routes, services, stops = [[],[],[]]

with open('data/bus_routes.json') as f:
    broutes = json.load(f)

with open('data/bus_services.json') as f:
    bservices = json.load(f)

with open('data/bus_stops.json') as f:
    bstops = json.load(f)

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
        for stoop in bstops:
            if criterion == 'code':
                if stoop["BusStopCode"] == params[0]:
                    stop = stoop
                    break
            elif criterion == "loc":
                if stoop["Description"] == params[0]:
                    stop = stoop
                    break;
            elif criterion == "coords":
                if stoop["Longtitude"] == params[0] and stoop["Latitude"] == params[1]:
                    stop = stoop
                    break;
        return render_template('search-busstop.html', stop=stop)
    param = request.form.get('param', None)
    return render_template('search.html', param=param)

@app.route('/routes', methods=['GET', 'POST'])
def routes():
    stopCode = request.form.get('code', None)
    buses = set()
    if stopCode is not None:
        for route in broutes:
            if route["BusStopCode"] == stopCode:
                buses.add(route["ServiceNo"])
    else:
        buses = False
    return render_template('routes.html', buses=buses)

app.run('0.0.0.0')