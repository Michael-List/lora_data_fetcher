import sys
import json
import logging

import requests

SERVER_URL = 'http://localhost:8086/write'
SERVER_USER = 'user'
SERVER_PASSWORD = 'user'


class ApiClient:
    token = None
    api_url = SERVER_URL
    session = requests.Session()

    def __init__(self):
        # if self.token:
        #     self.session.headers.update({'Authorization': self.token})
        # else:
        #     # if no token, do login
        #     if not self.token:
        #         try:
        #             self._login()
        #         except requests.HTTPError:
        #             sys.exit('Username-password invalid')
        pass

    def _login(self):
        headers = {'content-type': 'application/json'}
        payload = {
            'username': SERVER_USER,
            'password': SERVER_PASSWORD
        }
        r = requests.post(self.api_url + '/token/generate-token',
                          data=json.dumps(payload),
                          headers=headers)

        # raise exception if cannot login
        r.raise_for_status()

        # save token and update session
        self.token = r.json()['token']
        self.session.headers.update({'Authorization': 'Bearer ' + self.token})

    def _test_auth(self):
        r = self.session.get(self.api_url + '/api/temperature/1')
        # TODO: Make it more beautiful and error proof
        if r.status_code != 401:
            return True
        else:
            return False

    def send_data(self, db, ws_data):
        successful = True
        # if not self._test_auth():
        #     self._login()
        if ws_data.timestamp is None:
            raise Exception('Timestamp cannot be None')
        if db is None:
            raise Exception('db cannot be None')

        if ws_data.temperature:
            r = self.session.post(url=self.api_url, params={'db': db}, data='temperature,station=' + ws_data.station + ' value=' + str(ws_data.temperature) + ' ' + str(int((ws_data.timestamp.timestamp() * 1e+9))))
            if r.status_code not in range(200, 300):
                logging.warning('Could not post temperature, status code was: {}'.format(r.status_code))
                successful = False

        if ws_data.humidity:
            r = self.session.post(url=self.api_url, params={'db': db}, data='humidity,station=' + ws_data.station + ' value=' + str(ws_data.humidity) + ' ' + str(int((ws_data.timestamp.timestamp() * 1e+9))))
            if r.status_code not in range(200, 300):
                logging.warning('Could not post humidity, status code was: {}'.format(r.status_code))
                successful = False

        if ws_data.pressure:
            r = self.session.post(url=self.api_url, params={'db': db}, data='pressure,station=' + ws_data.station + ' value=' + str(ws_data.pressure) + ' ' + str(int((ws_data.timestamp.timestamp() * 1e+9))))
            if r.status_code not in range(200, 300):
                logging.warning('Could not post pressure, status code was: {}'.format(r.status_code))
                successful = False

        # if humidity:
        #     payload = {
        #         "humidity": humidity,
        #         "timestamp": timestamp
        #     }
        #     self.session.post(url=self.api_url + '/api/humidity', json=payload)
        #     if r.status_code not in range(200, 300):
        #         logging.warning('Could not post humidity, status code was: {}'.format(r.status_code))
        #         successful = False
        #
        # if pressure:
        #     payload = {
        #         "pressure": pressure,
        #         "timestamp": timestamp
        #     }
        #     self.session.post(url=self.api_url + '/api/pressure', json=payload)
        #     if r.status_code not in range(200, 300):
        #         logging.warning('Could not post pressure, status code was: {}'.format(r.status_code))
        #         successful = False

        return successful
