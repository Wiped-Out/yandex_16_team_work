FROM python:3.9
WORKDIR /functional

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD python prepare_env.py && python -m pytest . --html=report/pytest_report.html