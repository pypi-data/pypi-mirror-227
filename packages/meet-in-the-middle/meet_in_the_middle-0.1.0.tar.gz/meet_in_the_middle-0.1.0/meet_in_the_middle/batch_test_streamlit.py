import pandas as pd
import numpy as np
import requests
import json
import datetime
from geographiclib.geodesic import Geodesic
import pgeocode
import streamlit as st
import plotly.express as px
from streamlit_plotly_events import plotly_events

google_api_key = "AIzaSyAaCdN1Y8ov6R7mkhjSI4cDMmYRAoGdfzI"

def meetinthemiddle(origin_a, origin_b, type, keyword, radius):
    # converting postcodes to long/lat
    nomi = pgeocode.Nominatim("gb")
    lat1, lon1 = (
        nomi.query_postal_code(origin_a)["latitude"],
        nomi.query_postal_code(origin_a)["longitude"],
    )
    lat2, lon2 = (
        nomi.query_postal_code(origin_b)["latitude"],
        nomi.query_postal_code(origin_b)["longitude"],
    )
    origin_a_final = f"{lat1},{lon1}"
    origin_b_final = f"{lat2},{lon2}"

    ## Compute the midpoint
    l = Geodesic.WGS84.InverseLine(lat1, lon1, lat2, lon2)
    m = l.Position(0.5 * l.s13)
    midpoint = f"{m['lat2']},{m['lon2']}"

    # get list of places around midpoint
    st.text(f'Finding nearby {type}s')
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={midpoint}&radius={radius}&type={type}&keyword={keyword}&key={google_api_key}"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    places = response.json()["results"]
    clean_places = []
    for place in places:
        place_details = {}
        place_details["name"] = place["name"]
        place_details["location"] = place["geometry"]["location"]
        try:
            place_details["review"] = place["rating"]
        except:
            place_details["review"] = 0
        try:
            place_details["address"] = place["vicinity"]
        except:
            place_details["address"] = "N/A"
        place_details["place_id"] = place["place_id"]
        clean_places.append(place_details)

    # origin_a to place journeys
    st.text('Calculating your journey times')
    duration_dict_a = {}
    for place in clean_places:
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_a_final}&destination=place_id:{place['place_id']}&mode=transit&key={google_api_key}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        duration_dict_a[place["name"]] = response.json()["routes"][0]["legs"][0][
            "duration"
        ]["value"]

    # origin_b to place journeys
    st.text("Calculating your friend's journey times")
    duration_dict_b = {}
    for place in clean_places:
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin_b_final}&destination=place_id:{place['place_id']}&mode=transit&key={google_api_key}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        duration_dict_b[place["name"]] = response.json()["routes"][0]["legs"][0][
            "duration"
        ]["value"]

    avg_duration = {}
    for k in duration_dict_a.keys():
        avg_duration[k] = (duration_dict_a[k] + duration_dict_b[k]) / 2

    if len(avg_duration) > 0:
        final_place = min(avg_duration, key=avg_duration.get)
        final_time = np.ceil(min(avg_duration.values()) / 60)
        a_time = duration_dict_a[final_place]
        b_time = duration_dict_b[final_place]
        place_dict = {}
        for place in clean_places:
            place_dict[place['name']] = {'location':place['location'], 'rating':place['review'], 'address':place['address'], 'place_id':place['place_id']}

        place_df = pd.DataFrame.from_dict(place_dict, orient = 'index')
        place_df['lat'] = place_df['location'].apply(lambda x: x.get('lat'))
        place_df['lon'] = place_df['location'].apply(lambda x: x.get('lng'))
    else:
        final_place = 'N/A'
        final_time = 'N/A'
        a_time = 'N/A'
        b_time = 'N/A'
        place_df = 'N/A'
    
    # final_place = min(avg_duration, key=avg_duration.get)
    # final_time = np.ceil(min(avg_duration.values()) / 60)
    # a_time = duration_dict_a[final_place]
    # b_time = duration_dict_b[final_place]
    # df = pd.DataFrame()

    # place_dict = {}
    # for place in clean_places:
    #     place_dict[place['name']] = {'location':place['location'], 'rating':place['review'], 'address':place['address'], 'place_id':place['place_id']}

    # place_df = pd.DataFrame.from_dict(place_dict, orient = 'index')
    # place_df['lat'] = place_df['location'].apply(lambda x: x.get('lat'))
    # place_df['lon'] = place_df['location'].apply(lambda x: x.get('lng'))
    


    return (
        # avg_duration,
        final_place,
        final_time,
        a_time,
        b_time,
        place_df,
        len(clean_places)
    )


def flat_earth_calculate_center(postcodes):
    total_lat = 0
    total_lon = 0
    coordinates = []
    nomi = pgeocode.Nominatim('gb')
    for postcode in postcodes:
        lat, lon = nomi.query_postal_code(postcode)['latitude'], nomi.query_postal_code(postcode)['longitude']
        coordinates.append((lat,lon))
    num_coords = len(coordinates)

    for lat, lon in coordinates:
        total_lat += lat
        total_lon += lon

    center_lat = total_lat / num_coords
    center_lon = total_lon / num_coords

    return center_lat, center_lon