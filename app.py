import streamlit as st
import pandas as pd
from datetime import datetime

# Title
st.title("🌦️ Weather Data Explorer")

# Load CSV
df = pd.read_csv("./processed_weather_data.csv")

# Create a datetime column manually from Month, Day, Hour
df['datetime'] = pd.to_datetime({
    'year': 2025,  # You can change the year if needed
    'month': df['Month'],
    'day': df['Day'],
    'hour': df['Hour']
})
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

# Show filtered data
st.subheader("📄 Filtered Weather Data")
st.dataframe(filtered_df)

# Line Chart of Temperature over time for selected date
st.subheader(f"🌡️ Temperature Trend on {selected_date} in {selected_state}")
temp_day = df[(df['State'] == selected_state) & (df['date_only'] == selected_date)]
st.line_chart(temp_day.set_index('datetime')['Temperature'])

# Summary statistics
st.subheader("📊 Summary Statistics")
st.write(filtered_df.describe())

# Weather type information
st.subheader("🌈 Weather Type")
weather_type = filtered_df['WeatherType'].values[0] if not filtered_df.empty else "N/A"
st.write(f"**Weather:** {weather_type}")

# Download button
st.subheader("⬇️ Download Filtered Data")
st.download_button(
    label="Download as CSV",
    data=filtered_df.to_csv(index=False),
    file_name=f"weather_{selected_state}_{selected_date}_{selected_time}.csv",
    mime="text/csv"
)
