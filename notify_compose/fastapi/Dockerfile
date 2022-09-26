FROM python:3.9
WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD cd src && sleep 10 && gunicorn -b 0.0.0.0:8001 main:app -k uvicorn.workers.UvicornWorker