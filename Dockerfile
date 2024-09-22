FROM prefecthq/prefect:2-python3.9

RUN /usr/local/bin/python -m pip install --upgrade pip
WORKDIR /opt/prefect

COPY setup.py .
COPY requirements/ /opt/prefect/requirements/
COPY dataflowops/ /opt/prefect/dataflowops/
COPY flows/ /opt/prefect/flows/

RUN pip install .

# Optional: Check that prefect-aws is installed
RUN pip freeze

# Register blocks
RUN prefect block register -m prefect_aws.ecs
