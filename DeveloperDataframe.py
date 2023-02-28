from deta import Deta
import functions as func
import pandas as pd
import streamlit as st
import bcrypt

class DevDF:
    
    def __init__(self):
        #Load dev table into pandas data frame
        self.db = st.session_state["detaConn"].Base("Developer")
        self.loadDataframe()
        
    def loadDataframe(self):
        self.df = pd.DataFrame(self.db.fetch().items)

    def validateInputs(self,name,surname,email,isAdmin,password):
        isValid = True
        if name == "": 
            isValid = False
            st.error("First name cannot be blank.")
        if surname == "": 
            isValid = False
            st.error("Surname cannot be blank.")
        if email == "":
            isValid = False
            st.error("Email cannot be blank.")
        if "@" not in email:
            isValid = False
            st.error("Enter a valid email address.")
        if isAdmin and password == "":
            isValid = False
            st.error("Password cannot be blank if user is an admin.")
            
        return isValid
    
    def isEmailUnique(self,email):
        return not(email in self.df['email'].values)

    def addDev(self,name,surname,email,isAdmin,password):
        isValid = self.validateInputs(name,surname,email,isAdmin,password)
        if not(self.isEmailUnique(email)):
            st.error("A user with the email adress "+email+" already exists. Dev not added.")
            raise
        
        if isValid:
            if isAdmin:
                hashpw = self.getPWHash(password)
            else:
                hashpw = ""
            self.db.put({"name":name,"surname":surname,"email":email,"admin":isAdmin,"password":hashpw})
            self.loadDataframe()

    def getKey(self,email):
        return self.df.loc[self.df.email==email,'key'].values[0]
    
    def deleteDev(self,email):
        st.session_state["relationdf"].deleteDev(email)
        self.db.delete(self.getKey(email))
        self.loadDataframe()
        
    def getFullname(self,email):
        return self.getColVal("name",self.getKey(email)) + " " + self.getColVal("surname",self.getKey(email))

    def getEmailList(self):
        return self.df.email.values.tolist()

    def getDataframe(self):
        return self.df

    def getPWHash(self,password):
        return bcrypt.hashpw(password.encode('ascii'), bcrypt.gensalt()).decode('ascii')

    def getColVal(self,column,keyVal):
        return self.df.loc[(self.df.key==keyVal),column].values[0]
    
    def updateDev(self,name,surname,email,isAdmin,password,alreadyAdmin,key):
        #Do not change password if user is already an admin and no new password was supplied.
        if alreadyAdmin and password == "" and isAdmin:
            password = "SoValidationTestPasses"
            hashpw = self.getColVal("password",key)
            isValid = self.validateInputs(name, surname, email,isAdmin, password)
            password = ""
        #User is admin and new password was supplied - doesn't matter if they're already an admin
        if (not password == "") and isAdmin:
            isValid = self.validateInputs(name, surname, email,isAdmin, password)
            hashpw = self.getPWHash(password)
        #User is not or no longer an admin
        if isAdmin == False:
            isValid = self.validateInputs(name, surname, email,isAdmin, password)
            hashpw = ""  
        
        if isValid:
            self.db.put({"name":name,"surname":surname,"email":email,"admin":isAdmin,"password":hashpw},key)
            self.loadDataframe()

    def getAdminState(self,email):
        key = self.getKey(email)
        return self.getColVal("admin",key)

    def validatePassword(self,email,password):
        key = self.getKey(email)
        storedHash = self.getColVal("password",key).encode('ascii')
        return bcrypt.checkpw(password.encode('ascii'),storedHash)

    def getDevInfo(self,email):
        return self.df.loc[(self.df['email'] == email)][['name','surname','email','admin']]




        
        
        






