FROM python:3.9
WORKDIR /worker

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD cd src && sleep 60 && python main.py
