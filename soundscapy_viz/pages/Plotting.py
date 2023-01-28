import streamlit as st
import pandas as pd
import numpy as np
import soundscapy as sspy
from soundscapy import isd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

@st.cache
def load_data(version='latest'):
    return isd.load_isd_dataset(version)

st.markdown("# Plotting")
st.sidebar.markdown("# Plotting")

# Create a text element and let the reader know the data is loading
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe
data = load_data().copy()
# Notify the reader that the data was successfully loaded
data_load_state.text('Done! (using st.cache)')

# Inputs and options
# Sidebar
with st.sidebar:
    plot_type = st.selectbox(
        'Type of plot:',
        ['Density', 
         'Scatter', 
        #  'Jointplot'
         ],
    )

    location_select = st.multiselect(
        'Select some locations to look at:',
        data.LocationID.unique(),
        data.LocationID.unique()[0:2]
    )

    density_type = st.radio(
        'Density plot type',
        ('simple', 'full')
    )

    title = st.text_input('Plot title', 'Soundscapy Density plot')

    scatter_size = st.number_input(
        'Scatter size', min_value=10, max_value=100, value=20
    )

    with st.expander("Extra options"):
        # legend = st.checkbox('Show Legend', value=True)
        incl_scatter = st.checkbox('Include scatter points', value=True)
        alpha = st.number_input('Transparency (alpha)', min_value=0.0, max_value=1.0, value=0.5)

# st.write('You selected:', options)

# Matplotlib plot
fig, ax = plt.subplots(figsize = (5, 5))

location_data = data.isd.filter_location_ids(location_select)

if plot_type == 'Density':
    location_data.isd.density(ax=ax, hue='LocationID', density_type=density_type, title=title, alpha=alpha, incl_scatter=incl_scatter, scatter_kwargs={'s': scatter_size})
elif plot_type == 'Scatter':
    location_data.isd.scatter(ax=ax, hue='LocationID', title=title, s=scatter_size)
# elif plot_type == 'Jointplot':
#     location_data.isd.jointplot(hue='LocationID', density_type=density_type, title=title, alpha=alpha, incl_scatter=incl_scatter)

st.pyplot(fig)