import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import functions

st.set_page_config(page_title="Bus Factor - Assign Devs")

functions.add_logo()
functions.refresh_page()

if st.session_state["isAdmin"]:

    AssignDev, RemoveDev = st.tabs(["Assign a dev to a project", "Remove a dev from a project"])

    with AssignDev:
        #Select box to select devs
        email = st.selectbox("Select a developer.",st.session_state["devdf"].getEmailList(),key=0)

        #Select box for projects
        res = filter(lambda i: i not in st.session_state["relationdf"].getProjectsForDev(email).project_name.values.tolist(), st.session_state["projdf"].getProjectList())
        try:
            sel_project = st.selectbox("Select a project. Only projects that "+st.session_state["devdf"].getFullname(email)+" is not already a part of are shown.",res,key=1)
            insightLevel = st.selectbox("Select the level of insight that "+st.session_state["devdf"].getFullname(email)+" has on "+sel_project,["highly familiar","somewhat familiar"],key=19)
            #button to add dev to project
            if st.button("Add "+st.session_state["devdf"].getFullname(email)+" to "+sel_project):
                #insert data
                try: 
                    st.session_state["relationdf"].assignDev(email,sel_project,insightLevel)
                    st.success(st.session_state["devdf"].getFullname(email) + " added to " + sel_project)
                except:
                    st.error("Error")
        except:
            st.error(st.session_state["devdf"].getFullname(email)+" is already on all projects")

    with RemoveDev:
        #Select box to select devs
        email = st.selectbox("Select a developer.",st.session_state["devdf"].getEmailList(),key=2)

        try:
            #Select box for projects
            sel_project = st.selectbox("Select a project. Only projects that "+st.session_state["devdf"].getFullname(email)+" is a part of are shown.",st.session_state["relationdf"].getProjectsForDev(email).project_name.values.tolist(),key=3)

            if st.button("Remove "+st.session_state["devdf"].getFullname(email)+" from "+sel_project):
                try:
                    st.session_state["relationdf"].removeDev(email,sel_project)
                    st.success(st.session_state["devdf"].getFullname(email)+" was removed from "+sel_project)
                except:
                    st.error("Error")
        except:
            st.error(st.session_state["devdf"].getFullname(email)+" is not on any projects yet.")

else:
    st.error("You need to be signed in as an administrator to access this page.")
    st.write("Click on the '🧑‍💼 Sign in as Admin' tab to sign in.")




        

    