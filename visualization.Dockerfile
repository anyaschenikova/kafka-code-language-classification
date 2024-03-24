FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY utils/constants.py .
COPY consumer/visualization/visualization_consumer.py .

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "visualization_consumer.py", "--server.port=8501", "--server.address=0.0.0.0"]
