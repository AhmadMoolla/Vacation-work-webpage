from deta import Deta
import pandas as pd
import streamlit as st

class ProjDevDF:
    def __init__(self):
        self.db = st.session_state["detaConn"].Base("ProjectDeveloperRelation")
        self.loadDataframe()

    def loadDataframe(self):
        self.df = pd.DataFrame(self.db.fetch().items)

    def assignDev(self, email, projName, insightLevel):
        self.db.put({"devID":st.session_state["devdf"].getKey(email),"projID":st.session_state["projdf"].getKey(projName),"insight":insightLevel})
        self.loadDataframe()

    def getKey(self, email, projName):
        dev_id = st.session_state["devdf"].getKey(email)
        proj_id = st.session_state["projdf"].getKey(projName)
        return self.df.loc[(self.df.devID==dev_id)&(self.df.projID==proj_id),'key'].values[0]

#Returns a dataframe with the projects the dev is working on
    def getProjectsForDev(self, email):
        dev_id = st.session_state["devdf"].getKey(email)
        proj_dict = dict(zip(st.session_state["projdf"].getDataframe().key,st.session_state["projdf"].getDataframe().project_name))
        temp_df = (self.df.loc[(self.df.devID==dev_id)]).replace({"projID":proj_dict})
        return temp_df.rename(columns = {'projID':'project_name'}, inplace = False)

#Returns a dataframe with the devs working on the project      
    def getDevsOnProject(self,projName):
        proj_id = st.session_state["projdf"].getKey(projName)
        dev_dict = dict(zip(st.session_state["devdf"].getDataframe().key,st.session_state["devdf"].getDataframe().email))
        temp_df = (self.df.loc[(self.df.projID==proj_id)]).replace({"devID":dev_dict})
        return temp_df.rename(columns = {'devID':'dev_email'},inplace = False)

    def removeDev(self, email, projName):
        self.db.delete(self.getKey(email,projName))
        self.loadDataframe()

    def deleteDev(self,email):
        dev_id = st.session_state["devdf"].getKey(email)
        keys = self.df.loc[(self.df.devID==dev_id),'key'].values
        for key in keys:
            self.db.delete(key)
        self.loadDataframe()

    def deleteProj(self,projName):
        proj_id = st.session_state["projdf"].getKey(projName)
        keys = self.df.loc[(self.df.projID==proj_id),'key'].values
        for key in keys:
            self.db.delete(key)
        self.loadDataframe()

    def getBusFactor(self):
        df = pd.DataFrame(columns= ['Projects', 'Highly Familiar', 'Somewhat Familiar'])
        project_list = st.session_state["projdf"].getProjectList()
        for i in range(len(project_list)):
            df = df.append({'Projects':project_list[i], 
                'Highly Familiar':len(self.df[(self.df['projID'] == st.session_state["projdf"].getKey(project_list[i]))&(self.df['insight'] == 'highly familiar')]),
                'Somewhat Familiar':len(self.df[(self.df['projID'] == st.session_state["projdf"].getKey(project_list[i]))&(self.df['insight'] == 'somewhat familiar')])}, ignore_index = True)
        return df

