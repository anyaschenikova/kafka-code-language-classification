FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY utils/constants.py .
COPY processor/ml/ml_processor.py .


ENTRYPOINT [ "python3", "ml_processor.py" ]