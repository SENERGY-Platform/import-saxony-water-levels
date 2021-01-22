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
from datetime import datetime
from typing import Optional

from rfc3339 import rfc3339

from lib.meta.Station import Station


class Value(object):
    '''
    Class to store value metadata
    '''
    __slots__ = ('tendency', 'value', 'unit', 'status', 'time', 'station', 'predicted_for')

    def __init__(self, tendency: str, value: float, unit: str, staus: str, time: datetime, station: Station,
                 predicted_for: Optional[datetime] = None):
        self.tendency = tendency
        self.value = value
        self.unit = unit
        self.status = staus
        self.time = time
        self.station = station
        self.predicted_for = predicted_for

    def dict(self) -> dict:
        return {
            "tendency": self.tendency,
            "value": self.value,
            "unit": self.unit,
            "status": self.status,
            "predicted_for": rfc3339(self.predicted_for),
            "meta": self.station.dict()
        }
