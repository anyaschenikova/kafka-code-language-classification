import os
import time
import json

from dotenv import load_dotenv
from kafka import KafkaProducer
from datasets import load_dataset
from pathlib import Path
from tqdm import tqdm

from data_download import download_data_to_local
from constants import KAFKA_URL, PRODUCED_RAW_DATA_TOPIC, SLEEP_TIME, DATA_PATH
from utils import read_files_from_path

load_dotenv()

download_data_to_local()

time.sleep(int(os.getenv(SLEEP_TIME)))

producer = KafkaProducer(
    bootstrap_servers=[os.getenv(KAFKA_URL)],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data_path = Path(os.getenv(DATA_PATH))

while True:
    for data in read_files_from_path(data_path.absolute()):
        producer.send(PRODUCED_RAW_DATA_TOPIC,
                      value=data)

        producer.flush()

        time.sleep(5)
