FROM python:latest
LABEL authors="Garrett Allen"

WORKDIR /app
COPY app/. .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
