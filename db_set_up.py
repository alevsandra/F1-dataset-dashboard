import csv
import sqlite3


def load_file(file_name):
    a_file = open(file_name)
    return csv.reader(a_file)


conn = sqlite3.connect('f1.db')

c = conn.cursor()

c.execute('''CREATE TABLE circuits
            (circuitId integer,
            circuitRef text,
            name text,
            location text,
            country text,
            lat real,
            lng real,
            alt integer,
            url text
            )''')

c.execute('''CREATE TABLE constructor_results
            (constructorResultsId integer,
            raceId integer,
            constructorId integer,
            points integer,
            status text
            )''')

c.execute('''CREATE TABLE constructor_standings
            (constructorStandingsId integer,
            raceId integer,
            constructorId integer,
            points integer,
            final_position integer,
            positionText text,
            wins integer
            )''')

c.execute('''CREATE TABLE constructors
            (constructorId integer,
            constructorRef text,
            name text,
            nationality text,
            url text
            )''')

c.execute('''CREATE TABLE driver_standings
            (driverStandingsId integer,
            raceId integer,
            driverId integer,
            points integer,
            final_position integer,
            positionText integer,
            wins integer
            )''')

c.execute('''CREATE TABLE drivers
            (driverId integer,
            driverRef text,
            driver_number text,
            code text,
            forename text,
            surname text,
            dob blob,
            nationality text,
            url text
            )''')

c.execute('''CREATE TABLE lap_times
            (raceId integer,
            driverId integer,
            lap integer,
            final_position integer,
            time_ text,
            milliseconds integer
            )''')

c.execute('''CREATE TABLE pit_stops
            (raceId integer,
            driverId integer,
            stop integer,
            lap integer,
            time_ blob,
            duration real,
            milliseconds integer
            )''')

c.execute('''CREATE TABLE qualifying
            (qualifyId integer,
            raceId integer,
            driverId integer,
            constructorId integer,
            car_number integer,
            final_position integer,
            q1 text,
            q2 text,
            q3 text
            )''')

c.execute('''CREATE TABLE races
            (aceId integer,
            race_year integer,
            round integer,
            circuitId integer,
            track_name text,
            race_date blob,
            race_time text,
            url text
            )''')

c.execute('''CREATE TABLE results
            (resultId integer,
            raceId integer,
            driverId integer,
            constructorId integer,
            car_number integer,
            grid integer,
            final_position integer,
            positionText text,
            positionOrder integer,
            points integer,
            laps integer,
            time_ text,
            milliseconds integer,
            fastestLap integer,
            rank integer,
            fastestLapTime text,
            fastestLapSpeed real,
            statusId integer
            )''')

c.execute('''CREATE TABLE status
            (statusId integer,
            status text
            )''')

c.executemany("INSERT INTO status VALUES (?, ?)", load_file("data/status.csv"))

c.executemany("INSERT INTO results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              load_file("data/results.csv"))

c.executemany("INSERT INTO races VALUES (?, ?, ?, ?, ?, ?, ?, ?)", load_file("data/races.csv"))

c.executemany("INSERT INTO qualifying VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", load_file("data/qualifying.csv"))

c.executemany("INSERT INTO pit_stops VALUES (?, ?, ?, ?, ?, ?, ?)", load_file("data/pit_stops.csv"))

c.executemany("INSERT INTO lap_times VALUES (?, ?, ?, ?, ?, ?)", load_file("data/lap_times.csv"))

c.executemany("INSERT INTO drivers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", load_file("data/drivers.csv"))

c.executemany("INSERT INTO driver_standings VALUES (?, ?, ?, ?, ?, ?, ?)", load_file("data/driver_standings.csv"))

c.executemany("INSERT INTO constructors VALUES (?, ?, ?, ?, ?)", load_file("data/constructors.csv"))

c.executemany("INSERT INTO constructor_standings VALUES (?, ?, ?, ?, ?, ?, ?)",
              load_file("data/constructor_standings.csv"))

c.executemany("INSERT INTO constructor_results VALUES (?, ?, ?, ?, ?)", load_file("data/constructor_results.csv"))

c.executemany("INSERT INTO circuits VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", load_file("data/circuits.csv"))

conn.commit()

conn.close()
