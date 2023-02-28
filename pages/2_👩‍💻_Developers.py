import streamlit as st
import pandas as pd
import functions

st.set_page_config(page_title="Bus Factor - Devs")

functions.add_logo()
functions.refresh_page()

#Select box to select devs
email = st.selectbox("Select a developer to view the projects that they're working on",st.session_state["devdf"].getEmailList(),key=11)
st.dataframe(st.session_state["devdf"].getDevInfo(email))

#display the projects that the developers are working on
st.write(st.session_state["devdf"].getFullname(email)+" is part of the projects shown below.")
st.dataframe(st.session_state["relationdf"].getProjectsForDev(email)[["project_name","insight"]])

#Checkbox to display all the devs
if st.checkbox('Show all developers.'):
    st.dataframe(st.session_state["devdf"].getDataframe()[["name","surname","email","admin"]])

