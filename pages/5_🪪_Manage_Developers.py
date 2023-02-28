import streamlit as st
import functions

st.set_page_config(page_title="Bus Factor - Manage Devs")

functions.add_logo()
functions.refresh_page()

if st.session_state["isAdmin"]:
    AddDev, DeleteDev, ModDev = st.tabs(["Add a new dev", "Remove an existing dev","Edit an existing dev"])

    with AddDev:
        #Get developer information
        st.header("Please enter the details of the dev below.")
        first_name = st.text_input("First Name:")
        surname = st.text_input("Surname:")
        email = st.text_input("Helm email address:")
        if st.checkbox("Make admin"):
            isAdmin = True
            password = st.text_input("Enter a password")
        else:
            isAdmin = False
            password = ""

        #add developer
        if st.button("Add dev"):
            try:
                st.session_state["devdf"].addDev(first_name,surname,email,isAdmin,password)
                st.success(first_name + " " + surname + " added as a developer")
            except:
                st.error("Error, dev not added.")

    with DeleteDev:
        email = st.selectbox("Select a developer to remove from the organization.",st.session_state["devdf"].getEmailList(),key=4)

        #Delete
        if st.button("Delete "+st.session_state["devdf"].getFullname(email)+"."):
            try:
                fullname = st.session_state["devdf"].getFullname(email)
                st.session_state["devdf"].deleteDev(email)
                st.success(fullname+" was removed")
            except:
                st.error("Error")
    
    with ModDev:
        email = st.selectbox("Select a developer to edit.",st.session_state["devdf"].getEmailList(),key=5)
        st.write("Modify "+st.session_state["devdf"].getFullname(email))
        key = st.session_state["devdf"].getKey(email)
        
        #store current details - set them as placeholders for text inputs
        firstname = st.text_input("First name:",placeholder=st.session_state["devdf"].getColVal("name",key))        
        lastname = st.text_input("Surname:",placeholder=st.session_state["devdf"].getColVal("surname",key))
        old_email = st.session_state["devdf"].getColVal("email",key)
        email_address = st.text_input("Email address:",placeholder=old_email)
        alreadyAdmin = st.session_state["devdf"].getColVal("admin",key)
        
        if st.checkbox('Make administrator', value=alreadyAdmin):
            makeAdmin = True
            if alreadyAdmin:
                password = st.text_input("Enter a new password for "+st.session_state["devdf"].getFullname(email)+". If you leave this field blank their original password will remain.")
            else:
                password = st.text_input("Enter a new password for "+st.session_state["devdf"].getFullname(email))
        else:
            makeAdmin = False

        if st.button("Update"):
            #set placeholders as inputs bcs streamlit sees them as being blank
            if firstname == "": firstname = st.session_state["devdf"].getColVal("name",key)
            if lastname == "": lastname = st.session_state["devdf"].getColVal("surname",key)
            if email_address == "": email_address = old_email
         
            try:
                st.session_state["devdf"].updateDev(firstname,lastname,email_address,makeAdmin,password,alreadyAdmin,key)
                st.success(firstname + " " + lastname + " modified.")
            except:
                st.error("Error, dev not updated.")

else:
    st.error("You need to be signed in as an administrator to access this page.")
    st.write("Click on the '🧑‍💼 Sign in as Admin' tab to sign in.")