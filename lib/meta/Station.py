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

from import_lib.import_lib import get_logger

logger = get_logger(__name__)


class Station(object):
    '''
    Class to store station metadata
    '''
    __slots__ = ('station_id', 'lat', 'long', 'name', 'waterbody')

    def __init__(self, station_id: str, lat: float, long: float,
                 name: str, waterbody: str):
        self.station_id = station_id
        self.lat = lat
        self.long = long
        self.name = name
        self.waterbody = waterbody

    def dict(self) -> dict:
        return {
            "station_id": self.station_id,
            "lat": self.lat,
            "long": self.long,
            "name": self.name,
            "waterbody": self.waterbody,
        }
