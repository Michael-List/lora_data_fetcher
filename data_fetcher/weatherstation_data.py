import re
from datetime import datetime

REGEX_FILE_CONTENT = '^[0-9]{2};[-]?([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;[0-9]*;'


class WeatherstationData:
    def __init__(self, timestamp, station, temperature=None, humidity=None, pressure=None, vis_light=None,
                 ir_light=None, uv_light=None, gr_moisture=None):
        self.timestamp = timestamp
        self.station = station
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.vis_light = vis_light
        self.ir_light = ir_light
        self.uv_light = uv_light
        self.gr_moisture = gr_moisture

    @staticmethod
    def validate_string(data):
        if re.match(REGEX_FILE_CONTENT, data):
            split_content = data.split(';')
            return WeatherstationData(datetime.now(),
                                      int(split_content[0]),
                                      float(split_content[1]),
                                      float(split_content[3]),
                                      float(split_content[2]),
                                      float(split_content[4]),
                                      float(split_content[5]),
                                      float(split_content[6]),
                                      float(split_content[7]))
        else:
            return None
