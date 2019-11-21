from typing import Dict
from wirelesswatch.model import Station, Spot
import pymysql


class MySQLConnector:
    def __init__(self, user: str, password: str):
        self.user = user
        self.password = password
        self.connection = pymysql.connect(host='::1', port=3306, user=self.user, password=self.password, db='wirelesswatch')

    def persist_station(self, station: Station):
        self.connection.cursor().execute('INSERT INTO wirelesswatch.Station (mac) VALUES (%s);', station.mac)
        self.connection.commit()

    def persist_station_name(self, station: Station, name: str):
        self.connection.cursor().execute('INSERT INTO wirelesswatch.StationName (mac, name) VALUES (%s, %s);', (station.mac, name))
        self.connection.commit()

    def persist_spot(self, spot: Spot):
        self.connection.cursor().execute('INSERT INTO wirelesswatch.Spot (transmitter_mac, receiver_mac, sig, spot_time, frame_type, frame_subtype, channel) VALUES (%s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s);',
            (spot.transmitter, spot.receiver, spot.sig, spot.time, spot.frame_type, spot.frame_subtype, spot.channel))
        self.connection.commit()

    def close(self):
        self.connection.close()


class PersistenceController:
    def __init__(self, mysql_user: str, mysql_password: str):
        self.databaseConnector = MySQLConnector(mysql_user, mysql_password)
        self.stations: Dict[str, Station] = {}
        self.counter = 0

    def spot(self, spot: Spot):
        self.counter += 1
        print(self.counter)
        self.spot_station(spot.transmitter, spot.transmitter_name, spot)
        self.spot_station(spot.receiver, None, spot)
        self.databaseConnector.persist_spot(spot)

    def spot_station(self, mac: str, name: str, spot: Spot):
        if mac is None:
            return
        if mac not in self.stations:
            station = Station(mac)
            self.stations[mac] = station
            self.databaseConnector.persist_station(station)
        station: Station = self.stations[mac]
        if name is not None and name not in station.names:
            station.names.append(name)
            self.databaseConnector.persist_station_name(station, name)
        station.spots.append(spot)

    def get_name(self, mac: str):
        if mac not in self.stations:
            return None
        station = self.stations[mac]
        if len(station.names) > 0:
            return station.names[0]
        else:
            return None
