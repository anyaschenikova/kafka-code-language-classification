import os
import time
import json
import re
import pandas as pd

from dotenv import load_dotenv
from kafka import KafkaProducer, KafkaConsumer
from sklearn.metrics import confusion_matrix, accuracy_score, precision_recall_fscore_support

from constants import KAFKA_URL, ML_DATA_TOPIC, POST_PROCESSED_DATA_TOPIC, SLEEP_TIME, CODE_NAMES, ML_PROCESS

load_dotenv()

cur_ml_process = os.getenv(ML_PROCESS)

time.sleep(int(os.getenv(SLEEP_TIME)))

consumer = KafkaConsumer(
    ML_DATA_TOPIC,
    bootstrap_servers=[os.getenv(KAFKA_URL)],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=[os.getenv(KAFKA_URL)],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

y_true = []
y_pred = []
accuracys = []


def process_adding_to_y(y: list, y_pred: str):
    adding = y_pred

    y.append(adding)


def create_confusion_matrix(y_true, y_pred):

    result = confusion_matrix(
        y_true, y_pred, labels=CODE_NAMES)

    return pd.DataFrame(columns=CODE_NAMES, index=CODE_NAMES, data=result).to_dict()


def create_accuracy_report(y_true, y_pred):
    precision, recall, fscore, support = list(precision_recall_fscore_support(
        y_true, y_pred, average='weighted'))

    accuracy_report = {
        'precision': {cur_ml_process: precision},
        'recall': {cur_ml_process: recall},
        'fscore': {cur_ml_process: fscore},
    }
    accuracy = accuracy_score(y_true, y_pred)

    accuracy_report["accuracy"] = {cur_ml_process: accuracy}  # accuracy

    accuracys.append(accuracy)

    return accuracy_report


def post_process_data(raw_data):

    process_adding_to_y(y_true, msg.value["language"])
    process_adding_to_y(y_pred, msg.value["predicted_language"]["language"])

    raw_data['table_score'] = {
        "true_language": {cur_ml_process: msg.value["language"]},
        "predicted_language": {cur_ml_process: msg.value["predicted_language"]["language"]},
    }

    raw_data["confusion_matrix"] = create_confusion_matrix(y_true, y_pred)

    raw_data["accuracy_report"] = create_accuracy_report(y_true, y_pred)

    raw_data["accuracy"] = accuracys

    return raw_data


for msg in consumer:
    if msg is None:
        continue

    ml_results = post_process_data(msg.value)

    producer.send(POST_PROCESSED_DATA_TOPIC,
                  value=ml_results)

    producer.flush()
