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

from typing import List

from import_lib.import_lib import get_logger
from requests.auth import HTTPBasicAuth
from requests import Session
import zeep
from zeep.transports import Transport
import pyproj

from lib.meta.Station import Station

logger = get_logger(__name__)

wsdl = 'https://www.umwelt.sachsen.de/umwelt/infosysteme/hwims/webservices/stammdaten-ws?wsdl'

utm_zone = '33N'
utm_ellps = 'WGS84'


def __fetch_metadata(client: zeep.client.Client, typ: str, station_id: str, proj: pyproj.proj.Proj) -> Station:
    logger.info("Fetching metadata for station " + station_id)
    raw = client.service.liefereStammdatenZuMessstation(station_id, typ)
    if len(raw['messstation']) != 1:
        logger.error("Got more than one station with id " + station_id)
    station = raw['messstation'][0]
    long, lat = proj(station["utmOst"], station["utmNord"], inverse=True)
    return Station(station_id, lat, long, station["bezeichnung"], station["gewaesser"])


def get_stations(typ: str, station_ids: List[str], user: str, pw: str) -> List[Station]:
    session = Session()
    session.auth = HTTPBasicAuth(user, pw)
    client = zeep.Client(wsdl,
                         transport=Transport(session=session))
    proj = pyproj.Proj(proj='utm', zone=utm_zone, ellps=utm_ellps)
    stations = {}
    for station_id in station_ids:
        if station_id in stations:
            logger.warning("Duplicate station " + station_id + ". Not fetching metadata again")
        try:
            stations[station_id] = __fetch_metadata(client, typ, station_id, proj)
        except Exception:
            logger.error("Could not fetch metadata for station " + station_id)
    return list(stations.values())
