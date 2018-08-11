import sys
import json
import logging

import requests

SERVER_URL = 'http://localhost:8080'
SERVER_USER = 'test'
SERVER_PASSWORD = 'test'


class ApiClient():
    token = None
    api_url = SERVER_URL
    session = requests.Session()

    def __init__(self):
        if self.token:
            self.session.headers.update({'Authorization': self.token})
        else:
            # if no token, do login
            if not self.token:
                try:
                    self._login()
                except requests.HTTPError:
                    sys.exit('Username-password invalid')

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

    def send_data(self, temperature=None, humidity=None, pressure=None, timestamp=None):
        successful = True
        if not self._test_auth():
            self._login()
        if timestamp is None:
            raise Exception('Timestamp cannot be None')

        if temperature:
            payload = {
                "temperature": temperature,
                "timestamp": timestamp
            }
            r = self.session.post(url=self.api_url + '/api/temperature', json=payload)
            if r.status_code != 200:
                logging.warning('Could not post temperature, status code was: {}'.format(r.status_code))
                successful = False

        if humidity:
            payload = {
                "humidity": humidity,
                "timestamp": timestamp
            }
            self.session.post(url=self.api_url + '/api/humidity', json=payload)
            if r.status_code != 200:
                logging.warning('Could not post humidity, status code was: {}'.format(r.status_code))
                successful = False

        if pressure:
            payload = {
                "pressure": pressure,
                "timestamp": timestamp
            }
            self.session.post(url=self.api_url + '/api/pressure', json=payload)
            if r.status_code != 200:
                logging.warning('Could not post pressure, status code was: {}'.format(r.status_code))
                successful = False

        return successful
