import os

import streamlit as st


def get_divio_s3_bucket_env_vars():
    """
    Detects any Divio S3 Buckets environment variables.

    Returns:
        dict: A dictionary containing the Divio S3 Buckets environment
        variables with the bucket names as keys and additional information
        such as the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY as values.
    """

    env_vars = dict(os.environ.items())

    divio_bucket_env_var_suffix = "_BUCKET"

    divio_buckets_env_vars = {
        v: {
            "ACCESS_KEY_ID": env_vars.get(
                f"{k.split(divio_bucket_env_var_suffix)[0]}_ACCESS_KEY_ID"
            ),
            "SECRET_ACCESS_KEY": env_vars.get(
                f"{k.split(divio_bucket_env_var_suffix)[0]}_SECRET_ACCESS_KEY"
            ),
        }
        for k, v in env_vars.items()
        if k.endswith(divio_bucket_env_var_suffix)
    }

    return divio_buckets_env_vars


def generate_conversation(messages):
    """
    Generates a conversation from a list of messages being able to
    distinguish between streaming and non-streaming responses and
    displaying them accordingly.

    Args:
        messages (list[dict]): A list of messages to generate the conversation from.
    """

    for message in st.session_state.get("messages", []):
        message_text = message["content"][0]["text"]
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message_text)
        else:
            with st.chat_message("assistant"):
                if not isinstance(message_text, str):
                    stream_to_text = st.write_stream(message_text)
                    message["content"][0]["text"] = stream_to_text
                    st.session_state.messages = messages
                else:
                    st.write(message_text)
