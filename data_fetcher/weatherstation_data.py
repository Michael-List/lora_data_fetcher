import re
from datetime import datetime

REGEX_FILE_CONTENT = '^[0-9]{2};[-]?([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;[0-9]*;'


class WeatherstationData:
    def __init__(self, timestamp, station, temperature=None, humidity=None, pressure=None):
        self.timestamp = timestamp
        self.station = station
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    @staticmethod
    def validate_string(data):
        if re.match(REGEX_FILE_CONTENT, data):
            split_content = data.split(';')
            return WeatherstationData(datetime.now(),
                                      int(split_content[0]),
                                      float(split_content[1]),
                                      float(split_content[3]),
                                      float(split_content[2]))
        else:
            return None
