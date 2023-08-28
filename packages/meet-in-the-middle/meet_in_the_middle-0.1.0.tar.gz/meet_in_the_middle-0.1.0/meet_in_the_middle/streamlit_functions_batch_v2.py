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
from collections import defaultdict

google_api_key = "AIzaSyAaCdN1Y8ov6R7mkhjSI4cDMmYRAoGdfzI"


def flat_earth_calculate_center(postcodes):
    total_lat = 0
    total_lon = 0
    coordinates = {}
    nomi = pgeocode.Nominatim("gb")
    for user in postcodes:
        lat, lon = (
            nomi.query_postal_code(postcodes[user])["latitude"],
            nomi.query_postal_code(postcodes[user])["longitude"],
        )
        total_lat += lat
        total_lon += lon
        coordinates[user] = f"{lat},{lon}"
    num_coords = len(coordinates)

    center_lat = total_lat / num_coords
    center_lon = total_lon / num_coords
    midpoint = f"{center_lat}, {center_lon}"

    return midpoint, coordinates


def places_around_point(midpoint, radius, type):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={midpoint}&radius={radius}&type={type}&key={google_api_key}"
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
    return clean_places


def meetinthemiddle(postcodes, type, radius):
    # converting postcodes to long/lat
    midpoint, coordinates = flat_earth_calculate_center(postcodes)
    # get list of places around midpoint
    st.text(f"Finding nearby {type}s")
    # print(f'Finding nearby {type}s')
    clean_places = places_around_point(midpoint, radius, type)
    # origin_a to place journeys
    # st.text('Calculating your journey times')
    durations = []
    raw_journeys = {}
    for user in coordinates:
        st.text(f"Calculating user {user}'s journey times")
        # print(f"Calculating user {user}'s journey times")
        duration_dict = {}
        user_durations = {}
        journey_dict = {}
        for place in clean_places:
            url = f"https://maps.googleapis.com/maps/api/directions/json?origin={coordinates[user]}&destination=place_id:{place['place_id']}&mode=transit&key={google_api_key}"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            duration_dict[place["name"]] = response.json()["routes"][0]["legs"][0][
                "duration"
            ]["value"]
            journey_dict[place["name"]] = response.json()["routes"][0]["legs"][0]

        user_durations[user] = duration_dict
        durations.append(user_durations)
        raw_journeys[user] = journey_dict

    # Initialize the dictionary to store the journey times
    places_journey_times = defaultdict(int)

    # Loop through the durations list and accumulate the journey times
    num_users = len(durations)
    for user in durations:
        user_data = next(iter(user.values()))
        for place, duration in user_data.items():
            places_journey_times[place] += duration

    # Calculate the average journey time for each place
    for place, total_duration in places_journey_times.items():
        average_duration = round(total_duration / num_users)
        places_journey_times[place] = average_duration

    # Convert the defaultdict to a regular dictionary if needed
    places_journey_times = dict(places_journey_times)

    if len(places_journey_times) > 0:
        final_place = min(places_journey_times, key=places_journey_times.get)
        final_time = np.ceil(min(places_journey_times.values()) / 60)
        times = {}
        for user in durations:
            for key in user.keys():
                times[key] = user[key][final_place]
        # print(times)
        place_dict = {}
        for place in clean_places:
            place_dict[place["name"]] = {
                "location": place["location"],
                "rating": place["review"],
                "address": place["address"],
                "place_id": place["place_id"],
            }

        place_df = pd.DataFrame.from_dict(place_dict, orient="index")
        place_df["lat"] = place_df["location"].apply(lambda x: x.get("lat"))
        place_df["lon"] = place_df["location"].apply(lambda x: x.get("lng"))
    else:
        final_place = "N/A"
        final_time = "N/A"
        times = "N/A"
        place_df = "N/A"

    return (final_place, final_time, times, place_df, len(clean_places), raw_journeys)
