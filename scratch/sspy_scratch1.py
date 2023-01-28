#%%
import soundscapy as sspy
from soundscapy import isd
import numpy as np
import pandas as pd

#%%
data = isd.load_isd_dataset()

data.head()
# %%

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

uber_data = load_data(10000)

# %%

np.histogram(pd.factorize(data.LocationID)[0], bins=len(data.LocationID.unique()))[0]

# %%
