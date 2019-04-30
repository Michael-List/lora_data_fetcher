import logging

from data_fetcher.api_client import ApiClient
from data_fetcher.weatherstation_data import WeatherstationData

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    with open('/dev/shm/receive_fifo', "rb") as f:
        api_client = ApiClient()

        while True:
            # Read is blocking
            chunk = f.read(52)
            if chunk:
                logger.debug('Received message from lora: ' + chunk.decode("utf-8"))
                ws_data = WeatherstationData.validate_string(chunk.decode("utf-8"))

                if ws_data is not None:
                    api_client.send_data(db='weatherstation', ws_data=ws_data)
