import streamlit as st
import functions

st.set_page_config(page_title="Bus Factor - Sign in")

functions.add_logo()
functions.refresh_page()

st.header("Sign in as an administrator to edit projects and developers.")

if st.session_state["isAdmin"] == False:
    username = st.text_input("Enter your email address here.")
    password = st.text_input("Enter your password here.",type="password")
    isAdmin = False
    
    if st.button("Sign in as administrator."):
        try:
            isAdmin = st.session_state["devdf"].getAdminState(username)
        except:
            st.error("Invalid email address")

        if isAdmin:
            if st.session_state["devdf"].validatePassword(username,password):
                st.session_state['isAdmin'] = True
                st.experimental_rerun()
            else:
                st.error('Invalid password')
        else:
            st.error('User is not an admin.')
        
else:
    st.success("You are currently signed in as an administrator")