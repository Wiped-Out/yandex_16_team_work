FROM python:3.9-slim
RUN apt-get update && apt-get -y install cron

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

COPY . .

RUN echo $PYTHONPATH
# run crond as main process of container
CMD ["cron", "-f"]