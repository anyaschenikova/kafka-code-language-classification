import os
import time
import json
import torch
import random

from dotenv import load_dotenv
from kafka import KafkaConsumer, KafkaProducer
from transformers import TextClassificationPipeline, RobertaForSequenceClassification, RobertaTokenizer

from constants import KAFKA_URL, PROCESSED_DATA_TOPIC, ML_DATA_TOPIC, SLEEP_TIME, ML_PROCESS, CODE_NAMES

load_dotenv()

cur_ml_process = os.getenv(ML_PROCESS)

if cur_ml_process != "random_sample":

    CODEBERTA_LANGUAGE_ID = "huggingface/CodeBERTa-language-id"

    pipeline = TextClassificationPipeline(
        model=RobertaForSequenceClassification.from_pretrained(
            CODEBERTA_LANGUAGE_ID, device_map="auto"),
        tokenizer=RobertaTokenizer.from_pretrained(
            CODEBERTA_LANGUAGE_ID)
    )

time.sleep(int(os.getenv(SLEEP_TIME)))

consumer = KafkaConsumer(
    PROCESSED_DATA_TOPIC,
    bootstrap_servers=[os.getenv(KAFKA_URL)],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=[os.getenv(KAFKA_URL)],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def ml_processing(processed_data):
    if cur_ml_process != "random_sample":
        predicted_language = pipeline(processed_data["clean_code"])[0]
    else:
        probability = random.uniform(0.95, 1.00)

        predicted_language = {
            "language": random.choice(CODE_NAMES),
            "probability": probability
        }

    processed_data["predicted_language"] = predicted_language

    return processed_data


for msg in consumer:
    if msg is None:
        continue

    ml_results = ml_processing(msg.value)

    print(f"MESSAGE {msg.value}")

    producer.send(ML_DATA_TOPIC,
                  value=ml_results)

    producer.flush()
