import streamlit as st
import pickle
import pandas as pd

# Load model and encoders
with open('weather_predictor.pkl', 'rb') as f:
    model = pickle.load(f)
with open('state_encoder.pkl', 'rb') as f:
    state_encoder = pickle.load(f)
with open('weather_encoder.pkl', 'rb') as f:
    weather_encoder = pickle.load(f)

# Streamlit UI
st.title("🌦️ Future Weather Predictor")

state = st.selectbox("Select State", ['Andhra Pradesh'])  # Add more if needed
month = st.number_input("Month (1-12)", min_value=1, max_value=12)
day = st.number_input("Day (1-31)", min_value=1, max_value=31)
hour = st.number_input("Hour (0-23)", min_value=0, max_value=23)

if st.button("Predict Weather"):
    # Encode input
    state_encoded = state_encoder.transform([state])[0]
    input_df = pd.DataFrame([[state_encoded, month, day, hour]], columns=['State', 'Month', 'Day', 'Hour'])

    # Predict
    prediction = model.predict(input_df)[0]
    weather_label = weather_encoder.inverse_transform([prediction])[0]

    st.success(f"🌤️ Predicted Weather: **{weather_label}**")
