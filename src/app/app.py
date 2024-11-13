import streamlit as st

from api.client import Client
from utils.constants import Constants
from utils.divio import generate_conversation

client = Client()


# ~~~ Page Configuration ~~~ 🎨
st.set_page_config(
    page_title="Amazon Bedrock Chatbot Demo",
    initial_sidebar_state="expanded",
)


st.header("RAG Chatbot for Banks 🏦")

col1, col2 = st.columns([1, 1])
with col1:
    st.link_button(
        "Source Code (GitHub) 🔗",
        "https://github.com/NILodio/rag-chatbot-banks",
        use_container_width=True,
    )
with col2:
    st.link_button(
        "Blog Post 🔗",
        "https://furtive-crate-436.notion.site/AI-and-ML-Capstone-Project-96dcef08a310488fa093b3be3ebf661c",
        use_container_width=True,
    )

st.divider()


# ~~~ AWS Credentials ~~~ 🔑
with st.sidebar:
    st.text("Sign in with your AWS credentials")
    with st.form("aws_credentials_form"):
        st.text(
            "🔑 AWS Access Key",
            help=Constants.AWS_ACCESS_KEY_FORM_HELP_TEXT.value,
        )
        aws_access_key_id = st.text_input(
            "Access Key ID", type="password", key="aws_access_key_id"
        )
        aws_secret_access_key = st.text_input("Secret Access Key", type="password")
        aws_credentials_form_submitted = st.form_submit_button("Sign In")

    user_id = st.session_state.get("user_id", None)
    auth_message = st.session_state.get(
        "auth_message", Constants.AWS_AUTH_NO_CREDENTIALS_MESSAGE.value
    )

    if aws_credentials_form_submitted:
        user_id, auth_message = client.check_aws_credentials(
            aws_access_key_id, aws_secret_access_key
        )
        st.session_state.user_id = user_id
        st.session_state.auth_message = auth_message

if user_id:
    client.aws_access_key_id = aws_access_key_id
    client.aws_secret_access_key = aws_secret_access_key
    if not st.session_state.get("valid_aws_credentials_toast_shown", False):
        st.session_state.valid_aws_credentials_toast_shown = True
        st.toast(auth_message, icon="🎉")
else:
    st.session_state.valid_aws_credentials_toast_shown = False
    st.info(auth_message, icon="🚨")


# ~~~ AWS Region Selection ~~~ 🌍
with st.sidebar:
    # Listing available AWS regions does not require credentials.
    amazon_bedrock_regions_response = client.list_amazon_bedrock_regions()

    st.divider()
    region = st.selectbox(
        "🌍 AWS Region",
        placeholder="Select an AWS Region",
        options=amazon_bedrock_regions_response if user_id else [],
        help=Constants.AWS_REGION_SELECTBOX_HELP_TEXT.value,
        index=None,
        disabled=user_id is None,
    )

if user_id and not region:
    st.info("Please select an AWS region to view the available models.", icon="🌍")


# ~~~ Chat Messages ~~~ 📬
messages = st.session_state.get("messages", [])


# ~~~ Foundation Model Selection ~~~ 🧠
with st.sidebar:
    models = {}
    if region:
        foundation_models_response = client.list_foundation_models(
            region_name=region,
            byOutputModality="TEXT",
        )

        # NOTE: boto3 does not supports filtering by responseStreamingSupported.
        models = {
            m["modelId"]: {
                "name": m["modelName"],
                "model_arn": m["modelArn"],
            }
            for m in foundation_models_response.get("modelSummaries", [])
            if m.get("responseStreamingSupported", False)
        }

    st.divider()
    model_id = st.selectbox(
        "🧠 Model",
        placeholder="Select a Model",
        options=models,
        # Enable the following 2 lines (captions, format_func) if you go for
        # a radio button instead. (Optional)
        # captions = models,
        # format_func = lambda x: models[x]["name"],
        help=Constants.AWS_FOUNDATION_MODEL_SELECTBOX_HELP_TEXT.value,
        index=None,
        disabled=not all([user_id, region]),
    )

if not model_id and region:
    st.info(
        (
            "Please select a model to "
            f"{'continue' if messages else 'start'} the conversation."
        ),
        icon="🧠",
    )

with st.sidebar:
    with st.form("model_configuration_form"):
        max_tokens = st.slider(
            "Max Tokens",
            min_value=20,
            max_value=1000,
            value=500,
            step=20,
            disabled=not model_id,
            help=Constants.AWS_FOUNDATION_MODEL_CONFIGURATION_MAX_TOKENS_HELP_TEXT.value,
        )
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1,
            disabled=not model_id,
            help=Constants.AWS_FOUNDATION_MODEL_CONFIGURATION_TEMPERATURE_HELP_TEXT.value,
        )
        top_p = st.slider(
            "topP",
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.1,
            disabled=not model_id,
            help=Constants.AWS_FOUNDATION_MODEL_CONFIGURATION_TOP_P_HELP_TEXT.value,
        )
        system_prompt = st.text_input(
            "System Prompt",
            placeholder="Enter a system prompt",
            disabled=not model_id,
            help=Constants.AWS_FOUNDATION_MODEL_CONFIGURATION_SYSTEM_PROMPT_HELP_TEXT.value,
            value=None,
        )

        system_config = []
        if system_prompt:
            system_config = [{"text": system_prompt}]

        inference_config = {
            "maxTokens": max_tokens,
            "temperature": temperature,
            "topP": top_p,
        }

        st.form_submit_button(
            "Apply",
            disabled=not model_id,
        )


