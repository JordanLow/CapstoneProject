import sqlite3

class Data:
    def __init__(self, db):
        self.db = db
    
    def init(self, SQLinit, *args):
        conn, cur = self.connectSQL()
        cur.executescript(SQLinit)
        for j in args:
            data, script, params = j
            for i in data:
                cur.execute(script, eval(params))
        conn.commit()
        conn.close()

    def connectSQL(self):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        return conn, cur
    
class BusData(Data):
    def getStopByCode(self, code):
        """
        Find full data of a BusStop given its stop code.

        Usage:
        getStopByCode(code: string) --> Returns a dictionary contaning the full data of the bus stop with the code
        """
        conn, cur = self.connectSQL()
        cur.execute("SELECT * FROM Stops WHERE BusStopCode == ?", code)
        stop = cur.fetchall()
        conn.close()
        if len(stop) == 0:
            return None
        stop = stop[0]
        stop = {
            "Code": stop[0],
            "Road": stop[1],
            "Description": stop[2],
            "Latitude": stop[3],
            "Longitude": stop[4]
        }
        return stop

    def getStopByDesc(self, desc):
        """
        Find full data of a BusStop given its description.

        Usage:
        getStopByCode(desc: string) --> Returns a dictionary contaning the full data of the bus stop with the description
        """
        conn, cur = self.connectSQL()
        cur.execute("SELECT * FROM Stops WHERE Description == ?", desc)
        stop = cur.fetchall()
        conn.close()
        if len(stop) == 0:
            return None
        stop = stop[0]
        stop = {
            "Code": stop[0],
            "Road": stop[1],
            "Description": stop[2],
            "Latitude": stop[3],
            "Longitude": stop[4]
        }
        return stop

    def getStopByCoords(self, coords):
        """
        Find full data of a BusStop given its coordinates.

        Usage:
        getStopByCode(coords: tuple (X,Y)) --> Returns a dictionary contaning the full data of the bus stop at the coordinates
        """
        conn, cur = self.connectSQL()
        cur.execute("SELECT * FROM Stops WHERE Latitude == ? AND Longitude == ?", coords)
        stop = cur.fetchall()
        conn.close()
        print(stop)
        if len(stop) == 0:
            return None
        stop = stop[0]
        stop = {
            "Code": stop[0],
            "Road": stop[1],
            "Description": stop[2],
            "Latitude": stop[3],
            "Longitude": stop[4]
        }
        return stop
    
    def getBusesForStop(self, code):
        """
        Get a list of buses that service a given stop.

        Usage:
        getBusesForStop(code) --> Returns a list of buses that service the bus stop of the given code.
        """
        conn, cur = self.connectSQL()
        cur.execute("SELECT ServiceNo FROM Routes WHERE BusStopCode == ?", (code,))
        buses = cur.fetchall()
        conn.close()
        return list(set(buses))

    def quickSort2D(self, arr, index):
        """
        Sort a list of lists by a given index.
        
        Usage:
        quickSort2D(array, index) --> Returns a list sorted by the given index of its elements
        """
        if len(arr) <= 1:
            return arr
        piv = arr[0]
        L, R = ([], [])
        for i in range(1, len(arr)):
            if arr[i][index] > piv[index]:
                R.append(arr[i])
            else:
                L.append(arr[i])
        return self.quickSort2D(L, index) + [piv] + self.quickSort2D(R, index)
        

    def getBusesBetweenStops(self, stop1, stop2):
        """
        Get all direct buses between two stops, sorted in ascending order.

        Usage:
        getBusesBetweenStops(stop1, stop2) --> returns a list of tuples sorted by each tuple's second element. Each tuple's first element is a serviceNo and the second element is the distance the service travels between the two stops. 
        """
        conn, cur = self.connectSQL()
        cur.execute("SELECT ServiceNo, Distance FROM Routes WHERE BusStopCode == ?", (stop1,))
        route1 = dict(cur.fetchall())
        cur.execute("SELECT ServiceNo, Distance FROM Routes WHERE BusStopCode == ?", (stop2,))
        route2 = dict(cur.fetchall())
        conn.close()
        routes = []
        for i in route1.keys():
            if i in route2.keys():
                routes.append((i, round(abs(route1[i] - route2[i]), 1)))
        return self.quickSort2D(routes, 1) # Sort by index 1 (Distance)