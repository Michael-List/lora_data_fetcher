import logging
from time import sleep
import sys
import time
from datetime import datetime

from watchdog.observers import Observer

from data_fetcher.api_client import ApiClient
from data_fetcher.send_sensor_data import FSHandler
from data_fetcher.weatherstation_data import WeatherstationData

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    with open('/dev/shm/receive_fifo', "rb") as f:
        while True:
            # Read is blocking
            chunk = f.read(52)
            if chunk:
                logger.debug('Received message from lora: ' + chunk.decode("utf-8"))
                ws_data = WeatherstationData.validate_string(chunk.decode("utf-8"))
                #             if ws_data is not None:
                #                 print(ws_data.timestamp)
                #                 print(ws_data.station)
                #                 print(ws_data.temperature)

    # ws_data = WeatherstationData(datetime.now(), 1, 20.33)
    # print(int(datetime.now().timestamp() * 1e+9))
    #
    # api_client = ApiClient()
    # api_client.send_data(db='weatherstation', ws_data=ws_data)

    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # api_client = ApiClient()
    # event_handler = FSHandler(api_client)
    # observer = Observer()
    # observer.schedule(event_handler, path, recursive=True)
    # observer.start()
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    # observer.join()