# ~~~ Knowledge Base ~~~ 🗄️
with st.sidebar:
    knowledge_base_id = None

    # ~~~ Knowledge Base ~~~ 🗄️
    knowledge_bases = {}

    if region and model_id:
        knowledge_bases_response = client.list_knowledge_bases(
            region_name=region,
        )
        knowledge_bases_summaries = knowledge_bases_response.get(
            "knowledgeBaseSummaries", []
        )
        knowledge_bases = {
            kb["knowledgeBaseId"]: kb["name"] for kb in knowledge_bases_summaries
        }

    st.divider()
    knowledge_base_id = st.selectbox(
        "🔍 Knowledge Base",
        placeholder="Select a Knowledge Base",
        options=knowledge_bases,
        format_func=lambda x: knowledge_bases[x],
        help=Constants.KNOWLEDGE_BASE_SELECTBOX_HELP_TEXT.value,
        index=None,
        disabled=not all([user_id, region]),
    )


if knowledge_base_id:
    st.text(
        "🔍 Knowledge Base search mode enabled.",
        help=Constants.KNOWLEDGE_BASE_SEARCH_MODE_ENABLED_HELP_TEXT.value,
    )


with st.sidebar:
    # ~~~ Data Source ~~~ 🗃️
    knowledge_base_data_sources = {}
    if knowledge_base_id:
        response = client.list_data_sources(
            region_name=region,
            knowledge_base_id=knowledge_base_id,
        )
        knowledge_base_data_sources = {
            ds["dataSourceId"]: ds["name"]
            for ds in response.get("dataSourceSummaries", [])
        }

    data_source = st.selectbox(
        "📤 Upload file to Data Source",
        placeholder="Select a Data Source",
        options=knowledge_base_data_sources,
        format_func=lambda x: knowledge_base_data_sources[x],
        index=None,
        disabled=not knowledge_base_id,
        help=Constants.DATA_SOURCE_SELECTBOX_HELP_TEXT.value,
    )

    data_source_bucket_name = None
    if data_source:
        data_source_details = client.get_data_source(
            region_name=region,
            data_source_id=data_source,
            knowledge_base_id=knowledge_base_id,
        )

        data_source_bucket_arn = data_source_details["dataSource"][
            "dataSourceConfiguration"
        ]["s3Configuration"]["bucketArn"]
        data_source_bucket_name = data_source_bucket_arn.split(":::")[-1]

    # ~~~ Document Upload ~~~ 📁
    uploaded_file = None
    upload_file_to_s3_bucket_form_submitted = False
    if data_source_bucket_name:
        with st.form("upload_file_to_s3_bucket_form", border=False):
            uploaded_file = st.file_uploader(
                "📁 Upload file",
                type=["txt", "csv", "md", "pdf"],
                disabled=not data_source_bucket_name,
                label_visibility="collapsed",
            )
            upload_file_to_s3_bucket_form_submitted = st.form_submit_button(
                "Upload & Sync",
                disabled=not data_source_bucket_name,
            )

    if all(
        [
            upload_file_to_s3_bucket_form_submitted,
            uploaded_file,
            data_source_bucket_name,
        ]
    ):
        upload_to_s3_bucket_response = client.upload_to_s3_bucket(
            region_name=region,
            bucket_name=data_source_bucket_name,
            file_name=uploaded_file.name,
            file_body=uploaded_file.getvalue(),
        )

        sync_knowledge_base_response = client.sync_knowledge_base(
            region_name=region,
            data_source_id=data_source,
            knowledge_base_id=knowledge_base_id,
        )


# ~~~ Build Chat ~~~ 💬
prompt = st.chat_input(
    (
        f"Message {models[model_id]['name']}"
        if model_id
        else (
            "Please select a model to "
            f"{'continue' if messages else 'start'} the conversation."
        )
    ),
    disabled=not model_id,
    max_chars=1000,
)

if prompt:
    user_message = {
        "role": "user",
        "content": [{"text": prompt}],
    }
    messages.append(user_message)
    st.session_state.messages = messages

    if knowledge_base_id:
        assistant_response = client.get_assistant_response_using_knowledge_base(
            region_name=region,
            modelArn=models[model_id]["model_arn"],
            knowledge_base_id=knowledge_base_id,
            user_query=prompt,
            inference_config=inference_config,
        )
    else:
        assistant_response = client.get_assistant_response(
            region_name=region,
            model_id=model_id,
            system_config=system_config,
            messages=messages,
            inference_config=inference_config,
        )

    if assistant_response:
        if knowledge_base_id:
            stream = assistant_response["output"]["text"]
        else:
            stream = (
                chunk["contentBlockDelta"]["delta"]["text"]
                for chunk in assistant_response["stream"]
                if "contentBlockDelta" in chunk
            )

        assistant_message = {
            "role": "assistant",
            "content": [{"text": stream}],
        }
        messages.append(assistant_message)
        st.session_state.messages = messages
    else:
        messages.pop()
        st.session_state.messages = messages


# ~~~ Chat Display ~~~ 💬
if messages:
    st.button(
        "Clear Chat",
        on_click=lambda: st.session_state.pop("messages"),
    )
else:
    if model_id:
        st.info(
            "All set! You're ready to start a conversation.",
            icon="🌟",
        )

generate_conversation(st.session_state.get("messages", []))
