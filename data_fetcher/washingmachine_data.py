import re
from datetime import datetime

REGEX_FILE_CONTENT = '[0-9]{2};(started|stopped)Washing;;'


class WashingmachineData:
    def __init__(self, timestamp, station, start_stop):
        self.timestamp = timestamp
        self.station = station
        self.start_stop = start_stop

    @staticmethod
    def search_string(data):
        return re.search(REGEX_FILE_CONTENT, data)

    @staticmethod
    def convert_string(data):
        if re.match(REGEX_FILE_CONTENT, data):
            split_content = data.split(';')
            return WashingmachineData(datetime.now(), int(split_content[0]), split_content[1])
        else:
            return None
