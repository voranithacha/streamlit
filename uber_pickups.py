import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
# import plotly.figure_factory as ff
import plotly.express as px

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
#data_load_state.text('Loading data...done!')
data_load_state.text("Done! (using st.cache_data)")

#data
# st.subheader('Raw data')
# st.write(data)
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

st.subheader('Map of all pickups')
st.map(data)
# hour_to_filter = 17
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

# exercise 
# 1. convert 2D map to 3D map using PyDeck
st.subheader('exercise')
st.text("1. convert 2D map to 3D map using PyDeck \n2. Use Data input")
st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=40.75,
            longitude=-73.98,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=data,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)

# 3. Use Selectbox
st.text("3. Use Selectbox")

option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"),
)

st.write("You selected:", option)

# 4. Use plotly (any charts)
st.text("4. Use plotly (any charts)")
fig = px.scatter(data, x="lon", y="lat", title="Uber Pickups")
st.plotly_chart(fig)



# 5. Click a button to increase the numbrt x in the following message, "This page has run x time"
st.text('Click a button to increase the numbrt x in the following message, "This page has run x time"')
st.button("Clear", type="primary")
X = 0
if st.button("Click"):
    X = X + 1
    st.write(f"This page has run {X} time(s)")

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")
