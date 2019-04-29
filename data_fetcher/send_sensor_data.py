import time
import logging
import re
import shutil
import codecs

from watchdog.events import FileSystemEventHandler

REGEX_FILE_CONTENT = '^[0-9]{2};[-]?([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;([0-9]*[.])?[0-9]+;[0-9]*;'
REGEX_FILE_NAME = '^[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}:[0-9]{2}:[0-9]{2}.rec$'
REGEX_FALSE_FILE = '^.\/received\/.+$'


class FSHandler(FileSystemEventHandler):
    def __init__(self, api_client):
        self.api_client = api_client

    def on_created(self, event):
        successful = False
        logging.info('event type: {}, path: {}'.format(event.event_type, event.src_path))
        time.sleep(1)

        if re.match(REGEX_FILE_NAME, event.src_path.split('/')[-1]):
            with codecs.open(event.src_path, "r", encoding='utf-8', errors='ignore') as f:
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
                    timestamp = timestamp + '+0200'
                    # successful = self.api_client.send_data(temperature, humidity, pressure, timestamp)
                    print('New data')

        if successful:
            shutil.move(event.src_path, event.src_path.replace('received', 'send'))
        elif re.match(REGEX_FALSE_FILE, event.src_path) and not successful:
            shutil.move(event.src_path, event.src_path.replace('received', 'failed'))