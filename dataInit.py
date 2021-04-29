import json

routes, services, stops = [[],[],[]]

with open('data/bus_routes.json') as f:
    broutes = json.load(f)

with open('data/bus_services.json') as f:
    bservices = json.load(f)

with open('data/bus_stops.json') as f:
    bstops = json.load(f)  

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