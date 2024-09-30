FROM prefecthq/prefect:2-python3.12
RUN /usr/local/bin/python -m pip install --upgrade pip
WORKDIR /opt/prefect
COPY setup.py .
COPY requirements /opt/prefect/requirements
COPY flows/ /opt/prefect/flows/
RUN pip install . --no-cache
RUN prefect block register -m prefect_aws
