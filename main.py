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
        return render_template('search-busstop.html', stop=stop)
    param = request.form.get('param', None)
    return render_template('search.html', param=param)

app.run('0.0.0.0')