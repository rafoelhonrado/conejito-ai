"""
ui.py

Streamlit chat UI for the local finance assistant.
"""

import pandas as pd
import streamlit as st

from db import create_database
from parser import parse_user_message
from router import execute


st.set_page_config(
    page_title="Finance Agent",
    page_icon="💰",
    layout="centered",
)

create_database()

st.title("💰 Finance Agent")
st.caption("Local AI finance assistant using llama.cpp + SQLite")


def display_result(result):
    if isinstance(result, list):
        df = pd.DataFrame(result)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    else:
        st.write(result)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I can manage accounts, categories, transactions, and reports.",
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        content = message["content"]

        if isinstance(content, list):
            display_result(content)
        else:
            st.write(content)

user_input = st.chat_input("Ask me something...")

if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                action_obj = parse_user_message(user_input)
                result = execute(action_obj)

            st.subheader("Action")
            st.code(str(action_obj), language="text")

            st.subheader("Result")
            display_result(result)

            response = result

        except Exception as e:
            response = f"Error:\n{e}"
            st.error(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
