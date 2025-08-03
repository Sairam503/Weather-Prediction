# app.py

import streamlit as st
import pandas as pd
import joblib
import datetime

# 🔁 Load model and encoders
model = joblib.load("./weather_model.pkl")
state_encoder = joblib.load("./state_encoder.pkl")
weather_encoder = joblib.load("./weather_encoder.pkl")

# 📋 App Title
st.title("🌦️ Future Weather Prediction App")

# 🧾 Input Form
state_name = st.selectbox("Select State", state_encoder.classes_)
month = st.slider("Select Month", 1, 12, 1)
day = st.slider("Select Day", 1, 31, 1)
hour = st.slider("Select Hour", 0, 23, 12)
temperature = st.number_input("Temperature (°C)", value=28.0)
humidity = st.number_input("Humidity (%)", value=80.0)
windspeed = st.number_input("Wind Speed (km/h)", value=10.0)

# 🎯 Prediction Button
if st.button("Predict Weather Type"):
    # 🔄 Encode input
    encoded_state = state_encoder.transform([state_name])[0]
    
    # 🔢 Prepare input for prediction
    input_features = pd.DataFrame([[
        encoded_state, month, day, hour, temperature, humidity, windspeed
    ]], columns=['State', 'Month', 'Day', 'Hour', 'Temperature', 'Humidity', 'WindSpeed'])

    # 🧠 Predict
    prediction = model.predict(input_features)[0]
    weather_label = weather_encoder.inverse_transform([prediction])[0]

    # ✅ Display Result
    st.success(f"🌤️ Predicted Weather Type: **{weather_label}**")
