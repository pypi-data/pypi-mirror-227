import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import datetime
from geographiclib.geodesic import Geodesic
import pgeocode
import time
from batch_test_streamlit import meetinthemiddle
import plotly.express as px
from streamlit_plotly_events import plotly_events
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import pydeck as pdk

# st.title("Meet In The Middle - V0.0.0.0.0.0.1")

# origin_a = st.text_input("Where are you? (postcode)")
# origin_b = st.text_input("Where is your friend? (postcode)")
# radius = st.text_input(
#     "What radius would you like to search (in metres)? Lower radius = quicker results"
# )
# type = st.selectbox('Where do you want to go?', ('bar', 'cafe', 'movie_theater', 'night_club', 'park', 'restaurant'))
# keyword = ""

# ready = st.button("Ready?")

# if ready:
#     start_time = time.time()
#     with st.spinner('Calculating journey times...'):
#         data = meetinthemiddle(origin_a, origin_b, type, keyword, radius)
#     if data[5] == 0:
#         st.success(f"No locations found, try expanding your radius")
#     else:
#         st.success(f"Checked journeys for {data[5]} {type}s in {round((time.time() - start_time),2)} seconds")
#         #st.text("Calculating journey times...") 
#         ##data = meetinthemiddle(origin_a, origin_b, type, keyword, radius)
#         #st.text(f"{time.time() - start_time} to check journeys for {data[5]} pubs")
#         st.title(f"The best {type} to Meet in the Middle is: {data[0]}")
#         time.sleep(1)
#         st.title(f"with an average journey time of {data[1]} mins")
#         time.sleep(0.5)
#         fig = px.scatter_mapbox(data[4], lat="lat", lon="lon", hover_name=data[4].index, zoom=13, color = "rating", size = "rating", size_max = 20, color_continuous_scale='blues')
#         fig.update_layout(mapbox_style="open-street-map")
#         fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# # fig = px.line(x=[1], y=[1])
# # selected_points = plotly_events(fig)

# # with st.expander('Plot'):
# #     fig = px.line(x=[1], y=[1])
# #     selected_points = plotly_events(fig)

# # fig = px.line(x=[1,2], y=[1,2])
#         selected_points = plotly_events(fig, click_event=True, hover_event=False)
#         st.text(f'{selected_points}')

#ChatGPT test 2

def create_map():
    # Create a map centered at a specific location (e.g., London)
    map_center = [51.5074, -0.1278]  # London's latitude and longitude

    # Define the initial view state
    view_state = pdk.ViewState(
        latitude=map_center[0],
        longitude=map_center[1],
        zoom=10,
        pitch=0,
    )

    # Create the scatterplot layer without data for now
    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=[],
        get_position="[lon, lat]",
        get_radius=2000,
        radius_min_pixels=2,
        get_fill_color=[255, 140, 0],
    )

    # Create the deck (map)
    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        layers=[scatterplot_layer],
        map_provider="mapbox",
    )

    return deck

def main():
    st.title("Interactive Map with Click Events")

    # Create an empty list to store clicked locations
    clicked_locations = []

    # Render the initial map
    deck = create_map()
    st.pydeck_chart(deck)

    # Handle click events using Streamlit's "st.pydeck_chart" method
    # This will be triggered whenever a click event occurs on the map
    map_click = st.pydeck_chart(deck)
    if map_click:
        click_info = map_click["click_info"]
        if click_info is not None:
            lat, lon = click_info["lat"], click_info["lon"]
            clicked_locations.append((lon, lat))
            # Update the data on the map with clicked locations
            deck.layers[0].data = clicked_locations

    # Display the clicked locations as text on the Streamlit app
    st.write("Clicked Locations:")
    for lon, lat in clicked_locations:
        st.write(f"Latitude: {lat}, Longitude: {lon}")

if __name__ == "__main__":
    main()