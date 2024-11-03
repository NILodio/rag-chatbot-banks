# Deploy RAG/AI App To AWS

## Getting Started

### Configure AWS

You need to have an AWS account, and AWS CLI set up on your machine. You'll also need to have Bedrock enabled on AWS (and granted model access to Claude or whatever you want to use).

### Update .env File with AWS Credentials

Create a file named `.env` you can use .env.example as a template:

```
AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AWS_REGION=us-east-1
AWS_BUCKET_NAME=rag-chatbot-banks
PREFECT_BLOCK_AWS_CREDENTIALS=rbc-prefect-aws-credentials
PREFECT_BLOCK_S3_BUCKET=rcb-prefect-s3-bucket
PREFECT_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PREFECT_API_URL=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

This will be used by Docker for when we want to test the image locally. The AWS keys are just your normal AWS credentials and region you want to run this in (even when running locally you will still need access to Bedrock LLM and to the DynamoDB table to write/read the data).

You'll also need a TABLE_NAME for the DynamoDB table for this to work (so you'll have to create that first).

### Installing Requirements

```sh
made develop
```

### Building the Vector DB

Put all the PDF source files you want into `data/source/`.

```sh
# Use "--reset" if you want to overwrite an existing DB.
python src/scripts/main.py populate-database data/chroma data/source --clear
```

### Running the App

```sh
# Execute from image/src directory
python src/scripts/main.py query-rag "How much was the net income in Q3 2024 vs Q3 2023 for RBC"
```

Example output:

```text
Based on the provided context, the total revenue in Q1 2024 compared to Q4 2023 increased in all three scenarios:\n\n1. In the first scenario, total revenue increased by $387 million or 15% from the previous quarter.\n\n2. In the second scenario, total revenue increased by $800 million or 6% from the previous quarter.\n\n3. In the third scenario, total revenue increased by $349 million or 8% from the previous quarter.\n\nTherefore, the total revenue in Q1 2024 increased compared to Q4 2023.
```

### Starting FastAPI Server

```sh
# From image/src directory.
fastapi dev src/api/main.py
```

Then go to `http://0.0.0.0:8000/docs` to try it out.

## Using Docker Image

### Build and Test the Image Locally

These commands can be run from `docker/` directory to build, test, and serve the app locally.

```sh
docker build -t aws_rag_app -f Dockerfile_app ..
```

```sh
# Run the container using command `python app_work_handler.main`
docker run -d --name mycontainer -p 80:80 aws_rag_app
```

![fastapi](/img/fastapi.png)
