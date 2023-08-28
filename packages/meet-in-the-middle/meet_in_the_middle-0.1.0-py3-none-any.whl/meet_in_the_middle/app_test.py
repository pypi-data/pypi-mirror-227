import streamlit as st
from test_streamlit import meetinthemiddle
import pandas as pd
import pgeocode

st.title("TESTING")

data = pd.read_csv("./../data/bdx_files/zego_20230710.csv")

st.text(data.head(10))

origin_a = "n22 5dj"
origin_b = "e5 0bb"
type = "bar"
keyword = "pub"
radius = "500"

nomi = pgeocode.Nominatim("gb")

lat1, lon1 = (
    nomi.query_postal_code(origin_a)["latitude"],
    nomi.query_postal_code(origin_a)["longitude"],
)

st.text(lat1)

data = meetinthemiddle(origin_a, origin_b, type, keyword, radius)
st.text(data)
