FROM python:latest

WORKDIR /app 

RUN apt-get update && apt-get install -y \
    freetds-dev \
    gcc \
    g++ \
    make \
    curl \
    && apt-get clean

ENV CFLAGS="-I/usr/include/openssl"
ENV LDFLAGS="-L/usr/lib/x86_64-linux-gnu"
ENV CPPFLAGS="-I/usr/include/openssl"

COPY requirements.txt .

RUN pip install --pre --no-binary :all: pymssql==2.2.11 --no-cache-dir
RUN pip install -r requirements.txt 

COPY extract.py .
COPY load.py .
COPY clean.py .
COPY pipeline.py .

CMD ["python", "pipeline.py"]

