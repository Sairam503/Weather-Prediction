import streamlit as st
import pandas as pd
from datetime import datetime

# Load data
df = pd.read_csv("./processed_weather_data.csv")

# Safely create a datetime column
def safe_datetime(row):
    try:
        return datetime(2025, int(row['Month']), int(row['Day']), int(row['Hour']))
    except ValueError:
        return pd.NaT  # Not a Time (missing value)

df['datetime'] = df.apply(safe_datetime, axis=1)

# Drop invalid rows
df = df.dropna(subset=['datetime'])

# Extract date and time for filters
df['date_only'] = df['datetime'].dt.date
df['time_only'] = df['datetime'].dt.time

# Sidebar filters
st.sidebar.header("🔍 Filter Selection")

states = sorted(df['State'].unique())
selected_state = st.sidebar.selectbox("Select State", states)

dates = sorted(df[df['State'] == selected_state]['date_only'].unique())
selected_date = st.sidebar.selectbox("Select Date", dates)

times = sorted(df[(df['State'] == selected_state) & (df['date_only'] == selected_date)]['time_only'].unique())
selected_time = st.sidebar.selectbox("Select Time", times)

# Filtered Data
filtered_df = df[
    (df['State'] == selected_state) &
    (df['date_only'] == selected_date) &
    (df['time_only'] == selected_time)
]

# Display data
st.subheader("📄 Filtered Weather Data")
st.dataframe(filtered_df)

st.subheader(f"🌡️ Temperature Trend on {selected_date} in {selected_state}")
temp_day = df[(df['State'] == selected_state) & (df['date_only'] == selected_date)]
st.line_chart(temp_day.set_index('datetime')['Temperature'])

st.subheader("📊 Summary Statistics")
st.write(filtered_df.describe())

st.subheader("🌈 Weather Type")
if not filtered_df.empty:
    st.write(f"**Weather:** {filtered_df.iloc[0]['WeatherType']}")
else:
    st.write("No weather data for this selection.")

st.subheader("⬇️ Download Filtered Data")
st.download_button(
    label="Download as CSV",
    data=filtered_df.to_csv(index=False),
    file_name=f"weather_{selected_state}_{selected_date}_{selected_time}.csv",
    mime="text/csv"
)
