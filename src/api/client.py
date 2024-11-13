import time

import boto3
import streamlit as st
from botocore.exceptions import ClientError, NoCredentialsError
from loguru import logger

from utils.constants import Constants
from utils.divio import get_divio_s3_bucket_env_vars


class Client:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def get_client(
        self, resource, region_name, aws_access_key_id=None, aws_secret_access_key=None
    ):
        """
        Returns an AWS client for a specific resource and region.

        Args:
            resource (str): The AWS service to get the client for.
            region_name (str): The AWS region to use.
        """

        client = None
        try:
            client = boto3.client(
                resource,
                region_name=region_name,
                aws_access_key_id=aws_access_key_id or self.aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
                or self.aws_secret_access_key,
            )
        except Exception as err:
            st.toast(
                "An error occurred while trying to get the AWS client. Please check your AWS credentials.",
                icon="🚫",
            )
            logger.error(err)

        return client

    def check_aws_credentials(self, aws_access_key_id, aws_secret_access_key):
        """
        Checks if the user's AWS credentials are valid.

        Args:
            aws_access_key_id (str): The user's AWS access key ID.
            aws_secret_access_key (str): The user's AWS secret access key.
        """

        user_id = None
        auth_message = None
        try:
            session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
            sts_client = session.client("sts")
            response = sts_client.get_caller_identity()
            user_id = response["UserId"]
            auth_message = Constants.AWS_AUTH_AUTHENTICATED_MESSAGE.value
        except NoCredentialsError:
            auth_message = Constants.AWS_AUTH_NO_CREDENTIALS_MESSAGE.value
        except ClientError:
            auth_message = Constants.AWS_AUTH_INVALID_MESSAGE.value
        except Exception as err:
            auth_message = Constants.AWS_AUTH_UNKOWN_ERROR_MESSAGE.value
            logger.error(err)

        return user_id, auth_message

    @staticmethod
    def list_amazon_bedrock_regions():
        """
        Returns a list of AWS regions where Amazon Bedrock is available.
        """

        regions = []
        try:
            session = boto3.session.Session()
            regions = session.get_available_regions("bedrock")
        except Exception as err:
            st.toast(
                "An error occurred while trying to retrieve the Amazon Bedrock regions.",
                icon="🚫",
            )
            logger.error(err)

        return regions

    def list_foundation_models(
        self,
        region_name,
        **kwargs,
    ):
        """
        Lists the AWS Bedrock models that are available for a specific region.

        Args:
            region_name (str): The AWS region to list the models for.

        Returns:
            models (dict): The list of models available in the region.
        """

        client = self.get_client(
            "bedrock",
            region_name,
        )
        models = {}
        try:
            models = client.list_foundation_models(**kwargs)
        except Exception as err:
            st.toast(
                "An error occurred while trying to retrieve the foundation models.",
                icon="🚫",
            )
            logger.error(err)

        return models

    def list_knowledge_bases(
        self,
        region_name,
        **kwargs,
    ):
        """
        Lists the AWS Bedrock knowledge bases that are available for a specific
        region.

        Args:
            region_name (str): The AWS region to list the knowledge bases for.

        Returns:
            knowledge_bases (dict): The list of knowledge bases available in the region.
        """
        client = self.get_client(
            "bedrock-agent",
            region_name,
        )

        knowledge_bases = {}
        try:
            knowledge_bases = client.list_knowledge_bases(**kwargs)
        except Exception as err:
            st.toast(
                "An error occurred while trying to retrieve the knowledge bases.",
                icon="🚫",
            )
            logger.error(err)

        return knowledge_bases

    def list_data_sources(
        self,
        region_name,
        knowledge_base_id,
        **kwargs,
    ):
        """
        Lists the data sources that are available for a specific knowledge base.

        Args:
            region_name (str): The AWS region to list the data sources for.
            knowledge_base_id (str): The knowledge base ID to list the data sources for.

        Returns:
            data_sources (dict): The list of data sources available for the knowledge base.
        """

        client = self.get_client(
            "bedrock-agent",
            region_name,
        )

        data_sources = {}
        try:
            data_sources = client.list_data_sources(
                knowledgeBaseId=knowledge_base_id, **kwargs
            )
        except Exception as err:
            st.toast(
                "An error occurred while trying to retrieve the data sources.",
                icon="🚫",
            )
            logger.error(err)

        return data_sources

    def get_data_source(
        self,
        region_name,
        data_source_id,
        knowledge_base_id,
        **kwargs,
    ):
        """
        Gets a specific data source for a knowledge base.

        Args:
            region_name (str): The AWS region to get the data source for.
            knowledge_base_id (str): The knowledge base ID to get the data source for.
            data_source_id (str): The data source ID to get.

        Returns:
            data_source (dict): Details of the data source.
        """
        client = self.get_client(
            "bedrock-agent",
            region_name,
        )

        data_source = {}
        try:
            data_source = client.get_data_source(
                dataSourceId=data_source_id,
                knowledgeBaseId=knowledge_base_id,
                **kwargs,
            )
        except Exception as err:
            st.toast(
                "An error occurred while trying to retrieve the data source.",
                icon="🚫",
            )
            logger.error(err)

        return data_source

    def get_assistant_response(
        self,
        region_name,
        model_id,
        messages,
        system_config=[],
        inference_config={},
        **kwargs,
    ):
        """
        Generates a conversation with the Amazon Bedrock model including a
        history of messages, system prompts, and inference configuration
        settings to produce  a model response based on the last user message.

        Args:
            region_name (str): The AWS region to use.
            model_id (str): The model ID to use.
            messages (dict): The messages to send to the model.
            system_config (list[dict]): A set of system configurations to send to the model.
            inference_config (dict): The inference configuration to use.

        Returns:
            response (dict): The response from the model.
        """

        bedrock_runtime_client = self.get_client(
            resource="bedrock-runtime",
            region_name=region_name,
        )

        response = {}
        try:
            response = bedrock_runtime_client.converse_stream(
                modelId=model_id,
                system=system_config,
                messages=messages,
                inferenceConfig=inference_config,
                **kwargs,
            )
        except Exception as err:
            st.toast(
                "An error occurred while trying to retrieve the assistant response.",
                icon="🚫",
            )
            logger.error(err)

        return response

    def get_assistant_response_using_knowledge_base(
        self,
        region_name,
        modelArn,
        knowledge_base_id,
        user_query,
        inference_config={},
        **kwargs,
    ):
        """
        Generates a conversation with the Amazon Bedrock model using a
        knowledge base. This mode of interaction includes a user query,
        and the responses are based solely on the knowledge base resources.
        If no resourse is found to be relevant to the user query, the model
        will return a response stating that no relevant information was found.

        Args:
            region_name (str): The AWS region to use.
            model_id (str): The model ID to use.
            knowledge_base_id (str): The knowledge base ID to use.
            user_query (str): The user's query.
            system (list): The system prompts to send to the model.
            inference_config (dict): The inference configuration to use.

        Returns:
            response (dict): The response from the model.
        """

        response = {}
        try:
            bedrock_agent_runtime_client = self.get_client(
                resource="bedrock-agent-runtime",
                region_name=region_name,
            )

            bedrock_agent_runtime_session_id = st.session_state.get(
                "bedrock_agent_runtime_session_id",
                None,
            )

            retrieve_and_generate_request_params = {
                "input": {
                    "text": user_query,
                },
                "retrieveAndGenerateConfiguration": {
                    "type": "KNOWLEDGE_BASE",
                    "knowledgeBaseConfiguration": {
                        "generationConfiguration": {
                            "inferenceConfig": {
                                "textInferenceConfig": inference_config
                            },
                        },
                        "knowledgeBaseId": knowledge_base_id,
                        "modelArn": modelArn,
                        "retrievalConfiguration": {
                            "vectorSearchConfiguration": {"numberOfResults": 5}
                        },
                    },
                },
            }

            if bedrock_agent_runtime_session_id is not None:
                retrieve_and_generate_request_params["sessionId"] = (
                    bedrock_agent_runtime_session_id
                )
            else:
                retrieve_and_generate_request_params.pop("sessionId", None)

            response = bedrock_agent_runtime_client.retrieve_and_generate(
                **retrieve_and_generate_request_params,
                **kwargs,
            )
            st.session_state.bedrock_agent_runtime_session_id = response["sessionId"]
        except Exception as err:
            st.toast(
                "An error occurred while trying to retrieve the assistant response.",
                icon="🚫",
            )
            logger.error(err)

        return response

    def upload_to_s3_bucket(
        self,
        region_name,
        bucket_name,
        file_name,
        file_body,
        **kwargs,
    ):
        """
        Uploads a file to the S3 bucket related to

        Args:
            region_name (str): The AWS region to use.
            bucket_name (str): The name of the bucket to upload the file to.
            key (str): The filename to use for the uploaded file.
            body (bytes): The file content to upload in bytes.
        """

        divio_buckets = get_divio_s3_bucket_env_vars()

        if bucket_name in divio_buckets:
            s3_client = self.get_client(
                "s3",
                region_name,
                divio_buckets[bucket_name]["ACCESS_KEY_ID"],
                divio_buckets[bucket_name]["SECRET_ACCESS_KEY"],
            )
        else:
            s3_client = self.get_client(
                "s3",
                region_name,
            )

        response = {}
        try:
            with st.spinner("Uploading file..."):
                response = s3_client.put_object(
                    Bucket=bucket_name,
                    Key=file_name,
                    Body=file_body,
                    **kwargs,
                )
                if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    st.toast("File uploaded", icon="✅")
                else:
                    st.toast("File upload failed", icon="🚫")
        except Exception as err:
            st.toast("File upload failed", icon="🚫")
            logger.error(err)

        return response

    def sync_knowledge_base(
        self,
        region_name,
        data_source_id,
        knowledge_base_id,
        **kwargs,
    ):
        """
        Syncs a knowledge base.

        Args:
            region_name (str): The AWS region to use.
            data_source_id (str): The data source ID to sync.
            knowledge_base_id (str): The knowledge base ID to sync.
        """

        bedrock_agent_client = self.get_client(
            "bedrock-agent",
            region_name,
        )

        response = {}
        try:
            max_retries = 10
            with st.spinner("Syncing knowledge base..."):
                response = bedrock_agent_client.start_ingestion_job(
                    knowledgeBaseId=knowledge_base_id,
                    dataSourceId=data_source_id,
                    **kwargs,
                )
                ingestion_job = response["ingestionJob"]

                while ingestion_job["status"] != "COMPLETE":
                    response = bedrock_agent_client.get_ingestion_job(
                        knowledgeBaseId=knowledge_base_id,
                        dataSourceId=data_source_id,
                        ingestionJobId=ingestion_job["ingestionJobId"],
                    )

                    ingestion_job = response["ingestionJob"]
                    time.sleep(2)

                    max_retries -= 1
                    if max_retries <= 0:
                        break

                if ingestion_job["status"] == "COMPLETE":
                    st.toast("Knowledge base synced", icon="✅")
                else:
                    if max_retries <= 0:
                        st.toast(
                            "Knowledge base sync is taking too long. Please check the status in the AWS Console.",
                            icon="🚨",
                        )
                    else:
                        st.toast("Knowledge base sync failed", icon="🚫")
        except Exception as err:
            st.toast("Knowledge base sync failed", icon="🚫")
            logger.error(err)

        return response
