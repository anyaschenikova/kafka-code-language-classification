import os
import time
import json
import re

from dotenv import load_dotenv
from kafka import KafkaProducer, KafkaConsumer

from constants import KAFKA_URL, PRODUCED_RAW_DATA_TOPIC, PROCESSED_DATA_TOPIC, SLEEP_TIME

load_dotenv()

time.sleep(int(os.getenv(SLEEP_TIME)))

consumer = KafkaConsumer(
    PRODUCED_RAW_DATA_TOPIC,
    bootstrap_servers=[os.getenv(KAFKA_URL)],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=[os.getenv(KAFKA_URL)],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def process_data(raw_data):

    input_code = raw_data["whole_func_string"].replace(
        raw_data["func_documentation_string"], "")

    clear_data = {
        "language": raw_data["language"],
        "clean_code": input_code,
        "func_documentation_string": raw_data["func_documentation_string"],
        "file_extention": raw_data["func_path_in_repository"].split(".")[-1],
        "orig_code": raw_data["whole_func_string"]
    }

    return clear_data


for msg in consumer:
    if msg is None:
        continue

    ml_results = process_data(msg.value)

    producer.send(PROCESSED_DATA_TOPIC,
                  value=ml_results)

    producer.flush()
