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
        conn, cur = self.connectSQL()
        cur.execute("SELECT * FROM Stops WHERE BusStopCode == ?", code)
        stop = cur.fetchall()
        conn.close()
        return stop

    def getStopByDesc(self, desc):
        conn, cur = self.connectSQL()
        cur.execute("SELECT * FROM Stops WHERE Description == ?", desc)
        stop = cur.fetchall()
        conn.close()
        return stop

    def getStopByCoords(self, coords):
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


        conn, cur = connectSQLite()
        cur.execute("SELECT * FROM Routes WHERE BusStopCode == ?", (stop1,))
        buses1 = cur.fetchall()
        cur.execute("SELECT * FROM Routes WHERE BusStopCode == ?", (stop2,))
        buses2 = cur.fetchall()
        conn.close()
        routes = []
        for i in buses1:
            if i[0] in [x[0] for x in buses2]:
                routes.append(i)