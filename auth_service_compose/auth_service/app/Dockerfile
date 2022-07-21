FROM python:3.9
WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD sleep 3 && python utils/collect_static.py && flask db upgrade && gunicorn -b 0.0.0.0:5000 "wsgi:app"