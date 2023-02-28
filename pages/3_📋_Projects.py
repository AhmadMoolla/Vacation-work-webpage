import streamlit as st
import pandas as pd
import functions

st.set_page_config(page_title="Bus Factor - Projects")

functions.add_logo()
functions.refresh_page()

sel_project = st.selectbox("Select a project to view which devs are working on it.",st.session_state["projdf"].getProjectList())
st.write("The developers working on "+sel_project+" are shown below.")
st.dataframe(st.session_state["relationdf"].getDevsOnProject(sel_project)[["dev_email","insight"]])

if st.checkbox('View all projects.'):
    st.dataframe(st.session_state["projdf"].getDataframe()[["project_name"]])