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
        return stop
    
    def getBusesForStop(self, code):
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