import logging

import requests


class ApiClient:
    api_url = 'http://influxdb:8086/write'

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def send_data(self, db, ws_data):
        successful = True
        # if not self._test_auth():
        #     self._login()
        if ws_data.timestamp is None:
            raise Exception('Timestamp cannot be None')
        if db is None:
            raise Exception('db cannot be None')

        timestamp = int((ws_data.timestamp.timestamp() * 1e+9))

        if ws_data.temperature:
            r = requests.post(url=self.api_url,
                              params={'db': db},
                              data='temperature,station=' + str(ws_data.station) +
                                   ' value=' + str(ws_data.temperature) + ' ' + str(timestamp))
            if r.status_code not in range(200, 300):
                self.logger.warning('Could not post temperature, status code was: {}'.format(r.status_code))
                successful = False

        if ws_data.humidity:
            r = requests.post(url=self.api_url,
                              params={'db': db},
                              data='humidity,station=' + str(ws_data.station) +
                                   ' value=' + str(ws_data.humidity) + ' ' + str(timestamp))
            if r.status_code not in range(200, 300):
                self.logger.warning('Could not post humidity, status code was: {}'.format(r.status_code))
                successful = False

        if ws_data.pressure:
            r = requests.post(url=self.api_url,
                              params={'db': db},
                              data='pressure,station=' + str(ws_data.station) +
                                   ' value=' + str(ws_data.pressure) + ' ' + str(timestamp))
            if r.status_code not in range(200, 300):
                self.logger.warning('Could not post pressure, status code was: {}'.format(r.status_code))
                successful = False

        if ws_data.vis_light:
            r = requests.post(url=self.api_url,
                              params={'db': db},
                              data='vis_light,station=' + str(ws_data.station) +
                                   ' value=' + str(ws_data.vis_light) + ' ' + str(timestamp))
            if r.status_code not in range(200, 300):
                self.logger.warning('Could not post vis_light, status code was: {}'.format(r.status_code))
                successful = False

        if ws_data.ir_light:
            r = requests.post(url=self.api_url,
                              params={'db': db},
                              data='ir_light,station=' + str(ws_data.station) +
                                   ' value=' + str(ws_data.ir_light) + ' ' + str(timestamp))
            if r.status_code not in range(200, 300):
                self.logger.warning('Could not post ir_light, status code was: {}'.format(r.status_code))
                successful = False

        if ws_data.uv_light:
            r = requests.post(url=self.api_url,
                              params={'db': db},
                              data='uv_light,station=' + str(ws_data.station) +
                                   ' value=' + str(ws_data.uv_light) + ' ' + str(timestamp))
            if r.status_code not in range(200, 300):
                self.logger.warning('Could not post uv_light, status code was: {}'.format(r.status_code))
                successful = False

        if ws_data.gr_moisture:
            r = requests.post(url=self.api_url,
                              params={'db': db},
                              data='gr_moisture,station=' + str(ws_data.station) +
                                   ' value=' + str(ws_data.gr_moisture) + ' ' + str(timestamp))
            if r.status_code not in range(200, 300):
                self.logger.warning('Could not post gr_moisture, status code was: {}'.format(r.status_code))
                successful = False

        return successful
