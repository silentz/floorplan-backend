FROM python:3.8-slim

RUN apt update -y
RUN apt install -y g++ \
                   build-essential

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ backend/
