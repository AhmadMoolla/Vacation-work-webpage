import streamlit as st
from deta import Deta
import DeveloperDataframe
import ProjectDataframe
import ProjectDeveloperRelation


def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://pbs.twimg.com/profile_images/1514206731227869190/5VYyzOKJ_400x400.jpg);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
                background-size: 90% 37%;
            }
            [data-testid="stSidebarNav"]::before {
                content: "Helm - Bus Factor";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 40px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def refresh_page():
    if "isAdmin" not in st.session_state:
        st.session_state["isAdmin"] = False

    if "detaConn" not in st.session_state:
        st.session_state["detaConn"] = Deta("d0vdc3mo_evipcVAc4PFGDpQidEZ63MM1tMKhVGDw")
    
    if "devdf" not in st.session_state:
        st.session_state["devdf"] = DeveloperDataframe.DevDF()

    if "projdf" not in st.session_state:
        st.session_state["projdf"] = ProjectDataframe.ProjDF()

    if "relationdf" not in st.session_state:
        st.session_state["relationdf"] = ProjectDeveloperRelation.ProjDevDF()
