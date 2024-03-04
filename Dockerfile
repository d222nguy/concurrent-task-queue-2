FROM python:3.9-slim
RUN apt-get update && apt-get install -y redis-server
WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD redis-server --daemonize yes && python ./main_driver.py
