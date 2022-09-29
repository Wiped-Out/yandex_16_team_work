FROM python:3.9-slim
WORKDIR /worker

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD sleep 10 && python main.py