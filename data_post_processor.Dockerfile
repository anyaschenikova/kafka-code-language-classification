FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY utils/*.py .
COPY processor/data_post/data_post_processor.py .

ENTRYPOINT [ "python3", "data_post_processor.py" ]