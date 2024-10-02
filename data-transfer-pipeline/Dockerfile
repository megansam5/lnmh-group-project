FROM python:latest

WORKDIR /app 

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY extract.py .
COPY load.py .
COPY clean.py .
COPY pipeline.py .

CMD ["python", "pipeline.py"]