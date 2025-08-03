# model.py

# 📦 Import Required Libraries
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("./processed_weather_data.csv")

# Select only required features
X = df[['State', 'Month', 'Day', 'Hour']]
y = df['WeatherType']

# Encode categorical variables
state_encoder = LabelEncoder()
weather_encoder = LabelEncoder()

X['State'] = state_encoder.fit_transform(X['State'])
y = weather_encoder.fit_transform(y)

# Save encoders
with open('state_encoder.pkl', 'wb') as f:
    pickle.dump(state_encoder, f)
with open('weather_encoder.pkl', 'wb') as f:
    pickle.dump(weather_encoder, f)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
with open('weather_predictor.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved successfully.")
