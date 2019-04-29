import os
from pathlib import Path
from dotenv import load_dotenv

# Load local .env from root folder of the project if not in docker container
if not os.getenv('RUNNING_INSIDE_DOCKER', False):
    load_dotenv(verbose=True)
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

pipeline_path = os.environ['PIPELINE_PATH']
