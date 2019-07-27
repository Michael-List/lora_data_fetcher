import logging
import time
import os

from data_fetcher.api_client import ApiClient
from data_fetcher.washingmachine_data import WashingmachineData
from data_fetcher.weatherstation_data import WeatherstationData

FIFO_PATH = '/dev/shm/receive_fifo'

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    while not os.path.exists(FIFO_PATH):
        logger.debug('Pipe file ' + FIFO_PATH + ' doesn\'t exist. Waiting till created')
        time.sleep(5)

    with open(FIFO_PATH, "rb") as f:
        api_client = ApiClient()
        last_ws_data = None
        ws_data = None
        inc_data = ''

        while True:
            inc_string = f.read(1).decode("utf-8", 'ignore')
            if inc_string:
                logger.debug('New data: ' + inc_string)
                inc_data += inc_string

                logger.debug('String before manipulating: ' + inc_data)

                ws_match = WeatherstationData.search_string(inc_data)
                wm_match = WashingmachineData.search_string(inc_data)

                if ws_match and not wm_match:
                    logger.debug('Found ws: ' + ws_match.group(0))
                    inc_data = inc_data[ws_match.span(0)[1]:]
                    ws_data = WeatherstationData.convert_string(ws_match.group(0))

                    if ws_data is not None and (last_ws_data is None or ws_data.__ne__(last_ws_data)):
                        logger.debug("weather data doesn't equal last weather data")
                        api_client.send_ws_data(db='weatherstation', ws_data=ws_data)
                        last_ws_data = ws_data

                if wm_match and not ws_match:
                    logger.debug('Found wm: ' + ws_match.group(0))
                    inc_data = inc_data[wm_match.span(0)[1]:]
                    wm_data = WashingmachineData.convert_string(ws_match.group(0))
                    api_client.send_wm_data(db='washingmachine', wm_data=wm_data)

                if wm_match.span(0)[0] > ws_match.span(0)[0]:
                    logger.debug('Found ws: ' + ws_match.group(0))
                    inc_data = inc_data[ws_match.span(0)[1]:]
                    ws_data = WeatherstationData.convert_string(ws_match.group(0))

                    if ws_data is not None and (last_ws_data is None or ws_data.__ne__(last_ws_data)):
                        logger.debug("weather data doesn't equal last weather data")
                        api_client.send_ws_data(db='weatherstation', ws_data=ws_data)
                        last_ws_data = ws_data
                else:
                    logger.debug('Found wm: ' + ws_match.group(0))
                    inc_data = inc_data[wm_match.span(0)[1]:]
                    wm_data = WashingmachineData.convert_string(ws_match.group(0))
                    api_client.send_wm_data(db='washingmachine', wm_data=wm_data)

                logger.debug('String after manipulating: ' + inc_data)

            time.sleep(0.2)
