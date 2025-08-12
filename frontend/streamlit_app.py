
import requests
import streamlit as st
import pandas as pd

import os
backend_default = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="LLM Q&A", layout="wide")
st.title("LLM Q&A")


def save_feedback(index):
    """Save feedback in session state and optionally send to backend"""
    feedback_value = st.session_state[f"feedback_{index}"]
    st.session_state["messages"][index]["feedback"] = feedback_value

with st.sidebar:
    st.header("Backend settings")
    backend_url = st.text_input("FastAPI URL", value=backend_default)
    if st.button("Health check"):
        try:
            r = requests.get(f"{backend_url}/health", timeout=5)
            st.success(r.json())
        except Exception as e:
            st.error(f"Health error: {e}")



if "messages" not in st.session_state:
    st.session_state["messages"] = []

for i, m in enumerate(st.session_state["messages"]):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant":
            feedback = m.get("feedback", None)
            st.session_state[f"feedback_{i}"] = feedback
            st.feedback(
                "thumbs",
                key=f"feedback_{i}",
                disabled=feedback is not None,
                on_change=save_feedback,
                args=[i],
            )


prompt = st.chat_input("Постав питання (наприклад: Виведи топ-10 найпопулярніших марок авто)")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        resp = requests.post(f"{backend_url}/ask", json={"question": prompt}, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("answer", "")
        sql = data.get("sql", "")
        rows_preview = data.get("rows_preview", [])
        total_rows = data.get("total_rows", 0)

        with st.chat_message("assistant"):
            st.markdown(answer)

            with st.expander("Generated SQL"):
                st.code(sql, language="sql")
                st.write(f"Total rows: {total_rows}")

            if rows_preview:
                st.subheader("Rows preview")
                st.dataframe(pd.DataFrame(rows_preview), use_container_width=True)

            st.feedback(
                "thumbs",
                key=f"feedback_{len(st.session_state['messages'])}",
                on_change=save_feedback,
                args=[len(st.session_state["messages"])],
            )

        st.session_state["messages"].append({"role": "assistant", "content": answer})

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"Request failed: {e}")
        st.session_state["messages"].append({"role": "assistant", "content": f"{e}"})


with st.sidebar:
    st.header("Upload data")
    fmt_choice = st.radio("Format", ["auto", "csv", "excel"], horizontal=True)
    sheet_name = st.text_input("Excel sheet name")
    sep = st.text_input("CSV separator (optional, e.g. ;)", value="")
    encoding = st.text_input("CSV encoding (optional, e.g. utf-8, cp1251)", value="")

    uploaded = st.file_uploader("Choose CSV or Excel", type=["csv", "xlsx", "xls"])
    if uploaded and st.button("Upload & replace table"):
        try:
            files = {"file": (uploaded.name, uploaded.getvalue(), "application/octet-stream")}
            data = {}
            if fmt_choice != "auto":
                data["fmt"] = fmt_choice
            if sheet_name:
                data["sheet_name"] = sheet_name
            if sep:
                data["sep"] = sep
            if encoding:
                data["encoding"] = encoding

            r = requests.post(f"{backend_url}/upload", files=files, data=data, timeout=120)
            r.raise_for_status()
            info = r.json()
            st.success(f"Uploaded: {info.get('format')} | rows={info.get('rows')} | columns={info.get('columns')}")
        except Exception as e:
            st.error(f"Upload failed: {e}")
