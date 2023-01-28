import streamlit as st
import pandas as pd
import numpy as np
import soundscapy as sspy
from soundscapy import isd


st.title("Soundscapy analysis of ISD")

@st.cache
def load_data(version='latest'):
    return isd.load_isd_dataset(version)

# Create a text element and let the reader know the data is loading
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe
data = load_data().copy()
# Notify the reader that the data was successfully loaded
data_load_state.text('Done! (using st.cache)')

# Inspect the raw data
# (use a button to toggle raw data)
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Draw a histogram
# Add a subheader just below the raw data section
st.subheader('Number of responses per location')
# generate a histogram that breaks down responses per location
hist_values = np.histogram(
    pd.factorize(data.LocationID)[0], bins=len(data.LocationID.unique()))[0]
# use st.bar_chart to draw the histogram
st.bar_chart(hist_values)

# Plot data on a map
loc_data = data[['latitude', 'longitude']].dropna()
st.subheader('Map of all locations')
st.map(loc_data)

