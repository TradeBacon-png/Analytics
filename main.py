import numpy as np
import pandas as pd
import requests
import zipfile
import io
import streamlit as st

st.set_page_config(page_title="F1 Stats Pro", page_icon="🏎️", layout="wide")
drivers =['max-verstappen','fernando-alonso','kimi-antonelli', 'oliver-bearman','lando-norris','oscar-piastri']

file_url = "https://github.com/f1db/f1db/releases/download/v2026.3.0/f1db-csv.zip"
@st.cache_data
def get_f1_data(table):
    file=requests.get(file_url)
    with zipfile.ZipFile(io.BytesIO(file.content)) as z:
        with z.open(table) as x:
            return pd.read_csv(x, low_memory=False)

results = get_f1_data('f1db-races-race-results.csv')     
driver_choice = st.sidebar.selectbox("Select Driver", ["max-verstappen", "fernando-alonso", "lewis-hamilton", "kimi-antonelli"])
year_min = st.sidebar.number_input("Since the year", 1990, 2025, 2010)
display_name = driver_choice.replace('-', ' ').title()
wins_df = results[
    (results['driverId'] == driver_choice) & 
    (results['year'] >= year_min) & 
    (results['positionNumber'] == 1)]

st.title(f"{display_name} wins since {year_min}")

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Total Wins", len(wins_df))
    st.write(f"Showing wins since {year_min}")

with col2:
    if not wins_df.empty:
        chart_data = wins_df.groupby('year').size().reset_index(name='Wins')
        st.bar_chart(chart_data, x='year', y='Wins', color="#ff4b4b")
    else:
        st.info("No wins found for this period.")
st.write("### Win History")
st.dataframe(wins_df[['year', 'constructorId']].sort_values('year', ascending=False), use_container_width=True)

