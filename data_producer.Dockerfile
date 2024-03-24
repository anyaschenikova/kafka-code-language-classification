FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY utils/*.py .
COPY producer/data/data_producer.py .

ENTRYPOINT [ "python3", "data_producer.py" ]