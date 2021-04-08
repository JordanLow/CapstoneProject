CREATE TABLE IF NOT EXISTS Routes (
    ServiceNo TEXT,
    Operator TEXT,
    Direction INTEGER,
    StopSequence INTEGER,
    BusStopCode TEXT,
    Distance REAL,
    WD_FirstBus TEXT,
    WD_LastBus TEXT,
    SAT_FirstBus TEXT,
    SAT_LastBus TEXT,
    SUN_FirstBus TEXT,
    SUN_LastBus TEXT,
    FOREIGN KEY(BusStopCode) REFERENCES Stops(BusStopCode),
    FOREIGN KEY(ServiceNo) REFERENCES Services(ServiceNo),
    FOREIGN KEY(Direction) REFERENCES Services(Direction),
    PRIMARY KEY(ServiceNo, Direction, StopSequence)
);

CREATE TABLE IF NOT EXISTS Services (
    ServiceNo TEXT,
    Operator TEXT,
    Direction INTEGER,
    Category TEXT,
    OriginCode TEXT,
    DestinationCode TEXT,
    AM_Peak_Freq TEXT,
    AM_Offpeak_Freq TEXT,
    PM_Peak_Freq TEXT,
    PM_Offpeak_Freq TEXT,
    LoopDesc TEXT,
    PRIMARY KEY(ServiceNo, Direction)
);

CREATE TABLE IF NOT EXISTS Stops (
    BusStopCode TEXT,
    RoadName TEXT,
    "Description" TEXT,
    Latitude TEXT,
    Longitude TEXT,
    PRIMARY KEY(BusStopCode)
);