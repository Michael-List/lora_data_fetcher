import logging
import time
import os

from data_fetcher.api_client import ApiClient
from data_fetcher.weatherstation_data import WeatherstationData

FIFO_PATH = '/dev/shm/receive_fifo'

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    while not os.path.isfile(FIFO_PATH):
        logger.debug('Pipe file ' + FIFO_PATH + 'doesn\'t exist. Waiting till created')
        time.sleep(5)

    with open(FIFO_PATH, "rb") as f:
        api_client = ApiClient()
        last_ws_data = None
        ws_data = None

        while True:
            chunk = f.read(52)
            if chunk:
                try:
                    logger.debug('Received message from lora: ' + chunk.decode("utf-8"))
                    ws_data = WeatherstationData.validate_string(chunk.decode("utf-8"))
                except UnicodeDecodeError:
                    logger.warning('Could not decode received message')

                if ws_data is not None and (last_ws_data is None or ws_data.__ne__(last_ws_data)):
                    logger.debug("weather data doesn't equal last weather data")
                    api_client.send_data(db='weatherstation', ws_data=ws_data)
                    last_ws_data = ws_data

            time.sleep(0.2)
