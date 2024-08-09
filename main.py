import streamlit as st

with open("styles.css") as file:
    CSS = file.read()

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

pg = st.navigation([
    st.Page("pages/serious.py", title="Serious", icon="⚡"),
    st.Page("pages/fun.py", title="Fun", icon="🔥"),
    st.Page("pages/insights.py", title="Insights", icon="☀️")
])
pg.run()