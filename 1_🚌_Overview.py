import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import functions 

st.set_page_config(page_title="Bus Factor - Home")

functions.add_logo()
functions.refresh_page()

st.title("Bus Factor")
st.write("Bus factor is the number of people that need to be hit by a bus for a project to be compromised :|.")

barChart = st.session_state["relationdf"].getBusFactor().plot(x='Projects', kind='bar', stacked=True, title='Busfactor').figure
st.pyplot(barChart)

if st.checkbox("Show bus factor data."):
    st.dataframe(st.session_state["relationdf"].getBusFactor())