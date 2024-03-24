import os
import time
import streamlit as st
import json
import pandas as pd

from dotenv import load_dotenv
from kafka import KafkaConsumer
from constants import KAFKA_URL, POST_PROCESSED_DATA_TOPIC, SLEEP_TIME

time.sleep(int(os.getenv(SLEEP_TIME)))

load_dotenv()

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    POST_PROCESSED_DATA_TOPIC,
    bootstrap_servers=[os.getenv(KAFKA_URL)],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

st.title('Predict Language by Input Code')

# Create a placeholder for message bubbles
st.markdown(
    "## Input Code"
)
code_placeholder = st.empty()

st.divider()

st.markdown(
    "## Predicted Language Table"
)
table_score_placeholder = st.empty()
st.divider()
st.markdown(
    "## Consfusion Matrix Report"
)
confusion_matrix_placeholder = st.empty()
st.divider()
st.markdown(
    "## Accuracy Matrix Report"
)
accuracy_matrix_placeholder = st.empty()

st.divider()

st.markdown(
    "## Accuracy Chat"
)

accuracy_chat_placeholder = st.empty()

for msg in consumer:
    if msg is None:
        continue

    code_placeholder.empty()
    code_placeholder.code(f"{msg.value['orig_code']}")

    table_score_placeholder.empty()

    table_score_placeholder.dataframe(pd.DataFrame(msg.value["table_score"]))

    confusion_matrix_placeholder.empty()
    confusion_matrix_placeholder.dataframe(
        pd.DataFrame(msg.value["confusion_matrix"]))

    accuracy_matrix_placeholder.empty()
    accuracy_matrix_placeholder.dataframe(
        pd.DataFrame(msg.value["accuracy_report"]))

    accuracy_chat_placeholder.empty()
    accuracy_chat_placeholder.line_chart(
        msg.value["accuracy"])
