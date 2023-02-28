import streamlit as st
import functions

st.set_page_config(page_title="Bus Factor - Manage Devs")

functions.add_logo()
functions.refresh_page()

if st.session_state["isAdmin"]:

    AddProj, DeleteProj = st.tabs(["Add a new project", "Remove an existing project"])

    with AddProj:
        st.header("Enter the project information below.")
        proj_name = st.text_input("Project name:")
        
        if st.button("Add new project."):
            try:
                st.session_state["projdf"].addProject(proj_name)
                st.success(proj_name+" added successfully")
            except:
                st.error("Error")

    with DeleteProj:
        sel_project = st.selectbox("Select a project.",st.session_state["projdf"].getProjectList())

        if st.button("Delete "+sel_project):
            try:
                st.session_state["projdf"].deleteProject(sel_project)
                st.success(sel_project+" successfully deleted.")
            except:
                st.error("Error")

else:
    st.error("You need to be signed in as an administrator to access this page.")
    st.write("Click on the '🧑‍💼 Sign in as Admin' tab to sign in.")
            
        



