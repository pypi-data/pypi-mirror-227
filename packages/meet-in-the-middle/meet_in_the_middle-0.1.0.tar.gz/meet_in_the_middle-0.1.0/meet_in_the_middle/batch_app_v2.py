import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import datetime
from geographiclib.geodesic import Geodesic
import pgeocode
import time
from streamlit_functions_batch_v2 import (
    meetinthemiddle,
    flat_earth_calculate_center,
    places_around_point,
)
import plotly.express as px
from streamlit_plotly_events import plotly_events
from collections import defaultdict


st.title("Meet In The Middle - V0.0.0.0.0.0.1")

user_number = st.slider("How many people are meeting?", 2, 5)
postcodes = {}

for user in range(0, user_number):
    postcodes[chr(ord("`") + user + 1)] = st.text_input(
        f"Where is user {user+1} coming from? (postcode)"
    )  ## should probably get rid of this weird converting an integer to a letter to use as the key

# postcodes["a"] = st.text_input("Where are you? (postcode)")
# postcodes["b"] = st.text_input("Where is your friend? (postcode)")
radius = st.text_input(
    "What radius around the midpoint would you like to search (in metres)? Lower radius = quicker results"
)
type = st.selectbox(
    "Where do you want to go?",
    ("bar", "cafe", "movie_theater", "night_club", "park", "restaurant"),
)
ready = st.button("Ready?")

with st.expander("Debug"):
    user_number
    postcodes
    radius


if ready:
    start_time = time.time()
    with st.spinner("Calculating journey times..."):
        data = meetinthemiddle(postcodes, type, radius)
    if data[4] == 0:
        st.success(f"No locations found, try expanding your radius")
    else:
        st.success(
            f"Checked journeys for {data[4]} {type}s in {round((time.time() - start_time),2)} seconds"
        )
        # st.text("Calculating journey times...")
        ##data = meetinthemiddle(origin_a, origin_b, type, keyword, radius)
        # st.text(f"{time.time() - start_time} to check journeys for {data[5]} pubs")
        st.title(f"The best {type} to Meet in the Middle is: {data[0]}")
        time.sleep(1)
        st.title(f"with an average journey time of {data[1]} mins")
        time.sleep(0.5)
        fig = px.scatter_mapbox(
            data[3],
            lat="lat",
            lon="lon",
            hover_name=data[3].index,
            zoom=13,
            color="rating",
            size="rating",
            size_max=20,
            color_continuous_scale="blues",
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        plotly_events(fig)
        ##st.plotly_chart(fig)
        time.sleep(1)
        for k, v in data[2].items():
            st.text(f"User {k}'s journey time is approximately {np.ceil(v/60)} mins")
            with st.expander(f"User {k}'s journey"):
                for step in data[5][k][data[0]]["steps"]:
                    if step["travel_mode"] == "WALKING":
                        st.text(
                            f"{step['duration']['text']} - {step['html_instructions']}"
                        )
                    else:
                        st.text(
                            f"{step['duration']['text']} - {step['transit_details']['line']['short_name']} {step['transit_details']['line']['vehicle']['name']} from {step['transit_details']['departure_stop']['name']} to {step['transit_details']['arrival_stop']['name']}"
                        )
