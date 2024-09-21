FROM public.ecr.aws/lambda/python:3.11
RUN pip install prefect
ADD etl.py .
CMD ["etl.handler"]
