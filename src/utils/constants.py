from enum import Enum


class Constants(Enum):
    AWS_AUTH_AUTHENTICATED_MESSAGE = "Authenticated successfully!"
    AWS_AUTH_NO_CREDENTIALS_MESSAGE = "Please provide your AWS credentials to continue."
    AWS_AUTH_INVALID_MESSAGE = "Invalid AWS credentials. Please try again."
    AWS_AUTH_UNKOWN_ERROR_MESSAGE = "An unknown error occurred while trying to authenticate with AWS. Please try again."
    AWS_ACCESS_KEY_FORM_HELP_TEXT = (
        "Sign in with your AWS Access Key to access Amazon Bedrock resources. "
        "For more details on how to create an AWS Access Key, see the relevant "
        "[AWS documentation]"
        "(https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)."
    )
    AWS_REGION_SELECTBOX_HELP_TEXT = (
        "Select the AWS region where your Amazon Bedrock resources are located. "
        "For more details about AWS regions, see the relevant "
        "[AWS documentation]"
        "(https://aws.amazon.com/about-aws/global-infrastructure/regions_az/)."
    )
    AWS_FOUNDATION_MODEL_SELECTBOX_HELP_TEXT = (
        "Amazon Bedrock foundation models are pre-trained models that can "
        "be used to perform various tasks in the field of generative AI. "
        "For more details, see the relevant "
        "[Amazon Bedrock documentation]"
        "(https://aws.amazon.com/what-is/foundation-models/)."
    )
    AWS_FOUNDATION_MODEL_CONFIGURATION_MAX_TOKENS_HELP_TEXT = (
        "The maximum number of tokens that the model can generate in a single response."
    )
    AWS_FOUNDATION_MODEL_CONFIGURATION_TEMPERATURE_HELP_TEXT = (
        "The temperature affects the shape of the probability distribution "
        "for the predicted output and influences the likelihood of the model "
        "selecting lower-probability outputs. In other words, a higher temperature "
        "will result in more creative responses, while a lower temperature will "
        "result in more predictable responses."
    )
    AWS_FOUNDATION_MODEL_CONFIGURATION_TOP_P_HELP_TEXT = (
        "The percentage of most-likely candidates that the model considers "
        "for the next token. Choose a lower value to decrease the size of "
        "the pool and limit the options to more likely outputs. Choose a "
        "higher value to increase the size of the pool and allow the model "
        "to consider less likely outputs."
    )
    AWS_FOUNDATION_MODEL_CONFIGURATION_SYSTEM_PROMPT_HELP_TEXT = (
        "A system prompt is a unique message that gives extra context or "
        "instructions to the AI model. It helps steer the model's behavior "
        "and establishes expectations for its responses."
    )
    KNOWLEDGE_BASE_SELECTBOX_HELP_TEXT = (
        "Amazon Bedrock knowledge bases are collections of data sources that "
        "can be used to provide context to your foundation model. "
        "For more details, see the relevant "
        "[Amazon Bedrock documentation]"
        "(https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base)."
    )
    KNOWLEDGE_BASE_SEARCH_MODE_ENABLED_HELP_TEXT = (
        "Responses will be based solely on the selected Knowledge Base resources. "
        "Streaming responses and system prompts are not supported in this mode. "
        "Remove Knowledge Base selection to disable."
    )
    DATA_SOURCE_SELECTBOX_HELP_TEXT = (
        "A data source contains files with information that can be retrieved "
        "when your knowledge base is queried. For more details, see the relevant "
        "[Amazon Bedrock documentation]"
        "(https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ds)."
    )
