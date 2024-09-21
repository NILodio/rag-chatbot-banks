FROM public.ecr.aws/lambda/python:3.11
RUN pip install prefect
ADD ml.py .
CMD ["ml.handler"]
