FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY extract.py .
COPY transform.py .
COPY load.py .
COPY etl.py .
COPY lambda_function.py .


CMD ["lambda_function.lambda_handler"]

