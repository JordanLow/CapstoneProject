from flask import *
import csv, json

routes, services, stops = [[],[],[]]

with open('data/bus_routes.json') as f:
    routes = json.load(f)

with open('data/bus_services.json') as f:
    services = json.load(f)

with open('data/bus_stops.json') as f:
    stops = json.load(f)

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
        for stoop in stops:
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

app.run('0.0.0.0')