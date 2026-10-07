import streamlit as st

st.title("📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Interviews", "0")

with col2:
    st.metric("Average Score", "0")

with col3:
    st.metric("ATS Matches", "0")

with col4:
    st.metric("Questions Practiced", "0")

st.info("Analytics will appear here in later phases.")