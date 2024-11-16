<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/NILodio/rag-chatbot-banks">
    <img src="img/project-icon.png" alt="Icon" width="80" height="80">
  </a>

<h3 align="center">Canada Banks RAG Chatbot</h3>

This project is about creating a chatbot that makes it easier to explore and understand financial reports from trusted Canadian banks such as RBC, CIBC, TD, and more. Built with privacy and security in mind, the chatbot is designed to work in a secure environment, ensuring compliance with industry regulations. By using advanced AI techniques such as RAG for LLMs, it helps professionals save time by summarizing and highlighting key insights from lengthy reports. This tool was built with a focus on scalability and future updates.

  <p align="center">
    <br />
    <a href="https://github.com/NILodio/rag-chatbot-banks/issues">Report Bug</a>
    ·
    <a href="https://github.com/NILodio/rag-chatbot-banks/issues">Request Feature</a>
  </p>
</div>

## About The Project

<div align="center">
  <img src="img/project-showcase.png" alt="Showcase" width="400" height="400">
</div>
Using a combination of advanced technologies to build a chatbot that extracts, summarizes, and provides insights from financial reports published by major Canadian banks like RBC, CIBC, and TD, and more. Our pipeline started by processing thousands of PDFs web scrapped from the banks websites. These are converted into a vector store for efficient data retrieval. It utilizes Retrieval-Augmented Generation (RAG) to store relevant information, with a conversation buffer memory that tracks previous interactions and feeds them into the selected LLM along with the current user query. <br>
The user interface is developed using Streamlit, offering a simple and interactive experience. The solution is deployed on AWS services, leveraging S3 to store thousands of bank reports and Bedrock for scalable AI model management. This architecture ensures secure and compliant data handling while providing fast analysis to financial professionals. The system also integrates MLOps to support continuous updates and model deployment, making it a scalable tool for automating financial report analysis.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff&style=for-the-badge)
* ![MLflow Badge](https://img.shields.io/badge/MLflow-0194E2?logo=mlflow&logoColor=fff&style=for-the-badge)
* ![Amazon Web Services Badge](https://img.shields.io/badge/Amazon%20Web%20Services-232F3E?logo=amazonwebservices&logoColor=fff&style=flat)
* ![FastAPI Badge](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=fff&style=for-the-badge)
* ![Streamlit Badge](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=fff&style=for-the-badge)
* ![Terraform Badge](https://img.shields.io/badge/Terraform-844FBA?logo=terraform&logoColor=fff&style=for-the-badge)
* ![JupyterLab][jupyter-badge]

[jupyter-badge]: https://img.shields.io/badge/jupyter-book-orange?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAZCAMAAAAVHr4VAAAAXVBMVEX////v7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/zdybv7+/v7+/zdybv7+/zdybv7+/v7+/zdybv7+/zdybv7+/zdyaSmqV2AAAAHXRSTlMAEBAgIDAwQEBQUGBgcHCAgJCQoLCwwMDQ4ODw8MDkUIUAAADJSURBVHjaddAFkgNBCAXQP+7uAvc/5tLFVseYF8crUB0560r/5gwvjYYm8gq8QJoyIJNwlnUH0WEnART6YSezV6c5tjOTaoKdfGXtnclFlEBEXVd8JzG4pa/LDql9Jff/ZCC/h2zSqF5bzf4vqkgNwEzeClUd8uMadLE6OnhBFsES5niQh2BOYUqZsfGdmrmbN+TMvPROHUOkde8sEs6Bnr0tDDf2Roj6fmVfubuGyttejCeLc+xFm+NLuLnJeFAyl3gS932MF/wBoukfUcwI05kAAAAASUVORK5CYII=


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [ ] Enhancing User Interaction & Interface; Refine the Streamlit interface to improve user experience
- [ ] Update data extraction script to filter only document with useful information regarding financial reports
- [ ] MLOps Integration & Continuous Updates; Ensure real-time updates and scalability for future bank reports.

We are always open for any suggestions. Please, add them on the [issues section](https://github.com/NILodio/rag-chatbot-banks).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Deploy RAG/AI App To AWS - Configure AWS

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

<!-- CONTACT -->
## Contact
* Danilo Diaz - [GitHub Profile](https://github.com/NILodio)
* Aanal Patel - [GitHub Profile](https://github.com/Aanalpatel99)
* Bimal Shrestha - [GitHub Profile](https://github.com/bimalstha0)
* Ernie Sumoso - [GitHub Profile](https://github.com/ErnieSumoso)
* Jay Saravanan - [GitHub Profile](https://github.com/svjai)

Project Link: https://github.com/NILodio/rag-chatbot-banks
