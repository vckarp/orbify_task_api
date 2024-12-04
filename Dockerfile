FROM python:3.11.10-bullseye

WORKDIR /orbify_task
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000