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

from datetime import datetime, timezone, timedelta

from import_lib.import_lib import ImportLib, get_logger

from lib.data.Service import Service
from lib.meta.fetch import get_stations

logger = get_logger(__name__)

slice_size = timedelta(days=50)


class WaterLevelImport:
    def __init__(self, lib: ImportLib):
        self.__lib = lib
        logger.info("import init")
        self.__type = lib.get_config("type", "Pegel")
        self.__last_run = None
        previous = lib.get_last_n_messages(len(lib.get_config('stations', [])))
        if previous is not None:
            for t, _ in previous:
                if self.__last_run is None or t < self.__last_run:
                    self.__last_run = t
        if self.__last_run is None:
            if self.__type == "Pegel":
                self.__last_run = datetime.fromtimestamp(1293840000, timezone.utc)  # 2015-01-01
            else:
                self.__last_run = datetime.fromtimestamp(1451606400, timezone.utc)  # 2016-01-01
        else:
            self.__last_run = self.__last_run.replace(tzinfo=timezone.utc)

        with open('credentials.json', 'r') as f:
            import json
            credentials = json.loads(f.read())

        self.__stations = get_stations(self.__type, lib.get_config('stations', []), credentials['user'],
                                       credentials['password'])
        self.__service = Service(credentials['user'], credentials['password'])
        self.__series = lib.get_config("series", "Ziel")
        self.__phys_unit = lib.get_config("phys_unit", "W")

    def import_since_last_run(self):
        self.import_since(self.__last_run)

    def import_since(self, start: datetime):
        now = datetime.now(timezone.utc)
        next_end = start + slice_size
        self.__import_slice(start, next_end)
        while now > next_end:
            start = next_end  # works in python by value
            next_end = start + slice_size
            self.__import_slice(start, next_end)
        self.__last_run = now

    def __import_slice(self, start: datetime, end: datetime):
        values = self.__service.get_multiple_series_data(self.__stations, self.__type, self.__series, self.__phys_unit,
                                                         start, end)
        values.sort(key=lambda v: v.time)
        for value in values:
            self.__lib.put(value.time, value.dict())
