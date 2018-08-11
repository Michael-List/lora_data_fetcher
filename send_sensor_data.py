import sys
import time
import logging
import re
import shutil
import codecs

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

from api_client import ApiClient

REGEX_FILE_CONTENT = '^[d][0-9]{2};[-]?([0-9]*[.])?[0-9]+;[-]?([0-9]*[.])?[0-9]+;[-]?([0-9]*[.])?[0-9]+;[-]?([0-9]*[.])?[0-9]+;;'
REGEX_FILE_NAME = '^[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2}.rec$'
REGEX_FALSE_FILE = '^.\/received\/.+$'
API_CLIENT = None


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        successful = False
        logging.info('event type: {}, path: {}'.format(event.event_type, event.src_path))
        time.sleep(1)

        if re.match(REGEX_FILE_NAME, event.src_path.split('/')[-1]):
            with codecs.open(event.src_path, "r",encoding='utf-8', errors='ignore') as f:
                content = f.readline()
                if re.match(REGEX_FILE_CONTENT, content):
                    split_content = content.split(';')
                    temperature = (float(split_content[1]) + float(split_content[3])) / 2.0
                    pressure = split_content[2]
                    humidity = split_content[4]

                    # Prepare timestamp string
                    timestamp = event.src_path.split('/')[-1]
                    timestamp = timestamp.replace('.rec', '')
                    timestamp = timestamp.replace('_', 'T')
                    successful = API_CLIENT.send_data(temperature, humidity, pressure, timestamp)

        if successful:
            shutil.move(event.src_path, event.src_path.replace('received', 'send'))
        elif re.match(REGEX_FALSE_FILE, event.src_path) and not successful:
            shutil.move(event.src_path, event.src_path.replace('received', 'failed'))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    API_CLIENT = ApiClient()
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
