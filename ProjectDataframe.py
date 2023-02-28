from deta import Deta
import pandas as pd
import streamlit as st

class ProjDF:

    def __init__(self):
        #Load dev table into pandas data frame
        self.db = st.session_state["detaConn"].Base("Project")
        self.loadDataframe()

    def loadDataframe(self):
        self.df = pd.DataFrame(self.db.fetch().items)

    def getKey(self,name):
        return self.df.loc[self.df.project_name == name,'key'].values[0]    
    
    def addProject(self,name):
        if name in self.df['project_name'].values:
            st.error('Project already exists')
            raise
        if not name == "":
            self.db.put({"project_name":name})
            self.loadDataframe()
        else:
            st.error("Project name cannot be blank.")
            raise

    def deleteProject(self,name):
        st.session_state["relationdf"].deleteProj(name)
        self.db.delete(self.getKey(name))
        self.loadDataframe()

    def getProjectList(self):
        return self.df.project_name.tolist()    

    def getProjectName(self,projID):
        return self.df.loc[self.df.key == projID,'project_name'].values[0]

    def getDataframe(self):
        return self.df
    
