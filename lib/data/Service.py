#  Copyright 2020 InfAI (CC SES)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from datetime import datetime, timedelta
from typing import List, Dict, Optional

from import_lib.import_lib import get_logger
from requests.auth import HTTPBasicAuth
from requests import Session
import zeep
from zeep.transports import Transport

from lib.data.Value import Value
from lib.meta.Station import Station

logger = get_logger(__name__)

wsdl = 'https://www.umwelt.sachsen.de/umwelt/infosysteme/hwims/webservices/spurwerte-ws?wsdl'


# Class to fetch the actual values
class Service:
    def __init__(self, user: str, pw: str):
        session = Session()
        session.auth = HTTPBasicAuth(user, pw)
        self.__client = zeep.Client(wsdl, transport=Transport(session=session))
        self.__factory = self.__client.type_factory('ns0')

        logger.info('Service init finsihed')

    def get_series_data(self, station: Station, type: str, series: str, phys_unit: str, dt_from: datetime,
                        dt_to: datetime) -> List[Value]:
        return self.get_multiple_series_data([station], type, series, phys_unit, dt_from, dt_to)

    def get_multiple_series_data(self, stations: List[Station], type: str, series: str, phys_unit: str,
                                 dt_from: datetime, dt_to: datetime) -> List[Value]:
        if dt_to - dt_from > timedelta(days=100):
            raise ValueError('Maximum difference of 100 days allowed')
        logger.info("Getting data between " + dt_from.isoformat() + " and " + dt_to.isoformat())
        spur_identifikatoren = []
        for station in stations:
            spur_identifikatoren.append(
                self.__factory.spurIdentifikatorDTO(station.station_id, type, phys_unit, series))
        unit = None
        if phys_unit == 'Q':
            unit = 'm³/s'
        elif phys_unit == 'W':
            unit = 'cm'
        elif phys_unit == 'P':
            unit = 'mm'
        res = self.__client.service.liefereWerteZuSpuren2(spur_identifikatoren, dt_from, dt_to, False)
        if res is None or len(res) == 0:
            return []
        values = []
        for series in res:
            station = self.__find_station(stations, series["spurIdentifikator"]["messstationKennziffer"])
            for element in series["wert"]:
                if element["erstellungsZeitstempel"] is not None:
                    value = Value(element["tendenz"], element["wert"], unit, element["status"],
                                  element["erstellungsZeitstempel"],
                                  station, element["zeitstempel"])
                else:
                    value = Value(element["tendenz"], element["wert"], unit, element["status"], element["zeitstempel"],
                                  station)
                values.append(value)
        return values

    @staticmethod
    def __find_station(stations: List[Station], id: str) -> Optional[Station]:
        for station in stations:
            if station.station_id == id:
                return station
        return None
