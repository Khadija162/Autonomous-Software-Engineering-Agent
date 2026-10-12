import os
import requests
import streamlit as st

st.set_page_config(page_title="Software Engineering Agent", layout="wide")
st.title("Software Engineering Agent Control Center")
st.caption("Repository exploration → open-weight model proposal → human review → sandbox validation → draft PR")
st.warning("Read-only demonstration. This UI cannot apply changes, execute code, or open PRs.")
title = st.text_input("GitHub issue title", "Fix incorrect zero-value handling")
description = st.text_area("Issue description", "The function should accept zero as a valid input and return zero.")
if st.button("Investigate issue"):
    try:
        api = os.getenv("API_URL", "http://127.0.0.1:8000")
        result = requests.post(api + "/api/issues/analyze",
                               json={"title": title, "description": description},
                               timeout=120)
        result.raise_for_status()
        report = result.json()
        st.subheader("Relevant files")
        st.json(report["investigation"]["files"])
        st.subheader("Proposed approach")
        st.write(report["model"]["proposal"])
        st.info("Human approval is mandatory. No code has been executed.")
    except requests.RequestException as exc:
        st.error(str(exc))
