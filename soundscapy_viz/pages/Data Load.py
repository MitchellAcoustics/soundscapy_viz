import streamlit as st
import pandas as pd
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

import numpy as np
import soundscapy as sspy
from soundscapy import isd
from datetime import datetime

# Functions
@st.cache(allow_output_mutation=True)
def load_data(source, version='latest'):
    if source == "ISD":
        return isd.load_isd_dataset(version)
    elif source == "SATP":
        # url = "https://zenodo.org/record/7143599/files/SATP%20Dataset%20v1.2.xlsx"
        # return pd.read_excel(url, engine='openpyxl')
        return st.write("Whoops, SATP not yet supported")
    elif source == "ARAUS":
        return st.write("Whoops, ARAUS not yet supported")
    
@st.cache(allow_output_mutation=True)
def gen_profile_report(df, *report_args, **report_kwargs):
    pr = ProfileReport(df, *report_args, **report_kwargs)
    return pr

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

# Intro text
st.title("Explore one of our datasets or load your own data")

st.markdown("`soundscapy` was built to work with soundscape survey data. We make it super simple to load up and explore a few supported datasets.")
st.markdown("Simply select which dataset you'd like to explore and we'll automatically load it for you.")
st.markdown("But, that's not all! You don't just have to use one of our supported datasets! You can also load in your own data and create some lovely soundscapy-style plots. Just scroll on down to the `load your data` button.")
st.markdown("---")

# Sidebar elements
with st.sidebar:
    data_source = st.selectbox('Select Dataset', ('ISD', 'ARAUS', 'SATP'))

    uploaded_file = st.file_uploader("Load own data (.xlsx or .csv)", type=(["csv", "xlsx"]))

    # Load data source
    if data_source in ['ISD', 'SATP', 'ARAUS']:
        # Create a text element and let the reader know the data is loading
        # data_load_state = st.text('Loading data...')
        # Load data
        data = load_data(data_source)
        data = data.copy()
        # # Notify the reader that the data was successfully loaded
        # data_load_state.text('Check out the data:')    

    if uploaded_file is not None:
        path_in = uploaded_file.name
        if path_in.split(".")[-1] == "csv":
            data = pd.read_csv(uploaded_file)
        elif path_in.split(".")[-1] == "xlsx":
            data = pd.read_excel(uploaded_file)
        else:
            st.write(f"Can't recognise uploaded file type: {path_in}")

    validate = st.checkbox("Validate Dataset?", value=True)

    calc_isd = st.checkbox("Calculate ISO Coordinates?", value=True)

    paq_min = st.number_input("PAQ Min value", value=1, help="Let us know what the minimum allowed value for the PAQ responses is.")
    paq_max = st.number_input("PAQ Max value", value=5)
    paq_range = (paq_min, paq_max)


    with st.expander("Select columns"):
        show_cols = st.multiselect("Select columns", list(data.columns), list(data.columns))
        data = data[show_cols]

    with st.expander("Filters"):
        filter1 = st.text_input("`pd.query` command for filtering", "Empty", key="filter1")
        if filter1 != "Empty":
            try:
               data = data.query(filter1)
            except: 
                st.text("Sorry, formula error.")

        filter2 = st.text_input("`pd.query` command for filtering", "Empty", key="filter2")
        if filter2 != "Empty" and filter2 != "":
           data = data.query(filter2)

        filter3 = st.text_input("`pd.query` command for filtering", "Empty", key="filter3")
        if filter3 != "Empty":
           data = data.query(filter3)

        filter4 = st.text_input("`pd.query` command for filtering", "Empty", key="filter4")
        if filter4 != "Empty":
           data = data.query(filter4)

        filter5 = st.text_input("`pd.query` command for filtering", "Empty", key="filter5")
        if filter5 != "Empty":
           data = data.query(filter5)

    with st.expander("Rename PAQs"):
        st.write("Replace the PAQ labels if you need to rename them.")
        pleasant = st.text_input("pleasant", value='pleasant', label_visibility='collapsed')
        vibrant = st.text_input("vibrant", value='vibrant', label_visibility='collapsed')
        eventful = st.text_input("eventful", value='eventful', label_visibility='collapsed')
        chaotic = st.text_input("chaotic", value='chaotic', label_visibility='collapsed')
        annoying = st.text_input("annoying", value='annoying', label_visibility='collapsed')
        monotonous = st.text_input("monotonous", value='monotonous', label_visibility='collapsed')
        uneventful = st.text_input("uneventful", value='uneventful', label_visibility='collapsed')
        calm = st.text_input("calm", value='calm', label_visibility='collapsed')

    
    with st.expander("Extra options"):
        if st.checkbox("Remove all missing values?", value=False):
            data = data.dropna()

# Process data
try:
    # Execute the standard Soundscapy validation checks then return the data and excluded data frames
    if validate:
        data, excl_data = data.isd.validate_dataset(
            paq_aliases = [pleasant, vibrant, eventful, chaotic, annoying, monotonous, uneventful, calm],
            val_range=paq_range
            )
    else:
        data = load_data(data_source)
        data = data.copy()
        excl_data = None

    if calc_isd:
        if 'ISOPleasant' not in data.columns and 'ISOEventful' not in data.columns:
            data = data.isd.add_paq_coords(
                val_range=paq_range
                )

    st.subheader(data_source)

    st.markdown("Basic information about your data:")
    st.markdown(f"Number of observations: {data.shape[0]}")
    st.markdown(f"Number of columns     : {data.shape[1]}")

    tab1, tab2 = st.tabs(["Data", "Excluded data"])
    with tab1:

    
        st.dataframe(data)

        with st.expander("REPORT", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Generate Minimal Report"):
                    minimal=True
                    # pr = gen_profile_report(data, config_file="soundscapy_streamlit/config_minimal.yaml")   
                    pr = gen_profile_report(data, minimal=True)   
            with col2:
                if st.button("Generate FULL Report"):
                    pr = gen_profile_report(data)

            try:   
                st_profile_report(pr)
            except NameError:
                st.write("Waiting to generate a report.")

    with tab2:
        st.dataframe(excl_data)

    col1, col2 = st.columns(2)
    today = datetime.now()
    with col1:
        csv = convert_df(data)

        st.download_button(
            label = "Download Data", 
            data = csv, 
            file_name = f"{today.strftime('%Y-%m-%d_%H:%M')}_soundscapy_data.csv",
            mime='text/csv'
            )
        
    with col2:
        try:
            st.download_button(
                label = "Download Report",
                data = pr.to_html(),
                file_name = f"{today.strftime('%Y-%m-%d_%H:%M')}_soundscapy_report.html",
                mime='html'
            )
        except NameError:
            st.write('[Download Report]')
        

except NameError:
    st.write("Waiting for some data.")
except AttributeError:
    st.write("Waiting for some data.")