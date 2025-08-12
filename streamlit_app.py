# streamlit_app.py
import requests
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Reestr Q&A", layout="wide")
st.title("🚗 Reestr Q&A (FastAPI + DuckDB + LLM)")

# Налаштування бекенду
with st.sidebar:
    st.header("Backend settings")
    backend_url = st.text_input("FastAPI URL", value="http://127.0.0.1:8000")
    if st.button("Health check"):
        try:
            r = requests.get(f"{backend_url}/health", timeout=5)
            st.success(r.json())
        except Exception as e:
            st.error(f"Health error: {e}")

# Історія чату
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Рендер історії
for m in st.session_state["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Ввід питання
prompt = st.chat_input("Постав питання (наприклад: Виведи топ-10 найпопулярніших марок авто)")
if prompt:
    # показуємо юзерське повідомлення
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # викликаємо бекенд
    try:
        resp = requests.post(f"{backend_url}/ask", json={"question": prompt}, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        answer = data.get("answer", "")
        sql = data.get("sql", "")
        rows_preview = data.get("rows_preview", [])
        total_rows = data.get("total_rows", 0)

        # показуємо відповідь бота
        with st.chat_message("assistant"):
            st.markdown(answer)

            with st.expander("🔍 Generated SQL"):
                st.code(sql, language="sql")
                st.write(f"Total rows: {total_rows}")

            if rows_preview:
                st.subheader("Rows preview")
                st.dataframe(pd.DataFrame(rows_preview), use_container_width=True)

        st.session_state["messages"].append({"role": "assistant", "content": answer})

    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"Request failed: {e}")
        st.session_state["messages"].append({"role": "assistant", "content": f"❌ {e}"})
